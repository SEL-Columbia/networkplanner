'Database objects'
# Import pylons modules
from pylons import config
# Import system modules
import os, socket, signal
import cjson
import urllib
import hashlib
import datetime
import sqlalchemy as sa
import sqlalchemy.orm as orm
import psutil #process info
# Import custom modules
from np.model.meta import Session, Base
from np.config import parameter
from np.lib import store, dataset_store, metric, network


# Define methods

def init_model(engine):
    'Call me before using any of the tables or classes in the model'
    Session.configure(bind=engine)

def hashString(string): 
    'Compute the hash of the string'
    return hashlib.sha256(string).digest()


# Set constants
# Added statusInitializing for the state between constructed/commited scenario
# when it's actually set up with input (in this state, it's NOT ready to be processed)
# Added it to the end of the enum to preserve backward compatibility
statusNew, statusPending, statusDone, statusFailed, statusInitializing = xrange(5)
statusDictionary = {
    statusNew: 'New',
    statusPending: 'Pending',
    statusDone: 'Done',
    statusFailed: 'Failed',
    statusInitializing: 'Initializing',
}
scopePrivate, scopePublic = xrange(2)


# Define tables
people_table = sa.Table('people', Base.metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('username', sa.String(parameter.USERNAME_LENGTH_MAXIMUM), unique=True, nullable=False),
    sa.Column('password_hash', sa.LargeBinary(32), nullable=False),
    sa.Column('nickname', sa.Unicode(parameter.NICKNAME_LENGTH_MAXIMUM), unique=True, nullable=False),
    sa.Column('email', sa.String(parameter.EMAIL_LENGTH_MAXIMUM), unique=True, nullable=False),
    sa.Column('email_sms', sa.String(parameter.EMAIL_LENGTH_MAXIMUM)),
    sa.Column('role', sa.String(parameter.ROLE_LENGTH_MAXIMUM)),
    sa.Column('minutes_offset', sa.Integer, default=0),
    sa.Column('rejection_count', sa.Integer, default=0),
    sa.Column('pickled', sa.LargeBinary),
)
person_candidates_table = sa.Table('person_candidates', Base.metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('username', sa.String(parameter.USERNAME_LENGTH_MAXIMUM), nullable=False),
    sa.Column('password_hash', sa.LargeBinary(32), nullable=False),
    sa.Column('nickname', sa.Unicode(parameter.NICKNAME_LENGTH_MAXIMUM), nullable=False),
    sa.Column('email', sa.String(parameter.EMAIL_LENGTH_MAXIMUM), nullable=False),
    sa.Column('email_sms', sa.String(parameter.EMAIL_LENGTH_MAXIMUM)),
    sa.Column('ticket', sa.String(parameter.TICKET_LENGTH), unique=True, nullable=False),
    sa.Column('when_expired', sa.DateTime, nullable=False),
    sa.Column('person_id', sa.ForeignKey('people.id')),
)
scenarios_table = sa.Table('scenarios', Base.metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('owner_id', sa.ForeignKey('people.id')),
    sa.Column('name', sa.Unicode(parameter.SCENARIO_NAME_LENGTH_MAXIMUM)),
    sa.Column('scope', sa.Integer, default=scopePrivate),
    # NOTE:
    # need to be careful that only scenarios with input are committed with statusNew
    # otherwise they'll fail on processing.  
    # See create method in np.controllers.scenarios for how to handle this
    sa.Column('status', sa.Integer, default=statusNew), 
    sa.Column('when_created', sa.DateTime),
    # We can use mutable=False because we always assign new objects to these variables
    sa.Column('input', sa.PickleType(mutable=False)),
    sa.Column('output', sa.PickleType(mutable=False)),
)
processors_table = sa.Table('processors', Base.metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('ip', sa.String(parameter.IP_LENGTH_MAXIMUM)),
    sa.Column('when_updated', sa.DateTime),
)

jobs_table = sa.Table('jobs', Base.metadata,
    sa.Column('pid', sa.Integer, primary_key=True),
    sa.Column('host', sa.String(parameter.HOST_LENGTH_MAXIMUM), primary_key=True),
    sa.Column('start_time', sa.DateTime, primary_key=True),
    sa.Column('end_time', sa.DateTime, nullable=True),
)

# Define classes
class Job(object):


    @property
    def log_filename(self):
        #make sure the jobs directory exists
        job_log_dir = os.path.join(config['storage_path'], 'jobs')
        if not os.path.exists(job_log_dir):
            os.makedirs(job_log_dir, mode=0o755)
        return os.path.join(job_log_dir, "%s_%s.log" % (self.pid, self.start_time.strftime("%Y%m%d%H%M%S")))

    @staticmethod
    def _current():
        pid = os.getpid()
        host = socket.gethostname()
        job = Session.query(Job).filter(Job.pid == pid and Job.host == host).\
              order_by(Job.start_time.desc()).first()
        return job

    #write message to the log and append a newline
    #meant to be called from the running process without a specific job instance
    @staticmethod
    def log(message):
        job = Job._current()
        if(not job):
            job = Job()
            Session.add(job)
        job._pid_log(message)

    @staticmethod
    def end():
        job = Job._current()
        if(not job):
            # if we're ending a job that hasn't been initialized
            # don't bother
            return 

        job.end_time = datetime.datetime.utcnow()
        job._pid_log("End job")

    #write to this pid's log
    def _pid_log(self, message):
        time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file = open(self.log_filename, 'a')
        log_file.write("%s %s\n" % (time_str, message))
        log_file.close()
        
    def __init__(self):
        self.pid = os.getpid()
        self.host = socket.gethostname()
        proc = psutil.Process(self.pid)
        self.start_time = datetime.datetime.utcfromtimestamp(proc.create_time)

    def kill(self):
        #TODO:  handle the remote host case
        os.kill(self.pid, signal.SIGINT)
        self._pid_log("Kill Job pid %s" % self.pid)


class Person(object):

    def __init__(self, username, password_hash, nickname, email, email_sms=''):
        self.username = username
        self.password_hash = password_hash
        self.nickname = nickname
        self.email = email
        self.email_sms = email_sms
        self.role = "user"

    def __repr__(self):
        return "<Person('%s')>" % self.username


class PersonCandidate(Person):

    def __repr__(self):
        return "<PersonCandidate('%s')>" % self.username


class CaseInsensitiveComparator(orm.properties.ColumnProperty.Comparator):

    def __eq__(self, other):
        return sa.func.lower(self.__clause_element__()) == sa.func.lower(other)


class Scenario(object):

    def __init__(self, owner_id, name, scope):
        self.owner_id = owner_id
        self.name = name[:parameter.SCENARIO_NAME_LENGTH_MAXIMUM]
        self.scope = scope
        self.when_created = datetime.datetime.utcnow()

    def isQueued(self):
        return self.status == statusNew or self.status == statusPending

    def getFolder(self):
        return store.binPath(os.path.join(config['storage_path'], 'scenarios'), self.id)

    def getDataset(self):
        return dataset_store.load(self.getDatasetPath())

    def getDatasetPath(self):
        return os.path.join(self.getFolder(), 'dataset.db')

    def validateParameters(self):
        'Warn if parameters are missing or unknown'
        # Initialize
        scenarioInput = self.input
        pushWarning = lambda x: store.pushWarning(self.id, x)
        configurationPacks = [
            ('Metric', metric.getModel(scenarioInput['metric model name']), scenarioInput['metric configuration']),
            ('Network', network.getModel(scenarioInput['network model name']), scenarioInput['network configuration']),
        ]
        # For each configurationPack,
        for configurationName, configurationModel, configuration in configurationPacks:
            # Load default
            valueByOptionBySection = configurationModel.VariableStore().getValueByOptionBySection()
            # Make sure that the configuration has the same key hierarchy as the default
            for section, valueByOption in valueByOptionBySection.iteritems():
                if section not in configuration:
                    pushWarning('%s section missing: %s' % (configurationName, section))
                    continue
                for option in valueByOption:
                    if option not in configuration[section]:
                        pushWarning('%s option missing: %s > %s' % (configurationName, section, option))
            # Make sure that the input does not have unnecessary parameters
            for section, valueByOption in configuration.iteritems():
                if section not in valueByOptionBySection:
                    pushWarning('%s section unknown: %s' % (configurationName, section))
                    continue
                for option in valueByOption:
                    if option not in valueByOptionBySection[section]:
                        pushWarning('%s option unknown: %s > %s' % (configurationName, section, option))

    def run(self):
        # Prepare
        scenarioInput = self.input
        scenarioFolder = self.getFolder()
        expandPath = lambda x: os.path.join(scenarioFolder, x)
        # Setup status reporting
        from time import localtime, strftime
        time_format = "%Y-%m-%d %H:%M:%S"
        
        # Register demographics
        Job.log("Registering demographics")
        print "%s Registering demographics" % strftime(time_format, localtime())
        nodesPath = expandPath('nodes')
        targetPath = self.getDatasetPath()
        sourcePath = expandPath(scenarioInput['demographic file name'])
        datasetStore = dataset_store.create(targetPath, sourcePath)
        datasetStore.saveNodesSHP(nodesPath)
        datasetStore.saveNodesCSV(nodesPath)
        # Apply metric
        Job.log("Applying metric")
        print "%s Applying metric" % strftime(time_format, localtime())
        metricModel = metric.getModel(scenarioInput['metric model name'])
        metricConfiguration = scenarioInput['metric configuration']
        metricValueByOptionBySection = datasetStore.applyMetric(metricModel, metricConfiguration)
        # Build network
        Job.log("Building network")
        print "%s Building network" % strftime(time_format, localtime())
        networkModel = network.getModel(scenarioInput['network model name'])
        networkConfiguration = scenarioInput['network configuration']
        networkValueByOptionBySection = datasetStore.buildNetwork(networkModel, networkConfiguration, jobLogger=Job)
        # Update metric
        Job.log("Updating metric")
        print "%s Updating metric" % strftime(time_format, localtime())
        metricValueByOptionBySection = datasetStore.updateMetric(metricModel, metricValueByOptionBySection)
        # Save output
        Job.log("Saving output")
        print "%s Saving output" % strftime(time_format, localtime())
        metric.saveMetricsConfigurationCSV(expandPath('metrics-job-input'), metricConfiguration)
        metric.saveMetricsCSV(expandPath('metrics-global'), metricModel, metricValueByOptionBySection)
        datasetStore.saveMetricsCSV(expandPath('metrics-local'), metricModel)
        datasetStore.saveSegmentsSHP(expandPath('networks-existing'), is_existing=True)
        datasetStore.saveSegmentsSHP(expandPath('networks-proposed'), is_existing=False)
        # Bundle
        store.zipFolder(scenarioFolder + '.zip', scenarioFolder)
        # Validate
        self.validateParameters()
        # Save output
        self.output = {
            'variables': { 
                'node': dict((str(x.id), dict(input=x.input, output=x.output)) for x in datasetStore.cycleNodes()),
                'metric': metricValueByOptionBySection,
                'network': networkValueByOptionBySection,
            }, 
            'statistics': { 
                'node': datasetStore.getNodeStatistics(), 
                'metric': datasetStore.getMetricStatistics(), 
                'network': datasetStore.getNetworkStatistics(), 
            }, 
            'warnings': store.popWarnings(self.id),
        }
        # Commit
        Session.commit()

    
    def __repr__(self):
        return '<Scenario(id=%s)>' % self.id

    def exportJSON(self, nodeID=None): 
        'Export the entire scenario using JSON'
        # Prepare
        scenarioOutput = self.output
        # If we want nodeDetail,
        if nodeID is not None:
            # Prepare
            nodeIDString = str(nodeID)
            nodeByIDString = scenarioOutput['variables']['node']
            # If the nodeID does not exist,
            if nodeIDString not in nodeByIDString:
                return cjson.encode({})
            # Return
            return cjson.encode(nodeByIDString[nodeIDString])
        else:
            return cjson.encode({  
                'outputs': {
                    'variables': {
                        'metric': scenarioOutput['variables']['metric'],
                    },
                    'statistics': {
                        'metric': scenarioOutput['statistics']['metric'],
                        'network': scenarioOutput['statistics']['network'],
                    },
                }, 
            }) 


        # If we want everything,
        if complete:
            scenarioInput = self.input
            return cjson.encode({  
                'inputs': scenarioInput,  
                'outputs': scenarioOutput, 
                'formats': dict((x, '%s/scenarios/%s.%s' % (scenarioInput['host url'], self.id, x)) for x in ['html', 'zip', 'geojson', 'json']), 
            }) 

    def postCallback(self):
        'Send POST request to the registered callback URL'
        # If there is no input,
        if not self.input:
            return
        # Get
        callbackURL = self.input.get('callback url')
        # If the scenario does not have a callbackURL,
        if not callbackURL:
            return
        # Send a POST request to the callbackURL
        response = urllib.urlopen(callbackURL, urllib.urlencode(dict(payload=self.exportJSON())))
        if response.code != 200:
            raise Exception('Could not POST to callbackURL "%s"' % callbackURL)

class Processor(object):

    def __init__(self, ip):
        self.ip = ip


# Map classes to tables

orm.mapper(Person, people_table, properties={
    'username': orm.column_property(people_table.c.username, comparator_factory=CaseInsensitiveComparator),
    'nickname': orm.column_property(people_table.c.nickname, comparator_factory=CaseInsensitiveComparator),
    'email': orm.column_property(people_table.c.email, comparator_factory=CaseInsensitiveComparator),
    'email_sms': orm.column_property(people_table.c.email_sms, comparator_factory=CaseInsensitiveComparator),
})
orm.mapper(PersonCandidate, person_candidates_table)
orm.mapper(Scenario, scenarios_table, properties={
    'owner': orm.relation(Person, backref='scenarios'),
    'input': orm.deferred(scenarios_table.c.input, group='pickled'),
    'output': orm.deferred(scenarios_table.c.output, group='pickled'),
})
orm.mapper(Processor, processors_table)

orm.mapper(Job, jobs_table)

# Helpers

def getScopeFilter(personID):
    'Filter by scope'
    # Load public scenarios
    scopeFilter = Scenario.scope == scopePublic
    # If the user is logged in,
    if personID:
        # Load private scenarios as well
        scopeFilter = scopeFilter | (Scenario.owner_id == personID)
    # Return
    return scopeFilter
