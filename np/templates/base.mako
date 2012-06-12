## -*- coding: utf-8 -*-
<html>
<head>
<meta name="author" content="Roy Hyunjin Han" />
<title>${h.SITE_NAME} ${self.title()}</title>
<meta charset="UTF-8"/>
<meta property="og:title" content="${h.SITE_NAME} ${self.title()}"/>
<meta property="og:site_name" content="${h.SITE_NAME}"/>
<meta property="og:type" content="website"/>
<meta property="og:url" content="${request.url}"/>
<meta property="og:description" content="${h.SITE_DESCRIPTION}"/>
<meta name="description" content="${h.SITE_DESCRIPTION}" /> 
<meta name="keywords" content="${h.SITE_KEYWORDS}" /> 
<!-- <link href="styles/reset.css" media="all" rel="stylesheet" type="text/css"/> -->
<!-- <link href="styles/styles.css" media="all" rel="stylesheet" type="text/css"/> -->
<link rel="shortcut icon" href="/files/favicon.ico">
${h.javascript_link('/files/jquery-1.4.2.min.js')}
${h.stylesheet_link('/files/style.css')} 
${h.stylesheet_link('/files/styles.css')}
${h.stylesheet_link('/files/reset.css')}
<style>${self.css()}</style>\
${self.head()}\
<script>
<!-- TODO:  Fix THIS 
$(document).ready(function() {
    function getID(obj) {return /\d+/.exec(obj.id)[0]}
    function getNumber(obj) {return /\d+/.exec(obj)[0]}
    $('.tabOFF').hover( 
        function() {this.className = this.className.replace('OFF', 'ON');}, 
        function() {this.className = this.className.replace('ON', 'OFF');} 
    ).click(function() {$('#' + this.id + '_').toggle();});
    ${self.js()}\
    $('input').addClass('normalFONT');
    $('textarea').addClass('normalFONT');
    $('select').addClass('normalFONT');
    $('a').hover(
        function () {this.className = this.className.replace('OFF', 'ON');}, 
        function () {this.className = this.className.replace('ON', 'OFF');}
    );
});-->
</script>
</head>
<body class=normalFONT>
<a name="top"></a><!-- TODO:  Is this needed? -->
<div class="header">
<div class="headcontainer">
<span id="logo"><a href="${h.url('landing_index')}"><img src="files/images/np-logo-sm.png"></a></span>
<!-- <div id=navigation> -->
<!-- ${self.navigation()} -->
${self.links()}
<!-- </div> end navigation -->
</div> <!-- end headcontainer -->
<div id=toolbar>${self.toolbar()}</div> 
</div> <!-- end header -->
<a id="top"></a><!-- TODO:  Is this needed? -->
<div class="content">
${next.body()}
<div class="footer">${self.footer()}</div>
</div>
</body>
</html>\
<%def name='title()'></%def>\
<%def name='css()'></%def>\
<%def name='head()'></%def>\
<%def name='js()'></%def>\
<%def name='links()'>
<%
linkPacks = [
    # ('Processors', h.url('processor_index')),
    ('Scenarios', h.url('scenario_index')),
    # ('People', h.url('person_index')),
]
%>\
<ul>
% for linkName, linkURL in linkPacks:
% if request.path != linkURL:
<li><a href="${linkURL}" class=link>${linkName}</a></li>
% endif
% endfor
<li><a href="/docs" class=link target="_blank">Learn More</a></li>
<li><a href="/docs/tutorial.html" class=link target="_blank">Tutorial</a></li>
% if not h.isPerson():
% if not request.path.startswith('/people/login'):
<li><a id=person_login href="${h.url('person_login', targetURL=h.encodeURL(request.path))}" class=link>Sign Up / Log In</a></li>
% endif
% else:
<li><a id=person_update href="${h.url('person_update')}" class=link>${session['nickname']}</a></li>
<li><a id=person_logout href="${h.url('person_logout', targetURL=h.encodeURL(request.path))}" class=link>Logout</a></li>
% endif
</ul>
</%def>
<%def name='toolbar()'></%def>\
<%def name='navigation()'></%def>\
<%def name='footer()'>
<div class="footercontainer">
${self.links()}
<p>
© Copyright 2012, <a href="http://modi.mech.columbia.edu/">Modi Research Group</a>  &nbsp;<span style="color: #666">|</span>&nbsp;  <a href="https://github.com/modilabs/networkplanner">Network Planner on Github</a>
</p>
</%def>\
