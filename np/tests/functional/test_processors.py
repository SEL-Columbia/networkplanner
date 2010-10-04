from np.tests import *

class TestProcessorsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='processors', action='index'))
        # Test response...
