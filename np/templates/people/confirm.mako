We've received your ${c.action} request for the following credentials.

Username: ${c.username}
% if hasattr(c, 'password'):
Password: ${c.password}
% endif

Please click on the link below to complete your ${c.action}.
${request.relative_url(h.url('person_confirm', ticket=c.candidate.ticket), to_application=True)}

This ticket expires on ${c.candidate.when_expired.strftime('%A, %B %d, %Y at %H:%M%p')}.
