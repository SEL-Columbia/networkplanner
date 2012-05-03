<%
from np import model
personID = h.getPersonID()
whenIO = h.getWhenIO()
%>
% for scenario in c.scenarios:
<tr class=scenario id=scenario${scenario.id}>
    <td>${scenario.owner.nickname}</td>
    <td class=scenarioOFF id=scenarioName${scenario.id}>${scenario.name}</td>
    <td>
        <span title=${whenIO.to_local(scenario.when_created).strftime('%Y%m%d%H%M%S')}></span>
        ${whenIO.format(scenario.when_created)}
    </td>
    <td>${model.statusDictionary[scenario.status]}</td>
    <td>${'Public' if scenario.scope == model.scopePublic else 'Private'}</td>
    <td>
    % if personID == scenario.owner_id:
        <a class='linkOFF delete' id=delete${scenario.id}>Delete</a>
    % endif
        <a class=linkOFF href="${h.url('formatted_scenario', id=scenario.id, format='html')}">View</a>
        &nbsp;
        <a class=linkOFF href="${h.url('formatted_scenario', id=scenario.id, format='zip')}">Download</a>
        &nbsp;
        <a class=linkOFF href="${h.url('scenario_clone', scenarioID=scenario.id)}">Clone</a>
        &nbsp;
    </td>
</tr>
% endfor
