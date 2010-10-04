## -*- coding: utf-8 -*-
% if 'MSIE' in request.user_agent:
<!doctype html>
% endif
<html>
<head>
<meta name="author" content="Roy Hyunjin Han" />
<link rel="shortcut icon" href="/files/favicon.ico">
${h.javascript_link('/files/jquery-1.4.2.min.js')}
${h.stylesheet_link('/files/style.css')}
<title>${h.SITE_NAME} ${self.title()}</title>
<style>${self.css()}</style>\
${self.head()}\
<script>
$(document).ready(function() {
    $('input').addClass('normalFONT');
    $('textarea').addClass('normalFONT');
    $('select').addClass('normalFONT');
    $('a').hover(
        function () {this.className = this.className.replace('OFF', 'ON');}, 
        function () {this.className = this.className.replace('ON', 'OFF');}
    );
    function getID(obj) {return /\d+/.exec(obj.id)[0]}
    ${self.js()}\
});
</script>
</head>
<body class=normalFONT>
<div id=header>
<div id=toolbar>${self.toolbar()}</div>
<div id=navigation>
${self.navigation()}
<%
linkPacks = [
    ('People', h.url('person_index')),
]
%>\
% for linkName, linkURL in linkPacks:
% if request.path != linkURL:
&nbsp;
<a href="${linkURL}" class=linkOFF>${linkName}</a>
% endif
% endfor
% if not h.isPerson():
% if not request.path.startswith('/people/login'):
&nbsp;
<a id=person_login href="${h.url('person_login', targetURL=h.encodeURL(request.path))}" class=linkOFF>Login</a>
% endif
% else:
&nbsp;
<a id=person_update href="${h.url('person_update')}" class=linkOFF>${session['nickname']}</a>
&nbsp;
<a id=person_logout href="${h.url('person_logout', targetURL=h.encodeURL(request.path))}" class=linkOFF>Logout</a>
% endif
</div>
</div>
<div id=main>${next.body()}</div>
<div id=footer>${self.footer()}</div>
</body>
</html>\
<%def name='title()'></%def>\
<%def name='css()'></%def>\
<%def name='head()'></%def>\
<%def name='js()'></%def>\
<%def name='toolbar()'></%def>\
<%def name='navigation()'></%def>\
<%def name='footer()'></%def>\
