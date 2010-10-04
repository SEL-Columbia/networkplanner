'Scenarios controller'
# Import pylons modules
from pylons import request, tmpl_context as c, url, config
from pylons.controllers.util import redirect, forward
from pylons.decorators import jsonify
from paste.fileapp import FileApp
# Import system modules
import os
import shutil
import cjson
import geojson
import email.utils
from sqlalchemy import orm
# Import custom modules
from np import model
from np.model import Session
from np.config import parameter
from np.lib.base import BaseController, render
from np.lib import helpers as h, metric, network, variable_store, geometry_store, store, smtp


class ScenariosController(BaseController):
    'REST Controller styled on the Atom Publishing Protocol'

    def index(self, format='html'):
        'GET /scenarios: Show all items in the collection'
        # Initialize
        personID = h.getPersonID()
        # Load
        c.scenarios = Session.query(model.Scenario).filter(model.getScopeFilter(personID)).options(orm.eagerload(model.Scenario.owner)).order_by(model.Scenario.when_created.desc()).all()
        # If the desired format is html,
        if format == 'html':
            # Return
            return render('/scenarios/index.mako')

    def new(self, format='html'):
        'GET /scenarios/new: Show form to create a new item'
        # If the user is not logged in,
        if not h.isPerson():
            # Redirect to login
            return redirect(url('person_login', targetURL=h.encodeURL(h.url('new_scenario'))))
        # Make sure that the requested metric model exists
        metricModelNames = metric.getModelNames()
        metricModelName = request.GET.get('metricModel')
        if metricModelName not in metricModelNames:
            metricModelName = metricModelNames[0]
        c.metricModel = metric.getModel(metricModelName)
        c.metricConfiguration = {}
        # Make sure that the requested network model exists
        networkModelNames = network.getModelNames()
        networkModelName = request.GET.get('networkModel')
        if networkModelName not in networkModelNames:
            networkModelName = networkModelNames[0]
        c.networkModel = network.getModel(networkModelName)
        c.networkConfiguration = {}
        # Render form
        c.scenario = None
        return render('/scenarios/new.mako')

    def clone(self, scenarioID):
        'Show form to create a new item based on datasets and parameters from existing scenario'
        # Make sure the user is logged in
        personID = h.getPersonID()
        if not personID:
            return redirect(url('person_login', targetURL=h.encodeURL(request.path)))
        # Make sure the user has access to the scenario
        scenario = Session.query(model.Scenario).filter(model.getScopeFilter(personID)).filter(model.Scenario.id==scenarioID).first()
        if not scenario:
            return redirect(url('new_scenario'))
        # Load
        scenarioInput = scenario.input
        # Prepare
        c.scenario = scenario
        c.metricModel = metric.getModel(request.GET.get('metricModel', scenarioInput['metric model name']))
        c.metricConfiguration = scenarioInput['metric configuration']
        c.networkModel = network.getModel(request.GET.get('networkModel', scenarioInput['network model name']))
        c.networkConfiguration = scenarioInput['network configuration']
        # Return
        return render('/scenarios/new.mako')

    def create(self):
        'POST /scenarios: Create a new item'
        # Initialize
        personID = h.getPersonID()
        if not personID:
            return redirect(url('person_login', targetURL=h.encodeURL(h.url('new_scenario'))))
        # Load
        try:
            demographicDatabase_h = int(request.POST.get('demographicDatabase_h', 0))
        except ValueError:
            demographicDatabase_h = 0
        if not demographicDatabase_h and 'demographicDatabase' not in request.POST:
            return cjson.encode(dict(isOk=0, message='The demographicDatabase field is required'))
        scenarioName = request.POST.get('scenarioName') or 'Untitled'
        try:
            scenarioScope = int(request.POST.get('scenarioScope', model.scopePrivate))
        except ValueError:
            scenarioScope = model.scopePrivate
        metricModelName = request.POST.get('metricModelName', metric.getModelNames()[0])
        networkModelName = request.POST.get('networkModelName', network.getModelNames()[0])
        callbackURL = request.POST.get('callbackURL')
        # Create scenario
        scenario = model.Scenario(personID, scenarioName, scenarioScope)
        Session.add(scenario)
        Session.commit()
        scenarioFolder = store.makeFolderSafely(scenario.getFolder())
        # If the user is using an existing demographicDatabase,
        if demographicDatabase_h:
            # Copy source in case it is deleted
            sourceScenario = Session.query(model.Scenario).get(demographicDatabase_h)
            sourceScenarioFolder = sourceScenario.getFolder()
            demographicFileName = sourceScenario.input['demographic file name']
            demographicPath = os.path.join(scenarioFolder, demographicFileName)
            shutil.copyfile(os.path.join(sourceScenarioFolder, demographicFileName), demographicPath)
        # If the user is uploading a new demographicDatabase,
        else:
            # Save original demographicDatabase in case the user wants it later
            demographicDatabase = request.POST['demographicDatabase']
            demographicFileExtension = os.path.splitext(demographicDatabase.filename)[1]
            demographicFileName = 'demographics' + demographicFileExtension
            demographicPath = os.path.join(scenarioFolder, demographicFileName)
            shutil.copyfileobj(demographicDatabase.file, open(demographicPath, 'wb'))
            demographicDatabase.file.close()
        # Store input
        configurationByName = extractConfigurationByName(request.POST, scenarioFolder)
        scenario.input = {
            'demographic file name': str(demographicFileName),
            'metric model name': metricModelName,
            'metric configuration': configurationByName.get('metric', {}),
            'network model name': networkModelName,
            'network configuration': configurationByName.get('network', {}),
            'callback url': callbackURL,
            'host url': request.host_url, 
        }
        Session.commit()
        store.zipFolder(scenarioFolder + '.zip', scenarioFolder)
        # Redirect
        redirect(url('scenario', id=scenario.id))

    def show(self, id, format='html'):
        'GET /scenarios/id: Show a specific item'
        # If the output format is not supported, 
        if format not in ['html', 'zip', 'geojson', 'json']: 
            return 'Unsupported output format: ' + format 
        # Initialize
        personID = h.getPersonID()
        # Load
        c.scenario = Session.query(model.Scenario).filter(model.Scenario.id==id).filter(model.getScopeFilter(personID)).first()
        # If user does not have access to the scenario,
        if not c.scenario:
            c.status = model.statusFailed
            if format == 'html':
                return render('/scenarios/show.mako')
            elif format == 'zip':
                return ''
            elif format == 'geojson':
                return geojson.dumps(geojson.FeatureCollection([]))
            elif format == 'json':
                return cjson.encode({})
        # If the scenario has an error,
        if c.scenario.status == model.statusFailed:
            c.traceback = c.scenario.output['traceback']
            c.status = model.statusFailed
            if format == 'html':
                return render('/scenarios/show.mako')
            elif format == 'zip':
                return forward(FileApp(c.scenario.getFolder() + '.zip'))
            elif format == 'geojson':
                return geojson.dumps(geojson.FeatureCollection([]))
            elif format == 'json':
                return c.scenario.exportJSON()
        # If the scenario has not been processed,
        if c.scenario.isQueued():
            c.status = model.statusPending
            if format == 'html':
                return render('/scenarios/show.mako')
            elif format == 'zip':
                return forward(FileApp(c.scenario.getFolder() + '.zip'))
            elif format == 'geojson':
                return geojson.dumps(geojson.FeatureCollection([]))
            elif format == 'json':
                return c.scenario.exportJSON()
        # Prepare
        c.status = model.statusDone
        c.scenarioInput = c.scenario.input
        c.scenarioOutput = c.scenario.output
        transformPoint = geometry_store.getTransformPoint(geometry_store.proj4Default, geometry_store.proj4Google)
        # If the user wants HTML,
        if format == 'html':
            # Render scenario
            c.metricModel = metric.getModel(c.scenarioInput['metric model name'])
            scenarioStatistics = c.scenarioOutput['statistics']
            nodeStatistics = scenarioStatistics['node']
            # Prepare map
            centerX, centerY = transformPoint(nodeStatistics['mean longitude'], nodeStatistics['mean latitude'])
            box1X, box1Y = transformPoint(nodeStatistics['minimum longitude'], nodeStatistics['maximum latitude'])
            box2X, box2Y = transformPoint(nodeStatistics['maximum longitude'], nodeStatistics['minimum latitude'])
            # Render map
            datasetStore = c.scenario.getDataset()
            c.mapFeatures = datasetStore.exportGeoJSON(transformPoint)
            c.mapCenter = '%s, %s' % (centerX, centerY)
            c.mapBox = '%s, %s, %s, %s' % (box1X, box1Y, box2X, box2Y)
            # Render nodes
            c.nodes = list(datasetStore.cycleNodes())
            c.populationQuartiles = scenarioStatistics['metric']['population quartiles']
            # Render scenarios
            c.scenarios = Session.query(model.Scenario).filter(model.getScopeFilter(personID)).filter(model.Scenario.status==model.statusDone).filter(model.Scenario.id!=c.scenario.id).order_by(model.Scenario.id.desc()).all()
            # Return
            return render('/scenarios/show.mako')
        elif format == 'zip':
            return forward(FileApp(c.scenario.getFolder() + '.zip'))
        elif format == 'geojson':
            return c.scenario.getDataset().exportGeoJSON(transformPoint)
        elif format == 'json':
            try:
                complete = int(request.params.get('complete', 1))
            except ValueError:
                complete = 1
            return c.scenario.exportJSON(True if complete else False)

    @jsonify
    def check(self, scenarioID):
        # Initialize
        personID = h.getPersonID()
        # Load
        scenario = Session.query(model.Scenario).filter(model.Scenario.id==scenarioID).filter(model.getScopeFilter(personID)).first()
        # Return
        return dict(isOk=0 if not scenario or scenario.isQueued() else 1)

    def edit(self, id, format='html'):
        'GET /scenarios/id/edit: Show form to edit an existing item'
        # url('edit_scenario', id=ID)

    @jsonify
    def update(self, id):
        'PUT /scenarios/id: Update an existing item'
        # Initialize
        personID = h.getPersonID()
        # Load
        scenario = Session.query(model.Scenario).filter(model.Scenario.id==id).first()
        # If the scenario doesn't exist,
        if not scenario:
            return dict(isOk=0, message='Scenario %s does not exist' % id)
        # If the user is not the owner,
        if personID != scenario.owner_id:
            return dict(isOk=0, message='You are not the owner of scenario %s' % id)
        # Load
        scenarioName = request.params.get('scenarioName', '').strip()
        if not scenarioName:
            return dict(isOk=0, message='Please enter a scenario name')
        try:
            scenarioScope = int(request.params.get('scenarioScope'))
        except ValueError:
            return dict(isOk=0, message='Scenario scope must be an integer')
        if scenarioScope not in [model.scopePrivate, model.scopePublic]:
            return dict(isOk=0, message='Scenario scope can either be %s=private or %s=public' % (model.scopePrivate, model.scopePublic))
        # Update
        scenario.name = scenarioName
        scenario.scope = scenarioScope
        # Commit
        Session.commit()
        # Return
        return dict(isOk=1)

    @jsonify
    def delete(self, id):
        'DELETE /scenarios/id: Delete an existing item'
        # Initialize
        personID = h.getPersonID()
        # Load
        scenario = Session.query(model.Scenario).filter(model.Scenario.id==id).first()
        # If the scenario doesn't exist,
        if not scenario:
            return dict(isOk=0, message='Scenario %s does not exist' % id)
        # If the user is not the owner,
        if personID != scenario.owner_id:
            return dict(isOk=0, message='You are not the owner of scenario %s' % id)
        # Delete
        Session.delete(scenario)
        Session.commit()
        # Return
        return dict(isOk=1)

    @jsonify
    def feedback(self):
        'Send feedback'
        # Load
        text = request.POST.get('text', '').strip()
        # If there is text,
        if text:
            # Initialize
            personID = h.getPersonID()
            headerByValue = {}
            # If the person is logged in,
            if personID:
                # Load
                person = Session.query(model.Person).get(personID)
                nickname = person.nickname
                headerByValue['reply-to'] = email.utils.formataddr((nickname, person.email))
            # If th person is not logged in,
            else:
                nickname = 'Anonymous'
            # Send it
            subject = '[%s] Feedback from %s' % (parameter.SITE_NAME, nickname)
            try:
                smtp.sendMessage(
                    config['safe']['mail support'], 
                    config['safe']['mail support'], subject, text, headerByValue)
            except:
                return dict(isOk=0, message='Error sending message')
            # Return
            return dict(isOk=1)
        # Return
        return dict(isOk=0)


# Define helpers

def extractConfigurationByName(valueByName, scenarioFolder):
    # Initialize
    configuration = {}
    # For each value,
    for key, value in valueByName.iteritems():
        # Parse key
        keyTerms = variable_store.parseKey(key)
        # If the key is compound,
        if len(keyTerms) > 1:
            # Extract
            modelType, section, option = keyTerms
            # If the value already exists, then it must have been overridden
            if modelType in configuration:
                if section in configuration[modelType]:
                    if option in configuration[modelType][section]:
                        continue
            # If we have a hidden field,
            if option.endswith('_h'):
                # If the hidden field was overridden, skip this and wait until we find the real value
                if int(value) == 0:
                    continue
                # Remove suffix
                option = option[:-2]
                # Prepare
                sourceScenario = Session.query(model.Scenario).get(value)
                relativePath = sourceScenario.input['%s configuration' % modelType][section][option]
                # If the old scenario did not specify a file here,
                if not relativePath:
                    value = ''
                else:
                    # Prepare
                    sourcePath = os.path.join(sourceScenario.getFolder(), relativePath)
                    # Copy source in case it is deleted
                    store.makeFolderSafely(os.path.join(scenarioFolder, os.path.dirname(relativePath)))
                    targetPath = os.path.join(scenarioFolder, relativePath)
                    shutil.copyfile(sourcePath, targetPath)
                    value = relativePath
            # If the user wants to use a new file and the value is an upload,
            elif hasattr(value, 'file'):
                # Prepare
                relativePath = os.path.join(modelType, section, option + os.path.splitext(value.filename)[1])
                # Save it
                store.makeFolderSafely(os.path.join(scenarioFolder, os.path.dirname(relativePath)))
                targetPath = os.path.join(scenarioFolder, relativePath)
                shutil.copyfileobj(value.file, open(targetPath, 'wb'))
                value = relativePath
            # Store
            if modelType not in configuration:
                configuration[modelType] = {}
            if section not in configuration[modelType]:
                configuration[modelType][section] = {}
            configuration[modelType][section][option] = value
    # Return
    return configuration
