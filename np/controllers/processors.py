'Processors controller'
# Import pylons modules
from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
# Import system modules
import logging; log = logging.getLogger(__name__)
import datetime
# Import custom modules
from np import model
from np.model import Session
from np.lib.base import BaseController, render
from np.lib import helpers as h


class ProcessorsController(BaseController):
    'Methods to track processor status'

    def index(self):
        'Show processors that have updated in the last hour'
        c.processors = Session.query(model.Processor).filter(model.Processor.when_updated > datetime.datetime.utcnow() - datetime.timedelta(hours=1)).order_by(model.Processor.when_updated.desc()).all()
        return render('/processors/index.mako')

    def update(self):
        'Update processor information'
        # Load
        ip = h.getRemoteIP()
        processor = Session.query(model.Processor).filter(model.Processor.ip==ip).first()
        # If the processor doesn't exist,
        if not processor:
            processor = model.Processor(ip)
            Session.add(processor)
        # Update
        processor.when_updated = datetime.datetime.utcnow()
        Session.commit()
