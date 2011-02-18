<%inherit file='/base.mako'/>\
\
<%def name='title()'>Scenario New</%def>\
\
<%def name='css()'>
td {vertical-align: top}
.option {width: 300px}
.value {width: 300px}
.section {font-weight: bold; font-size: x-large}
.error {color: red}
#network-0_ {display: block}
.message {padding-left: 1em}

% if c.scenario:
.upload {display: none}
% else:
.override {display: none}
% endif
</%def>\
\
<%def name='js()'>
// Buttons
function refresh() {window.location = "${request.path}?metricModel=" + $('#metricModelName').val() + "&networkModel=" + $('#networkModelName').val();}
$('#metricModelName').change(refresh);
$('#networkModelName').change(refresh);
$('#scenarioName').change(validateName);
$('#buttonAdd').click(function() {
    if ($('#demographicDatabase_h').val() == 0 && $('#demographicDatabase').val() == '') {
        alert('Please upload a demographic database');
        $('#demographicDatabase').focus();
        return;
    } 
    if ($('#scenarioName').val() == '') {
        alert('Please enter a scenario name');
        $('#scenarioName').focus();
        return;
    }
    var isOk = true;
    if (!validateName()) isOk = false;
    if (!validateFields('validateNumber', validateNumber)) isOk = false;
    if (!validateFields('validateNumberList', validateNumberList)) isOk = false;
    if (!validateFields('validateCoordinatesList', validateCoordinatesList)) isOk = false;
    if (!isOk) {
        alert('Please correct the indicated fields.');
    } else {
        $('#form').submit();
    }
});

// Validators
function isNumber(x) {return !isNaN(parseFloat(x)) && isFinite(x);}
function getMessageObj(obj) {return $('#' + obj.id + '_m');}
function validateName() {
    var obj = $('#scenarioName');
    var isOk = obj.val().length <= ${h.SCENARIO_NAME_LENGTH_MAXIMUM};
    $('#' + obj.attr('id') + '_m').html(!isOk ? '<span class=error>This name is too long and will be truncated</span>' : '');
    if (!isOk) {
        obj.select();
        obj.focus();
    }
    return isOk;
}
function validateFields(fieldClass, validate) {
    var isOk = true;
    var fields = $('.' + fieldClass);
    for (var i = 0; i < fields.length; i++) {
        var field = fields[i];
        if (!validate(field)) {
            isOk = false;
            $(field).parentsUntil('form').show();
            $(field).focus();
        }
    }
    return isOk;
}
function validateNumber(obj) {
    var isOk = isNumber(obj.value);
    getMessageObj(obj).html(!isOk ? '<span class=error>Must be a number</span>' : '');
    return isOk;
}
function validateNumberList(obj) {
    var isOk = true;
    var numbers = obj.value.split(' ');
    for (var i = 0; i < numbers.length; i++) {
        if (!isNumber(numbers[i])) {
            isOk = false;
        }
    }
    getMessageObj(obj).html(!isOk ? '<span class=error>Must be a list of numbers separated by spaces</span>' : '');
    return isOk;
}
function validateCoordinatesList(obj) {
    var isOk = true;
    var coordinatePacks = obj.value.split(';');
    for (var i = 0; i < coordinatePacks.length; i++) {
        var coordinates = $.trim(coordinatePacks[i]).split(' ');
        for (var j = 0; j < coordinates.length; j++) {
            if (!isNumber(coordinates[j])) {
                isOk = false;
            }
        }
    }
    getMessageObj(obj).html(!isOk ? '<span class=error>Must be a list of coordinates separated by semicolons</span>' : '');
    return isOk;
}
$('.validateNumber').keyup(function() {validateNumber(this)});
$('.validateNumberList').keyup(function() {validateNumberList(this)});
$('.validateCoordinatesList').keyup(function() {validateCoordinatesList(this)});

// Customizations
<%
from np.lib import variable_store
networkExistingNetworksKey = variable_store.formatKey('network', c.networkModel.ExistingNetworks)
%>
$('#${networkExistingNetworksKey}_u').html("<div id=${networkExistingNetworksKey}_s class=upload><a class=linkOFF href='/files/networksXY.zip'>Download sample ZIP containing shapefile</a></div><input id=${networkExistingNetworksKey}_ob class=override type=button value=Override title='Replace with your own dataset'>");
% if c.scenario:
$('.override').click(function() {
    var key = this.id.replace(/_ob$/, '');
    $('#' + key + '_h').val(0);  // Set hidden field to zero
    $('#' + key + '_ob').hide(); // Hide override name
    $('#' + key + '_on').hide(); // Hide override button
    $('#' + key).show();         // Show field
    $('#' + key + '_s').show();  // Show samples
});
% endif
$('#scenarioName').focus();
</%def>\
\
<%def name='toolbar()'>
<input type=button value='Add this scenario to the queue' id=buttonAdd title="Run scenario using the datasets and parameters that you specified below">
</%def>\
\
<%def name='renderConfigurationForm(modelType, modelNames, modelModule, modelConfiguration)'>
<table>
<tr>
<td class="option section">${modelType.capitalize()} model</td>
<td>
<select id="${modelType}ModelName" name="${modelType}ModelName" class=section>
% for modelName in modelNames:
    <option value="${modelName}"\
% if modelName == modelModule.__name__:
    selected=selected\
% endif
    >${modelName}</option>
% endfor
</select>
</td>
</tr>
</table>
<%
from mako.template import Template
from np.lib import variable_store, curve
variableByOptionBySection = modelModule.VariableStore(modelConfiguration).getVariableByOptionBySection()
if modelConfiguration:
    formatValue = lambda x: x.c['format'](x.value)
else:
    formatValue = lambda x: x.default
%>
% for sIndex, section in enumerate(sorted(variableByOptionBySection, key=lambda x: modelModule.sections.index(x))):
    <table id="${modelType}-${sIndex}" class="tabOFF maximumWidth">
        <tr>
            <td class=option></td>
            <td>${section.capitalize()}</td>
        </tr>
    </table>
    <table id="${modelType}-${sIndex}_" class=tab_> 
    <%
    variableByOption = variableByOptionBySection[section]
    %>
    % for option in sorted(variableByOption):
    <%
        variable = variableByOption[option]
        value = formatValue(variable)
        key = variable_store.formatKey(modelType, variable)
    %>
        <tr>
            <td class=option>
                <label for="${key}">
                    <a href="/docs/${modelType}-${modelModule.__name__}.html#${variable_store.formatLabel(variable)}" class=linkOFF target=_blank>${option.capitalize()}</a>
                </label>
            </td>
            <td class=value>${h.literal(Template(variable.c['input']).render(key=key, value=value, validate=variable.c['validate'], scenario=c.scenario))}</td>
            <td id="${key}_u">${variable.units}</td>
            <td id="${key}_m" class=message></td>
        </tr>
    % endfor
    </table>
% endfor
</%def>\
\
<% 
from mako.template import Template
from np import model 
from np.lib import metric, network, variable_store
%>
<form id=form action="${h.url('scenarios')}" enctype="multipart/form-data" method="post">
<table> 
<tr>
    <td>Scenario name</td>
    <td class=value>
        <textarea id=scenarioName name=scenarioName class=maximumWidth>${c.scenario.name + ' clone' if c.scenario else 'Untitled'}</textarea>
    </td>
    <td>
        <select id=scenarioScope name=scenarioScope>
            <option value=${model.scopePrivate}>Private</option>
            <option value=${model.scopePublic}>Public</option>
        </select>
    </td>
    <td id=scenarioName_m></td>
</tr>
<tr>
    <td class=option>Existing locations</td>
    <td class=value>
        ${h.literal(Template(variable_store.inputFile).render(key='demographicDatabase', value=None, scenario=c.scenario))}
    </td>
    <td>
        <div id=demographicDatabase_s class=upload>
            <a class=linkOFF href='/files/demographicsLL.csv'>Download sample CSV in latitude and longitude</a><br>
            <a class=linkOFF href='/files/demographicsXY.csv'>Download sample CSV in x and y</a><br>
            <a class=linkOFF href='/files/demographicsXY.zip'>Download sample ZIP containing shapefile</a><br>
        </div>
        <input id=demographicDatabase_ob class=override type=button value=Override title='Replace with your own dataset'>
    </td>
</tr>
</table>
${renderConfigurationForm('metric', metric.getModelNames(), c.metricModel, c.metricConfiguration)}
<br>
${renderConfigurationForm('network', network.getModelNames(), c.networkModel, c.networkConfiguration)}
</form>
