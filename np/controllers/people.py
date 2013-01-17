'People controller'
# Import pylons modules
from pylons import request, session, tmpl_context as c, url, config
from pylons.controllers.util import redirect
from pylons.decorators import jsonify
import formencode
# Import system modules
import recaptcha.client.captcha as captcha
import cStringIO as StringIO
import datetime
# Import custom modules
from np import model
from np.model import Session
from np.config import parameter
from np.lib import smtp, store, helpers as h
from np.lib.base import BaseController, render


class PeopleController(BaseController):
    'Methods to handle registration, authentication and account modification'

    def index(self):
        'Show information about people registered in the database'
        c.people = Session.query(model.Person).all()
        return render('/people/index.mako')

    def register(self):
        'Show account registration page'
        c.isNew = True
        return render('/people/change.mako')

    @jsonify
    def register_(self):
        'Store proposed changes and send confirmation email'
        return changeAccount(dict(request.POST), 'registration', '/people/confirm.mako')

    def confirm(self, ticket):
        'Confirm changes'
        # Send feedback
        candidate = confirmPersonCandidate(ticket)
        # If the candidate exists,
        if candidate:
            messageCode = 'updated' if candidate.person_id else 'created'
        else:
            messageCode = 'expired'
        # Return
        return redirect(url('person_login', targetURL=h.encodeURL('/'), messageCode=messageCode))

    def update(self):
        'Show account update page'
        # Load
        personID = h.getPersonID()
        # If the person is not logged in,
        if not personID:
            # Return
            return redirect(url('person_login', targetURL=h.encodeURL('/')))
        # Render
        c.isNew = False
        person = Session.query(model.Person).get(personID)
        # Return
        return formencode.htmlfill.render(render('/people/change.mako'), {
            'username': person.username,
            'nickname': person.nickname,
            'email': person.email,
            'email_sms': person.email_sms,
        })

    @jsonify
    def update_(self):
        'Send update confirmation email'
        # Load
        personID = h.getPersonID()
        # If the person is not logged in,
        if not personID:
            return dict(isOk=0)
        # Prepare
        person = Session.query(model.Person).get(personID)
        # Return
        return changeAccount(dict(request.POST), 'update', '/people/confirm.mako', person)

    def login(self, targetURL=h.encodeURL('/')):
        'Show login form'
        c.messageCode = request.GET.get('messageCode')
        c.targetURL = h.decodeURL(targetURL)
        c.publicKey = config['safe']['recaptcha']['public']
        return render('/people/login.mako')

    @jsonify
    def login_(self):
        'Process login credentials'
        # Check username
        username = str(request.POST.get('username', ''))
        person = Session.query(model.Person).filter_by(username=username).first()
        # If the username does not exist,
        if not person:
            return dict(isOk=0)
        # Check password
        password_hash = model.hashString(str(request.POST.get('password', '')))
        # If the password is incorrect,
        if password_hash != StringIO.StringIO(person.password_hash).read():
            # Increase and return rejection_count without a requery
            rejection_count = person.rejection_count = person.rejection_count + 1
            Session.commit()
            return dict(isOk=0, rejection_count=rejection_count)
        # If there have been too many rejections,
        if person.rejection_count >= parameter.REJECTION_LIMIT:
            # Expect recaptcha response
            recaptchaChallenge = request.POST.get('recaptcha_challenge_field', '')
            recaptchaResponse = request.POST.get('recaptcha_response_field', '')
            recaptchaKey = config['safe']['recaptcha']['private']
            # Validate
            result = captcha.submit(recaptchaChallenge, recaptchaResponse, recaptchaKey, h.getRemoteIP())
            # If the response is not valid,
            if not result.is_valid:
                return dict(isOk=0, rejection_count=person.rejection_count)
        # Get minutesOffset from UTC
        minutesOffset = h.getMinutesOffset()
        # Save session
        session['minutesOffset'] = minutesOffset
        session['personID'] = person.id
        session['nickname'] = person.nickname
        session['role'] = person.role
        session.save()
        # Save person
        person.minutes_offset = minutesOffset
        person.rejection_count = 0
        Session.commit()
        # Return
        return dict(isOk=1)

    def logout(self, targetURL=h.encodeURL('/')):
        'Logout'
        # If the person is logged in,
        if h.isPerson():
            del session['minutesOffset']
            del session['personID']
            del session['nickname']
            session.save()
        # Redirect
        return redirect(url(h.decodeURL(targetURL)))

    @jsonify
    def reset(self):
        'Reset password'
        # Get email
        email = request.POST.get('email')
        # Try to load the person
        person = Session.query(model.Person).filter(model.Person.email==email).first()
        # If the email is not in our database,
        if not person: 
            return dict(isOk=0)
        # Reset account
        c.password = store.makeRandomAlphaNumericString(parameter.PASSWORD_LENGTH_AVERAGE)
        return changeAccount(dict(
            username=person.username,
            password=c.password,
            nickname=person.nickname,
            email=person.email,
            email_sms=person.email_sms,
        ), 'reset', '/people/confirm.mako', person)


# Validators

class Unique(formencode.validators.FancyValidator):
    'Validator to ensure unique values in a field'

    def __init__(self, fieldName, errorMessage):
        'Store fieldName and errorMessage'
        super(Unique, self).__init__()
        self.fieldName = fieldName
        self.errorMessage = errorMessage

    def _to_python(self, value, person):
        'Check whether the value is unique'
        # If the person is new or the value changed,
        if not person or getattr(person, self.fieldName) != value:
            # Make sure the value is unique
            if Session.query(model.Person).filter(getattr(model.Person, self.fieldName)==value).first():
                # Raise
                raise formencode.Invalid(self.errorMessage, value, person)
        # Return
        return value


class SecurePassword(formencode.validators.FancyValidator):
    'Validator to prevent weak passwords'

    def _to_python(self, value, person):
        'Check whether a password is strong enough'
        if len(set(value)) < 4:
            raise formencode.Invalid('That password needs more variety', value, person)
        return value


class PersonForm(formencode.Schema):
    'Validate user credentials'

    username = formencode.All(
        formencode.validators.String(
            min=parameter.USERNAME_LENGTH_MINIMUM,
            max=parameter.USERNAME_LENGTH_MAXIMUM,
        ),
        Unique('username', 'That username already exists'),
    )
    password = formencode.All(
        formencode.validators.MinLength(
            parameter.PASSWORD_LENGTH_MINIMUM, 
            not_empty=True,
        ), 
        SecurePassword(),
    )
    nickname = formencode.All(
        formencode.validators.PlainText(), 
        formencode.validators.UnicodeString(
            min=parameter.NICKNAME_LENGTH_MINIMUM, 
            max=parameter.NICKNAME_LENGTH_MAXIMUM,
        ),
        Unique('nickname', 'That nickname already exists'),
    )
    email = formencode.All(
        formencode.validators.Email(not_empty=True),
        Unique('email', 'That email is reserved for another account'),
    )
    email_sms = formencode.All(
        formencode.validators.Email(),
        Unique('email_sms', 'That SMS address is reserved for another account'),
    )


# Helpers

def changeAccount(valueByName, action, templatePath, person=None):
    'Validate values and send confirmation email if values are okay'
    try:
        # Validate form
        form = PersonForm().to_python(valueByName, person)
    except formencode.Invalid, error:
        return dict(isOk=0, errorByID=error.unpack_errors())
    else:
        # Purge expired candidates
        purgeExpiredPersonCandidates()
        # Prepare candidate
        candidate = model.PersonCandidate(form['username'], model.hashString(form['password']), form['nickname'], form['email'], form['email_sms'])
        candidate.person_id = person.id if person else None
        candidate.ticket = store.makeRandomUniqueTicket(parameter.TICKET_LENGTH, Session.query(model.PersonCandidate))
        candidate.when_expired = datetime.datetime.utcnow() + datetime.timedelta(days=parameter.TICKET_LIFESPAN_IN_DAYS)
        Session.add(candidate) 
        Session.commit()
        # Prepare recipient
        toByValue = dict(nickname=form['nickname'], email=form['email'])
        # Prepare subject
        subject = '[%s] Confirm %s' % (parameter.SITE_NAME, action)
        # Prepare body
        c.candidate = candidate
        c.username = form['username']
        c.action = action
        body = render(templatePath)
        # Send
        try:
            smtp.sendMessage(config['safe']['mail support'], toByValue, subject, body)
        except smtp.SMTPError:
            return dict(isOk=0, errorByID={'status': 'Unable to send confirmation; please try again later.'})
        # Return
        return dict(isOk=1)

def purgeExpiredPersonCandidates():
    'Delete candidates that have expired'
    Session.execute(model.person_candidates_table.delete().where(model.PersonCandidate.when_expired<datetime.datetime.utcnow()))

def confirmPersonCandidate(ticket):
    'Move changes from the PersonCandidate table into the Person table'
    # Query
    candidate = Session.query(model.PersonCandidate).filter(model.PersonCandidate.ticket==ticket).filter(model.PersonCandidate.when_expired>=datetime.datetime.utcnow()).first()
    # If the ticket exists,
    if candidate:
        # If the person exists,
        if candidate.person_id:
            # Update person
            person = Session.query(model.Person).get(candidate.person_id)
            person.username = candidate.username
            person.password_hash = candidate.password_hash
            person.nickname = candidate.nickname
            person.email = candidate.email
            person.email_sms = candidate.email_sms
            # Reset rejection_count
            person.rejection_count = 0
        # If the person does not exist,
        else:
            # Add person
            Session.add(model.Person(candidate.username, candidate.password_hash, candidate.nickname, candidate.email, candidate.email_sms))
        # Delete ticket
        Session.delete(candidate)
        # Commit
        Session.commit()
    # Return
    return candidate
