# import custom modules
from np import model
from np.model import meta
from np.config import parameter
from np.lib import store, helpers as h
from np.tests import *
from np.lib import variable_store
from np.lib.metric.mvMax4 import demand
from np.lib import dataset_store as ds
import collections

# scenario needs to be associated with a person
username = 'username'
password = 'password'
email = 'username@example.com'
email_sms = ''
nickname = u'nickname'

good_dataset_store_path = "test_data/dataset2/dataset.db"

class TestScenariosController(TestController):

    def setUp(self):
        'Add person'
        meta.Session.query(model.Person).delete()
        meta.Session.query(model.Scenario).delete()
        meta.Session.add(model.Person(username, model.hashString(password), nickname, email))
        meta.Session.commit()

    def tearDown(self):
        'Delete all'
        meta.Session.query(model.Person).delete()
        meta.Session.query(model.Scenario).delete()
        meta.Session.commit()

    def test_run(self):
        'Run the default scenario'
        # Initialize
        # TODO:  REMOVE THE NEED FOR THIS AWKWARD CONFIG SETTING (not understanding pylons config)
        from pylons import config
        config['storage_path'] = self.app.app.config['storage_path']

        # login to set the personID in the session
        resp = self.app.post(url('person_login_'), dict(username=username, password=password))

        householdDemandKey = variable_store.formatKey('metric', demand.HouseholdUnitDemandPerHouseholdPerYear)
        params = {
                'scenarioName': 'scenario1',
                householdDemandKey: 200,
                'metricModelName': 'mvMax4',
                'networkModelName': 'modKruskal'
        }

        upload_file = ('demographicDatabase', u"test_data/demographics_dataset2.csv")

        response = self.app.post(url('scenarios'), params=params, upload_files=[upload_file])
        scenario = meta.Session.query(model.Scenario).filter(model.Scenario.name == 'scenario1').first()
        scenario.run() 

        # compare the dataset from this scenario to a known "good" dataset
        this_dataset = scenario.getDataset()
        good_dataset = ds.load(good_dataset_store_path)

        assert this_dataset.countNodes() == good_dataset.countNodes()
        assert this_dataset.countSegments() == good_dataset.countSegments()
        
        # compare all nodes (just the metrics for now)
        this_nodes = list(this_dataset.cycleNodes())
        good_nodes = list(good_dataset.cycleNodes())
        good_nodes_lookup = collections.defaultdict()
        for good_node in good_nodes: good_nodes_lookup[good_node.x, good_node.y] = good_node
        for i in range(0, len(this_nodes)):
            this_node = this_nodes[i]
            good_node = good_nodes_lookup[this_node.x, this_node.y]
            # Make sure the metric is within a nanometer of
            # the known good metric
            assert abs(this_node.metric - good_node.metric) < 1e-9

        # ensure there are no diffs in sets of segments
        this_segments = set(this_dataset.cycleSegments())
        good_segments = set(good_dataset.cycleSegments())
        assert len(good_segments ^ this_segments) == 0
        
        # compare subnets
        assert this_dataset.countSubnets() == good_dataset.countSubnets()
        this_subnet_counts = [len(sn.segments) for sn in this_dataset.cycleSubnets()]
        good_subnet_counts = [len(sn.segments) for sn in good_dataset.cycleSubnets()]


    def test_index(self):
        response = self.app.get(url('scenarios'))

    def test_create(self):
        response = self.app.post(url('scenarios'))

    def test_new(self):
        response = self.app.get(url('new_scenario'))

    def test_update(self):
        response = self.app.put(url('scenario', id=1))

    def test_update_browser_fakeout(self):
        response = self.app.post(url('scenario', id=1), params=dict(_method='put'))

    def test_delete(self):
        response = self.app.delete(url('scenario', id=1))

    def test_delete_browser_fakeout(self):
        response = self.app.post(url('scenario', id=1), params=dict(_method='delete'))

    def test_show(self):
        response = self.app.get(url('scenario', id=1))

    def test_edit(self):
        response = self.app.get(url('edit_scenario', id=1))
