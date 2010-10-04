'Routines for sending messages'
# Import system modules
import smtplib
import email.message
import email.utils
import socket


def sendMessage(fromByValue, toByValue, subject, body, headerByName=None):
    'Send a message using SMTP'
    # Prepare
    message = email.message.Message()
    message.add_header('from', email.utils.formataddr((fromByValue['nickname'], fromByValue['email'])))
    message.add_header('to', email.utils.formataddr((toByValue['nickname'], toByValue['email'])))
    message.add_header('subject', subject)
    message.set_payload(body)
    if headerByName:
        for key, value in headerByName.iteritems():
            message.add_header(key, value)
    # Connect to server
    if fromByValue['smtp'] == 'localhost':
        server = smtplib.SMTP('localhost')
    else:
        server = smtplib.SMTP_SSL(fromByValue['smtp'], 465)
        if len(fromByValue['username']):
            server.login(fromByValue['username'], fromByValue['password'])
    # Send mail
    try:
        server.sendmail(fromByValue['email'], toByValue['email'], message.as_string())
    except socket.error, error:
        raise SMTPError(error)
    finally:
        server.quit()


class SMTPError(Exception):
    pass
