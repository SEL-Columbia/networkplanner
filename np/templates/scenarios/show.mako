<%inherit file="/base.mako"/>

<%def name="title()">
Scenario 
% if c.scenario:
${c.scenario.id} - ${c.scenario.name}
% endif
</%def>

<%def name="footer()"></%def>

<%def name="css()">
table {border-spacing: 0}
#legend {padding-top: 5px; padding-bottom: 5px;}
#map {position: absolute; top: 85; left: 0; width: 50%; height: 50%}
#information {position: absolute; top: 70; right: 0; width: 49%; overflow: auto}
#nodeSummary {position: absolute; bottom: 0; left: 0; width: 50%; height: 35%; overflow: auto}
#node {display: none}
#scenarioName {font-size: xx-large; margin-bottom: 10px}
#scenarioEdit {display: none; margin-bottom: 10px}
.summary1 {width: 31%}
.summary2 {width: 23%}
.summary3 {width: 23%}
.summary4 {width: 23%}
.flag {font-size: small; color: gray}

.positive {color: green}
.negative {color: red}

.nodeNormal {background-color: white} 
.nodeHover {background-color: #ff9900}
.nodeSelect {background-color: #ffff00}

.alignL {text-align: left}
.alignR {text-align: right}
.tableHeader {padding-right: 1em}

#nodeName {font-size: xx-large; margin-bottom: 20px; display: none}
#nodeInput {margin-bottom: 20px}
.nodeSection {font-size: x-large; font-weight: bold}
.value {font-weight: bold}
.plot {width: 300px; height: 100px}
</%def>

<%def name='head()'>
${h.stylesheet_link('/files/dataTables/css/dataTablesNP.css')}
${h.javascript_link('/files/dataTables/dataTablesPlus.min.js')}
${h.javascript_link('/files/flot/jquery.flot.min.js')}
% if 'MSIE' in request.environ.get('HTTP_USER_AGENT', ''):
${h.javascript_link('/files/flot/excanvas.min.js')}
% endif
${h.stylesheet_link('/files/openlayers/theme/default/style.css')}
${h.javascript_link('/files/openlayers/OpenLayers.js')}
${h.javascript_link('http://maps.google.com/maps/api/js?sensor=false')}
<style>
.olControlScaleLine {left: 5px; bottom: 40px}
.olLayerGoogleCopyright {display: none}
</style>
</%def>

<%def name="js()">
<% 
from np import model
from np.lib import variable_store
%>
% if c.status == model.statusPending:
    var secondsUntilRefreshDefault = 60;
    var secondsUntilRefresh = secondsUntilRefreshDefault;
    var intervalRefresh = window.setInterval(function () {
    var ending = secondsUntilRefresh > 1 ? 's' : '';
    $('#message').html('Checking scenario status in ' + secondsUntilRefresh + ' second' + ending + '...');
    secondsUntilRefresh -= 1;
    if (!secondsUntilRefresh) {
        $.get("${h.url('scenario_check', scenarioID=c.scenario.id)}", function(data) {
            if (data.isOk) {
                $('#message').html('Scenario has been processed.  Please be patient while the page refreshes...');
                window.clearInterval(intervalRefresh);
                window.location.reload(true);
            }
        });
        secondsUntilRefresh = secondsUntilRefreshDefault;
    }
}, 1000);
% elif c.status == model.statusDone:
// Add styling rules for system type and population
var myStyles = new OpenLayers.StyleMap({
   'default': new OpenLayers.Style({
        fillColor: '#6633FF',
        fillOpacity: 0.4,
        strokeColor: '#6633FF',
        strokeOpacity: 1,
        strokeWidth: 1.1,
        strokeDashstyle: 'solid',
        strokeLinecap: 'round',
        extendDefault: 'true',
        display: 'visible'
    },
    {
        rules: [
            new OpenLayers.Rule({
                filter: new OpenLayers.Filter.Comparison({
                    type: OpenLayers.Filter.Comparison.LESS_THAN,
                    property: 'population',
                    value: ${c.populationQuartiles[0]}
                }),
                symbolizer: { pointRadius: 4 }
            }),
            new OpenLayers.Rule({
                filter: new OpenLayers.Filter.Comparison({
                    type: OpenLayers.Filter.Comparison.BETWEEN,
                    property: 'population',
                    lowerBoundary: ${c.populationQuartiles[0]},
                    upperBoundary: ${c.populationQuartiles[1]}
                }),
                symbolizer: { pointRadius: 6 }
            }),
            new OpenLayers.Rule({
                filter: new OpenLayers.Filter.Comparison({
                    type: OpenLayers.Filter.Comparison.BETWEEN,
                    property: 'population',
                    lowerBoundary: ${c.populationQuartiles[1]},
                    upperBoundary: ${c.populationQuartiles[2]}
                }),
                symbolizer: { pointRadius: 8 }
            }),
            new OpenLayers.Rule({
                filter: new OpenLayers.Filter.Comparison({
                    type: OpenLayers.Filter.Comparison.GREATER_THAN_OR_EQUAL_TO,
                    property: 'population',
                    value: ${c.populationQuartiles[2]},
                }),
                symbolizer: { pointRadius: 10 }
            }),
            new OpenLayers.Rule({
                elseFilter: true, // applies to everything else- need this to display line segments
                symbolizer: { }
            })
        ]
    }),
    'temporary': new OpenLayers.Style({ 
        fillColor: '#ff9900', 
        fillOpacity: 1, 
        strokeColor: '#ff9900', 
        strokeOpacity: 1, 
        strokeWidth: 1.1
    }),
    'select': new OpenLayers.Style({
        fillColor: '#ffff00',
        fillOpacity: 1,
        strokeColor: '#ffff00',
        strokeOpacity: 1,
        strokeWidth: 1.1
    })
});
// Change style based on system type
myStyles.addUniqueValueRules('default', 'system', {
    'unelectrified': {fillColor: '#000000', strokeColor: '#000000', strokeWidth: 1},
    'off-grid': {fillColor: '#00CC00', strokeColor: '#00CC00', strokeWidth: 1},
    'mini-grid': {fillColor: '#CC0033', strokeColor: '#CC0033', strokeWidth: 1},
    'grid': {fillColor: '#6633FF', strokeColor: '#6633FF', strokeWidth: 1}
});
// Change line layer style based on existing or proposed type
myStyles.addUniqueValueRules('default', 'is_existing', {
    1: { strokeDashstyle: 'solid' },
    0: { strokeDashstyle: 'dash' }
});

// Define map
var map = new OpenLayers.Map('map');
var layerSwitcher = new OpenLayers.Control.LayerSwitcher();
map.addControl(layerSwitcher);
map.addControl(new OpenLayers.Control.ScaleLine());
map.addLayers([
    new OpenLayers.Layer.Google("Google Physical", {type: google.maps.MapTypeId.TERRAIN}),
    new OpenLayers.Layer.Google("Google Streets", {numZoomLevels: 20}),
    new OpenLayers.Layer.Google("Google Hybrid", {type: google.maps.MapTypeId.HYBRID, numZoomLevels: 20}),
    new OpenLayers.Layer.Google("Google Satellite", {type: google.maps.MapTypeId.SATELLITE, numZoomLevels: 22})
]);
map.setCenter(new OpenLayers.LonLat(${c.mapCenter}), map.getZoomForExtent(new OpenLayers.Bounds(${c.mapBox})) - 1);
// Add features
var layer1 = new OpenLayers.Layer.Vector('Scenario ${c.scenario.id}', {styleMap: myStyles});
var geoJSONReader = new OpenLayers.Format.GeoJSON();
layer1.addFeatures(geoJSONReader.read(${h.literal(c.mapFeatures)}));
map.addLayer(layer1);
// Store
var featureByFeatureID = {}, featureCount = layer1.features.length;
for (var i=0; i<featureCount; i++) {
    var feature = layer1.features[i];
    featureByFeatureID[feature.fid] = feature;
}

// Prepare node data
var scenario1Data = eval('(${h.literal(c.scenario.exportJSON())})')
var scenario2Data;
function isNumber(x) {return !isNaN(parseFloat(x)) && isFinite(x)}
function isInteger(x) {return parseInt(x) == Number(x)}
function formatInteger(x) {
    return addCommas(parseInt(Math.round(x)));
}
function formatFloat(x) {
    var xParsed = parseFloat(x);
    var xFormatted = addCommas(xParsed.toFixed(2));
    if (xFormatted == '0.00' && xParsed != 0) {
        xFormatted = xParsed.toPrecision(2);
    }
    return xFormatted;
}
// Define node summary
var nodeSummaryHover, scrollNodeSummary = 1;
function showNodeSummary(nodeID) {
    if (nodeSummaryHover) {
        nodeSummaryHover.attr('className', nodeSummaryHover.attr('className').replace('nodeHover', 'nodeNormal'));
    }
    nodeSummaryHover = $('#nodeSummary' + nodeID);
    nodeSummaryHover.attr('className', nodeSummaryHover.attr('className').replace('nodeNormal', 'nodeHover'));
    if (scrollNodeSummary) {
        $('#nodeSummary').scrollTop($('#nodeSummary').scrollTop() + nodeSummaryHover.position().top - $('#nodeSummary').height() / 2);
    }
}
// Define node detail
function loadNodeDetail(nodeID, callback) {
    // Initialize
    var variables = scenario1Data.outputs.variables;
    if (variables.node === undefined) variables.node = {};
    // If the node detail is cached,
    if (variables.node[nodeID] !== undefined) {
        callback(nodeID);
    }
    // Get node detail from server
    $.get("${h.url('formatted_scenario', id=c.scenario.id, format='json')}", {
        nodeID: nodeID
    }, function(data) {
        // Cache it
        variables.node[nodeID] = eval('(' + data + ')');
        // Do something with it
        callback(nodeID);
    });
}
function showNodeDetail(nodeID) {
    // Change style for corresponding node summary
    var nodeSummarySelect = $('#nodeSummary' + nodeID);
    nodeSummarySelect.attr('className', nodeSummarySelect.attr('className').replace('nodeHover', 'nodeSelect'));
    // Hide scenario-level information
    $('#scenarioSummary').hide();
    // Show node detail
    $('#node').show();
    var nodeData = scenario1Data.outputs.variables.node[nodeID];
    var nodeInputByOption = nodeData.input;
    $('#nodeName').html(nodeInputByOption['name'] || 'Node ' + nodeID).show();
    var nodeInputParts = [];
    for (var option in nodeInputByOption) {
        if ($.trim(option).length && option != 'x' && option != 'y' && option != 'name') {
            var value = nodeInputByOption[option];
            if (value != '') {
                nodeInputParts.push(option + ' = <span class=value>' + value + '</span>');
            }
        }
    }
    $('#nodeInput').html(nodeInputParts.join('<br>'));
    var nodeOutputByOptionBySection = nodeData.output;
    for (var section in nodeOutputByOptionBySection) {
        var nodeOutputByOption = nodeOutputByOptionBySection[section];
        for (var option in nodeOutputByOption) {
            var value = nodeOutputByOption[option];
            var target = $(("#metric${variable_store.separator}" + section + "${variable_store.separator}" + option).replace(/ /g, '11').replace(/\(/g, '22').replace(/\)/g, '33'));
            if (/curve$/.test(option)) {
                var sectionTable = target.parent().parent().parent().parent();
                var sectionTableIsVisible = sectionTable.is(':visible');
                sectionTable.show();
                $.plot(target, [eval(value.split(';')[1])]);
                if (!sectionTableIsVisible) sectionTable.hide()
            } else {
                if (isInteger(value)) {
                    value = formatInteger(value);
                } else if (isNumber(value)) {
                    value = formatFloat(value);
                }
                target.html(value);
            }
        }
    }
}
function hideNodeDetail(nodeID) {
    // Hide node detail
    $('#node').hide();
    // Change style for corresponding node summary
    var nodeSummarySelect = $('#nodeSummary' + nodeID);
    nodeSummarySelect.attr('className', nodeSummarySelect.attr('className').replace('nodeSelect', 'nodeNormal'));
    // Show scenario-level information
    $('#scenarioSummary').show();
}

// Add node summary hover
$('.nodeSummary').hover(
    function() {
        scrollNodeSummary = 0;
        hoverControl.overFeature(featureByFeatureID['n' + getID(this)]);
    },
    function() {
        hoverControl.outFeature(featureByFeatureID['n' + getID(this)]);
        scrollNodeSummary = 1;
    }
);
// Add node summary select
var previousNode;
$('.nodeSummary').click(
    function() {
        // Unselect all map features
        if (previousNode != getID(this)) {
            selectControl.unselectAll();
            // Select the map feature
            selectControl.select(featureByFeatureID['n' + getID(this)]);
            previousNode = getID(this);
        }
    },
    function() {}
);

// Manage popup
var popup;
function destroyPopup() {
    if (popup) {
        map.removePopup(popup);
        popup.destroy();
        popup = null;
    }
}
// Add map hover
var hoverControl = new OpenLayers.Control.SelectFeature([layer1], {
    renderIntent: 'temporary',
    hover: true,
    highlightOnly: true,
    eventListeners: {
        featurehighlighted: function(e) {
            var feature = e.feature, featureID = feature.fid;
            // If the feature is a node,
            if (featureID[0] == 'n') {
                showNodeSummary(getNumber(featureID));
            }
            // If the feature is a segment,
            else {
                destroyPopup();
                popup = new OpenLayers.Popup.FramedCloud(featureID, feature.geometry.getBounds().getCenterLonLat(), null, (feature.attributes.is_existing == 1 ? 'Existing' : 'Proposed') + ' medium voltage line: ' + addCommas(feature.attributes.weight) + ' m', null, false, function() {});
                popup.contentDiv.style.fontSize = 'small';
                map.addPopup(popup);
                popup.events.register('click', map, function() {
                    destroyPopup();
                });
            }
        },
        featureunhighlighted: function(e) {
            destroyPopup();
        }
    }
});
map.addControl(hoverControl);
hoverControl.activate();

// Add map select
var selectControl = new OpenLayers.Control.SelectFeature([layer1], {
    renderIntent: 'select',
    hover: false,
    highlightOnly: false,
    onSelect: function(f) {
        // If the feature is a node,
        if (f.fid[0] == 'n') {
            loadNodeDetail(getNumber(f.fid), showNodeDetail);
        }
    },
    onUnselect: function(f) {
        // If the feature is a node,
        if (f.fid[0] == 'n') {
            hideNodeDetail(getNumber(f.fid));
        }
    }
});
map.addControl(selectControl);
selectControl.activate();

function addCommas(x) {
    var parts = (x + '').split('.');
    var pattern = /(\d+)(\d{3})/;
	x1 = parts[0];
	x2 = parts.length > 1 ? '.' + parts[1] : '';
	while (pattern.test(x1)) {
		x1 = x1.replace(pattern, '$1' + ',' + '$2');
	}
	return x1 + x2;
}

<%
countBySystem = c.scenarioOutput['statistics']['metric']['count by system']
metricByOptionBySection = c.scenarioOutput['variables']['metric']
networkStatisticByName = c.scenarioOutput['statistics']['network']
%>
var comparisonLayer;
$('#compare').change(function() {
    // If the comparisonLayer is not defined,
    if (!comparisonLayer) {
        comparisonLayer = new OpenLayers.Layer.Vector('Compare', {styleMap: myStyles});
        map.addLayer(comparisonLayer);
    }
    // Destroy current features in layer
    comparisonLayer.destroyFeatures();
    // Load scenarioID
    var scenarioID = this.value;
    // Set
    layerSwitcher.maximizeControl();
    comparisonLayer.setName('Scenario ' + scenarioID);
    // Load geojson for scenario
    $.get('/scenarios/' + scenarioID + '.geojson', function(data) {
        // Add features to layer
        comparisonLayer.addFeatures(geoJSONReader.read(data));
    });
    // Load JSON for scenario
    $.get('/scenarios/' + scenarioID + '.json', {complete: 0}, function(data) {
        $('#scenario2').html('<b>Scenario ' + scenarioID + '</b>');
        scenario2Data = eval('(' + data + ')');
        showDiff(['variables', 'metric', 'system (off-grid)', 'system total discounted cost'], 'off_grid_cost', '$XXX');
        showDiff(['variables', 'metric', 'system (mini-grid)', 'system total discounted cost'], 'mini_grid_cost', '$XXX');
        showDiff(['variables', 'metric', 'system (grid)', 'system total discounted cost'], 'grid_cost', '$XXX');
        showDiff(['variables', 'metric', 'system (off-grid)', 'system total levelized cost'], 'off_grid_lcoe', '$XXX / kWh', formatFloat);
        showDiff(['variables', 'metric', 'system (mini-grid)', 'system total levelized cost'], 'mini_grid_lcoe', '$XXX / kWh', formatFloat);
        showDiff(['variables', 'metric', 'system (grid)', 'system total levelized cost'], 'grid_lcoe', '$XXX / kWh', formatFloat);
        showDiff(['statistics', 'metric', 'count by system', 'unelectrified'], 'unelectrified_count', 'XXX');
        showDiff(['statistics', 'metric', 'count by system', 'off-grid'], 'off_grid_count', 'XXX');
        showDiff(['statistics', 'metric', 'count by system', 'mini-grid'], 'mini_grid_count', 'XXX');
        showDiff(['statistics', 'metric', 'count by system', 'grid'], 'grid_count', 'XXX');
        showDiff(['statistics', 'network', 'old segment weight'], 'grid_length_old', 'XXX m');
        showDiff(['statistics', 'network', 'new segment weight'], 'grid_length_new', 'XXX m');
        $('#download2').html('<a class=linkOFF href="' + "${h.url('formatted_scenario', id='XXX', format='zip')}".replace('XXX', scenarioID) + '">Download</a>');
        $('#download2 a').hover(
            function () {this.className = this.className.replace('OFF', 'ON');}, 
            function () {this.className = this.className.replace('ON', 'OFF');}
        );
    });
});
function followKeys(keys, x) {
    for (var i = 0; i < keys.length; i++) {
        x = x[keys[i]];
    }
    return x;
}
function showDiff(keys, id, template, format) {
    if (!format) format = formatInteger;

    var value1 = followKeys(keys, scenario1Data.outputs);
    var value2 = followKeys(keys, scenario2Data.outputs);
    if (typeof value1 == 'undefined') value1 = 0;
    if (typeof value2 == 'undefined') value2 = 0;

    var difference = value2 - value1;
    var differenceObj = $('#' + id + '_diff');

    $('#' + id + '_2').html(template.replace('XXX', format(value2)));
    differenceObj.html(template.replace('XXX', format(difference))).removeClass('positive negative');

    if (difference > 0) {
        differenceObj.addClass('positive');
    } else if (difference < 0) {
        differenceObj.addClass('negative');
    }
}


% if h.getPersonID() == c.scenario.owner_id:
$('#scenarioName').hover(
    function() {$(this).append('<span class=flag> click to edit</span>')},
    function() {$(this).find('span.flag').remove()}
).click(function() {
    var obj = $(this);
    obj.find('span.flag').remove();
    $('#scenarioName').hide();
    $('#scenarioEdit').show();
    $('#scenarioEditName').focus();
});
$('#scenarioEditSave').click(function() {
    var scenarioName = $('#scenarioEditName').val();
    if (!scenarioName) {
        alert('Please enter a scenario name');
        $('#scenarioEditName').focus();
        return;
    }
    $('#scenarioEdit').hide();
    $('#scenarioName').html(scenarioName).show();
    updateScenario(scenarioName, $('#scenarioEditScope').val());
});
$('#scenarioEditCancel').click(function() {
    $('#scenarioEdit').hide();
    $('#scenarioName').show();
});
function updateScenario(scenarioName, scenarioScope) {
    $.ajax({
        type: 'PUT',
        url: "${h.url('scenario', id=c.scenario.id)}",
        data: {scenarioName: scenarioName, scenarioScope: scenarioScope},
        success: function(data) {
            if (!data.isOk) alert(data.message);
        },
        dataType: 'json'});
}
% endif

// Implement dataTable
$('#nodeSummaryTable').dataTable({
    "bPaginate": false,
    "bAutoWidth": true,
    "oLanguage": {
        'sSearch': 'Filter'
    },
    "aoColumns": [
        {'sType': 'string'},
        {'sType': 'formatted-num'},
        {'sType': 'currency'},
        {'sType': 'currency'},
        {'sType': 'currency'},
        {'sType': 'string'}
    ]
});
$('#nodeSummaryTable_filter input').focus();
% endif
</%def>

<%def name='toolbar()'>
</%def>

<div id=legend>
Legend &nbsp; 
<span class="normalFONT">
<span style='background-color: #000000; opacity: 0.4'>&nbsp; &nbsp; </span> Unelectrified &nbsp;
<span style='background-color: #00CC00; opacity: 0.4'>&nbsp; &nbsp; </span> Off-grid &nbsp;
<span style='background-color: #CC0033; opacity: 0.4'>&nbsp; &nbsp; </span> Mini-grid &nbsp;
<span style='background-color: #6633FF; opacity: 0.4'>&nbsp; &nbsp; </span> Grid &nbsp;
</span>
</div>

<%
from np import model
formatNumber = lambda x: h.format_number(int(round(float(x))))
formatFloat = lambda x: h.format_number('%0.2f' % float(x))
%>

% if not c.scenario:
You do not have access to this scenario, either because it is private to its owner or it does not exist.
% elif c.status == model.statusPending:
<div id=message></div>
% elif c.status == model.statusFailed:
<pre>${c.traceback}</pre>
% endif

<div id=map></div>


% if c.status == model.statusDone:
<div class=normalFONT id=nodeSummary>
<table class="normalFONT maximumWidth" id="nodeSummaryTable">
    <thead>
        <tr>
            <th class="alignL tableHeader"><b>Name</b></th>
            <th class="alignR tableHeader"><b>Pop</b></th>
            <th class="alignR tableHeader"><b>Off-grid</b></th>
            <th class="alignR tableHeader"><b>Mini-grid</b></th>
            <th class="alignR tableHeader"><b>Grid internal</b></th>
            <th class="alignR tableHeader"><b>System</b></th>
        </tr>
    </thead>
    <tbody>
% for node in c.nodes:
<%
    nodeID = node.id
    nodeInput = node.input
    nodeOutput = node.output
%>
    <tr id="nodeSummary${nodeID}" class="nodeSummary nodeNormal">
        <td class=alignL>${nodeInput.get('name', 'Node %s' % nodeID).title()}</td>
        <td class=alignR>${formatNumber(nodeOutput['demographics']['population count'])}</td>
        <td class=alignR>$${formatNumber(nodeOutput['system (off-grid)']['system nodal discounted cost'])}</td>
        <td class=alignR>$${formatNumber(nodeOutput['system (mini-grid)']['system nodal discounted cost'])}</td>
        <td class=alignR>$${formatNumber(nodeOutput['system (grid)']['internal system nodal discounted cost'])}</td>
        <td class=alignR>${nodeOutput['metric']['system']}</td>
    </tr>
% endfor
   </tbody>
</table>
</div>
% endif


<div class=normalFONT id=information>
% if c.status == model.statusDone:
<%
countBySystem = c.scenarioOutput['statistics']['metric']['count by system']
metricByOptionBySection = c.scenarioOutput['variables']['metric']
networkStatisticByName = c.scenarioOutput['statistics']['network']
personID = h.getPersonID()
%>
<div class=normalFONT id=scenarioSummary>
<div id=scenarioName>${c.scenario.name}</div>
% if personID == c.scenario.owner_id:
<div id=scenarioEdit>
    <textarea id=scenarioEditName class="maximumWidth normalFONT" rows=3>${c.scenario.name}</textarea><br>
    <select id=scenarioEditScope>
        <option value=${model.scopePrivate}>Private</option>
        <option value=${model.scopePublic}>Public</option>
    </select>
    <input id=scenarioEditSave type=button value=Save title="Save changes">
    <input id=scenarioEditCancel type=button value=Cancel title="Cancel changes">
</div>
% endif
<table class="normalFONT maximumWidth">
    <tr>
        <td class="summary1"></td>
        <td class="summary2 alignR" id=scenario1>
            <b>Scenario ${c.scenario.id}</b>
        </td>
        <td class="summary3 alignR" id=scenario2>
            <b>Comparison</b>
        </td>
        <td class="summary4 alignR" id=diff>
            <b>Difference</b>
        </td>
    </tr>
    <tr>
        <td class="summary1">Unelectrified</td>
        <td class="summary2 alignR" id=unelectrified_count_1>${countBySystem.get('unelectrified', 0)}</td>
        <td class="summary3 alignR compare" id=unelectrified_count_2></td>
        <td class="summary4 alignR compare" id=unelectrified_count_diff></td>
    </tr>
    <tr>
        <td class="summary1">Off-grid</td>
        <td class="summary2 alignR" id=off_grid_count_1>${countBySystem.get('off-grid', 0)}</td>
        <td class="summary3 alignR compare" id=off_grid_count_2></td>
        <td class="summary4 alignR compare" id=off_grid_count_diff></td>
    </tr>
    <tr>
        <td class="summary1">Off-grid cost</td>
        <td class="summary2 alignR" id=off_grid_cost_1>$${formatNumber(float(metricByOptionBySection['system (off-grid)']['system total discounted cost']))}</td>
        <td class="summary3 alignR compare" id=off_grid_cost_2></td>
        <td class="summary4 alignR compare" id=off_grid_cost_diff></td>
    </tr>
    <tr>
        <td class="summary1">Off-grid cost levelized</td>
        <td class="summary2 alignR" id=off_grid_lcoe_1>$${formatFloat(metricByOptionBySection['system (off-grid)']['system total levelized cost'])} / kWh</td>
        <td class="summary3 alignR compare" id=off_grid_lcoe_2></td>
        <td class="summary4 alignR compare" id=off_grid_lcoe_diff></td>
    </tr>
    <tr>
        <td class="summary1">Mini-grid</td>
        <td class="summary2 alignR" id=mini_grid_count_1>${countBySystem.get('mini-grid', 0)}</td>
        <td class="summary3 alignR compare" id=mini_grid_count_2></td>
        <td class="summary4 alignR compare" id=mini_grid_count_diff></td>
    </tr>
    <tr>
        <td class="summary1">Mini-grid cost</td>
        <td class="summary2 alignR" id=mini_grid_cost_1>$${formatNumber(float(metricByOptionBySection['system (mini-grid)']['system total discounted cost']))}</td>
        <td class="summary3 alignR compare" id=mini_grid_cost_2></td>
        <td class="summary4 alignR compare" id=mini_grid_cost_diff></td>
    </tr>
    <tr>
        <td class="summary1">Mini-grid cost levelized</td>
        <td class="summary2 alignR" id=mini_grid_lcoe_1>$${formatFloat(metricByOptionBySection['system (mini-grid)']['system total levelized cost'])} / kWh</td>
        <td class="summary3 alignR compare" id=mini_grid_lcoe_2></td>
        <td class="summary4 alignR compare" id=mini_grid_lcoe_diff></td>
    </tr>
    <tr>
        <td class="summary1">Grid</td>
        <td class="summary2 alignR" id=grid_count_1>${countBySystem.get('grid', 0)}</td>
        <td class="summary3 alignR compare" id=grid_count_2></td>
        <td class="summary4 alignR compare" id=grid_count_diff></td>
    </tr>
    <tr>
        <td class="summary1">Grid cost</td>
        <td class="summary2 alignR" id=grid_cost_1>$${formatNumber(float(metricByOptionBySection['system (grid)']['system total discounted cost']))}</td>
        <td class="summary3 alignR compare" id=grid_cost_2></td>
        <td class="summary4 alignR compare" id=grid_cost_diff></td>
    </tr>
    <tr>
        <td class="summary1">Grid cost levelized</td>
        <td class="summary2 alignR" id=grid_lcoe_1>$${formatFloat(metricByOptionBySection['system (grid)']['system total levelized cost'])} / kWh</td>
        <td class="summary3 alignR compare" id=grid_lcoe_2></td>
        <td class="summary4 alignR compare" id=grid_lcoe_diff></td>
    </tr>
    <tr>
        <td class="summary1">Grid length existing</td>
        <td class="summary2 alignR" id=grid_length_old_1>${formatNumber(networkStatisticByName['old segment weight'])} m</td>
        <td class="summary3 alignR compare" id=grid_length_old_2></td>
        <td class="summary4 alignR compare" id=grid_length_old_diff></td>
    </tr>
    <tr>
        <td class="summary1">Grid length proposed</td>
        <td class="summary2 alignR" id=grid_length_new_1>${formatNumber(networkStatisticByName['new segment weight'])} m</td>
        <td class="summary3 alignR compare" id=grid_length_new_2></td>
        <td class="summary4 alignR compare" id=grid_length_new_diff></td>
    </tr>
    <tr>
        <td class="summary1"></td>
        <td class="summary2 alignR" id=download1><a class=linkOFF href="${h.url('formatted_scenario', id=c.scenario.id, format='zip')}">Download</a></td>
        <td class="summary3 alignR compare" id=download2></td>
        <tdclass="summary4 alignR compare" ></td>
    </tr>
</table>
<br>
<select id=compare class=maximumWidth size=10 title="Select a comparison">
% for scenario in c.scenarios:
    <option value=${scenario.id}>Scenario ${scenario.id} - ${scenario.name}</option>
% endfor
</select>
</div>

<%
from np.lib import variable_store
variableByOptionBySection = c.metricModel.VariableStore(c.nodes[0].output).getVariableByOptionBySection()
%>
<div id=node>
<div id=nodeName></div>
<div id=nodeInput></div>
<div id=nodeOutput>
% for sIndex, section in enumerate(c.metricModel.sections):
<% variableByOption = variableByOptionBySection[section] %>
    <div id="section${sIndex}" class="tabOFF nodeSection">${section.capitalize()}</div>
    <table id="section${sIndex}_" class="tab_ maximumWidth">
    % for option in sorted(variableByOption):
    <% variable = variableByOption[option] %>
        <tr>
            <td><a href="/docs/metric-${c.metricModel.__name__}.html#${variable_store.formatLabel(variable)}" class=linkOFF target=_blank>${option.capitalize()}</a></td>
        % if option.endswith('curve'):
            <td colspan=2><div id="${variable_store.formatKey('metric', variable)}" class=plot></div></td>
        % else:
            <td id="${variable_store.formatKey('metric', variable)}" class="value alignR"></td>
            <td>${variable.units}</td>
        % endif
        </tr>
    % endfor
    </table>
% endfor
</div>
<br>
Click elsewhere on the map to see the scenario overview
</div>
% endif
