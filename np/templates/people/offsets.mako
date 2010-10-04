<% import datetime; utcNow = datetime.datetime.utcnow() %>
% for offset in xrange(1440, 0, -30):
<option value=${offset}>${(utcNow + datetime.timedelta(minutes=-offset)).strftime('%I:%M %p')}</option>
% endfor
