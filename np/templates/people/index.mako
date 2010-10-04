<%inherit file="/base.mako"/>

<%def name="title()">People</%def>

<%def name="toolbar()">${len(c.people)} people</%def>

<%
import random
random.shuffle(c.people)
%>

% for person in c.people:
${person.nickname}<br>
% endfor
