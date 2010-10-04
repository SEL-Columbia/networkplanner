from np.tests import *

class TestScenariosController(TestController):

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
