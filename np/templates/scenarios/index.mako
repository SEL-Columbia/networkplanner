<%inherit file="/base.mako"/>\
\
<%def name="title()">Scenario Index</%def>\
\
<%def name="css()">
.scenarioOFF {color: black; background-color: white} 
.scenarioON {color: black; background-color: yellow}
.alignL {text-align: left}
</%def>\
\
<%def name="head()">
${h.stylesheet_link('/files/dataTables/css/dataTablesNP.css')}
${h.javascript_link('/files/dataTables/dataTablesPlus.min.js')}
</%def>\
\
<%def name="js()">
$('#feedback').click(function() {
    var text = prompt('Please enter your comments below.');
    if (text) {
        $.post("${h.url('scenario_feedback')}", {text: text}, function(data) {
            if (data.isOk) {
                $('#message').html('Thanks!').fadeOut(3000, function () {$(this).html('').show()});
            } else if (data.message) {
                alert(data.message);
            }
        });
    }
});
$('#create').click(function() {
    if (${h.isPerson()}) {
        window.location = "${h.url('new_scenario')}";
    } else {
        window.location = "${h.url('person_login', targetURL=h.encodeURL(h.url('new_scenario')))}";
    }
});
$('.delete').click(function() {
    var scenarioID = getID(this);
    $('#scenario' + scenarioID).hide();
    $.ajax({
        type: 'DELETE',
        url: "${h.url('scenario', id='XXX')}".replace('XXX', scenarioID),
        success: function(data) {
            if (!data.isOk) {
                $('#scenario' + scenarioID).show();
                alert(data.message);
            }
        },
        dataType: 'json'});
});
$('.scenario').hover(
    function() {
        var scenarioID = getID(this);
        var scenarioName = $('#scenarioName' + scenarioID)[0];
        scenarioName.className = scenarioName.className.replace('OFF', 'ON');
    }, 
    function() {
        var scenarioID = getID(this);
        var scenarioName = $('#scenarioName' + scenarioID)[0];
        scenarioName.className = scenarioName.className.replace('ON', 'OFF');
    }
);
$('#scenarios').dataTable({
    "bPaginate": false,
    "bAutoWidth": true,
    "oLanguage": {
        'sSearch': 'Filter'
    },
    "aaSorting": [[ 2, "desc" ]],
    "aoColumns": [
        {'sType': 'string'},
        {'sType': 'string'},
        {'sType': 'title-string'},
        {'sType': 'string'},
        {'sType': 'string'},
        {'bSortable': false}
    ]
});
$('#scenarios_filter input').focus();
</%def>\
\
<%def name="toolbar()">
<input type=button id=create value="Create new scenario" title="Run a scenario using your own datasets and parameters">
<input type=button id=feedback value="Send feedback" title="Send comments or bug reports">
<span id=message></span>
</%def>
\
% if c.scenarios:
<% 
from np import model 
personID = h.getPersonID()
whenIO = h.getWhenIO()
%>
<table class=maximumWidth id=scenarios>
<thead>
<tr>
    <th class=alignL><b>Owner</b></th>
    <th class=alignL><b>Name</b></th>
    <th class=alignL><b>Created</b></th>
    <th class=alignL><b>Status</b></th>
    <th class=alignL><b>Scope</b></th>
</tr>
</thead>
% for scenario in c.scenarios:
<tr class=scenario id=scenario${scenario.id}>
    <td>${scenario.owner.nickname}</td>
    <td class=scenarioOFF id=scenarioName${scenario.id}>${scenario.name}</td>
    <td>
        <span title=${whenIO.toLocal(scenario.when_created).strftime('%Y%m%d%H%M%S')}></span>
        ${whenIO.format(scenario.when_created)}
    </td>
    <td>${model.statusDictionary[scenario.status]}</td>
    <td>${'Public' if scenario.scope == model.scopePublic else 'Private'}</td>
    <td>
        <a class=linkOFF href="${h.url('formatted_scenario', id=scenario.id, format='html')}">View</a>
        &nbsp;
        <a class=linkOFF href="${h.url('formatted_scenario', id=scenario.id, format='zip')}">Download</a>
        &nbsp;
        <a class=linkOFF href="${h.url('scenario_clone', scenarioID=scenario.id)}">Clone</a>
        &nbsp;
    % if personID == scenario.owner_id:
        <a class='linkOFF delete' id=delete${scenario.id}>Delete</a>
    % endif
    </td>
</tr>
% endfor
</table>
% endif
