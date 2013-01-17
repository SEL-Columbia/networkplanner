'Jobs controller'
# Import pylons modules
from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify
from paste.fileapp import FileApp
# Import system modules
import logging; log = logging.getLogger(__name__)
import datetime
import os
# Import custom modules
from np import model
from np.model import Session
from np.lib.base import BaseController, render
from np.lib import helpers as h


class JobsController(BaseController):
    'Methods to view and interact with jobs'

    def index(self):
        'Show 10 most recent jobs'
        c.jobs = Session.query(model.Job).order_by(model.Job.start_time.desc()).limit(10).all()
        return render('/jobs/index.mako')

    def show(self, jobID, host):
        'Show the job log'
        c.jobID = jobID
        c.host = host
        return render('/jobs/show.mako')

    @jsonify
    def kill(self, jobID, host):
        'Attempt to kill the job'
        job = Session.query(model.Job).filter(model.Job.pid == jobID and model.Job.host == host).first()
        if (not job) or (job.end_time) or (not h.isAdmin()):
            return dict(isOk=0)
        else:
            job.kill()
        return dict(isOk=1)

    def log(self, jobID, host):
        'Show the log for the job'
        job = Session.query(model.Job).filter(model.Job.pid == jobID and model.Job.host == host).first()
        filepath = job.log_filename 
        file_size = os.path.getsize(filepath)
        headers = [('Content-Type', 'text/plain'), ('Content-Length', str(file_size))]
        fapp = FileApp(filepath, headers=headers)
        return fapp(request.environ, self.start_response)

