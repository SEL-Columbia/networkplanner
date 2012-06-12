'Landing controller'
# Import pylons modules
from pylons import request, tmpl_context as c, url, config
from pylons.controllers.util import redirect, forward
# Import custom modules
from np.lib.base import BaseController, render
from np.lib import helpers as h

class LandingController(BaseController):
    
    def index(self, format='html'):
        'GET /: Show landing page if not logged in'
        # Initialize
        personID = h.getPersonID()
        # If not logged in,
        if not personID:
            return render('/landing/index.mako')
        # Take them to the scenarios,
        else:
            return redirect(url('scenario_index'))

