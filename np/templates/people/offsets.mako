<% import datetime; utcNow = datetime.datetime.utcnow() %>
% for offset in xrange(1410, -1, -30):
<option value=${offset}>${(utcNow + datetime.timedelta(minutes=-offset)).strftime('%I:%M %p')}</option>
% endfor
