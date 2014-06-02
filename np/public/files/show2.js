(function($){


Map = {};
Map.init = function(geojson){
    var self = this;

    // Initialize map
    self.map = L.map('map', {zoomAnimation: false, inertia: false})
        .setView([40.809400, -73.960029], 16);

    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(self.map);

    // Load GeoJSON
    var nodes = [];
    var lines = [];
    geojson.features.forEach(function(feature){
        var geometry = feature.geometry;
        if (geometry.type === 'LineString'){
            lines.push(feature);
        } else if (geometry.type === 'Point'){
            var node = {
                id: feature.id,
                lat: geometry.coordinates[1],
                lon: geometry.coordinates[0]
            };
            $.each(feature.properties, function(key, val){
                node[key] = val;
            });
            nodes.push(node);
        }
    });

    // Draw network
    self.map.fitBounds(nodes, {padding: [5, 5]});
    self.initD3Layer();
    self.drawLines(lines);
    self.drawNodes(nodes);
    
    // Box node selection
    // Cheap hack to disable zoom
    // http://stackoverflow.com/questions/17611596/multiple-marker-selection-within-a-box-in-leaflet
    self.map._fitBounds = map.fitBounds;
    self.map.fitBounds = function(){return self.map;};
    self.map.on('boxzoomend', function(e){
        $('.node').each(function(){
            var node = d3.select(this).data()[0];
            if (e.boxZoomBounds.contains(L.latLng(node.lat, node.lon))){
                if (this.classList.contains('selected')){
                    this.classList.remove('selected');
                } else {
                    this.classList.add('selected');
                }
            }
            Map.updateSelected();
        });
    });

    // Event Handlers
    $(document.body).on('click', '.node', function(){
        if (this.classList.contains('selected')){
            this.classList.remove('selected');
        } else {
            this.classList.add('selected');
        }
        Map.updateSelected();
        console.log(d3.select(this).data()[0])
    });

    $('#controls_selected').click(self.selectedModal);
};


Map.initD3Layer = function(){
    var self = this;
    var center = self.map.getCenter();
    var size = self.map.getSize();
    var overlay = self.map.getPanes().overlayPane;
    var bounds = self.map.getBounds()
    self.dLat = bounds.getNorth() - bounds.getSouth();
    self.initialScale = (1 << 8 + self.map.getZoom()) / 2 / Math.PI;
    self.projection = d3.geo.mercator()
        .center([center.lng, center.lat])
        .scale(self.initialScale)
        .translate([size.x/2, size.y/2]);
    self.path = d3.geo.path().projection(self.projection);
    self.svg = d3.select(overlay)
        .append('svg')
        .attr('width', size.x)
        .attr('height', size.y);
    self.g = self.svg.append('g');

    self.updateSVG = function(){
        var size = self.map.getSize();
        var bounds = self.map.getBounds();
        var dLat = bounds.getNorth() - bounds.getSouth();
        var scale = Math.round(self.dLat / dLat * 10) / 10;
        var offset = self.map.containerPointToLayerPoint([0, 0]);
        var centerLatLon = self.map.getCenter()
        var center = self.projection([centerLatLon.lng, centerLatLon.lat]);

        // Reverse leaflet CSS transform of SVG pane
        L.DomUtil.setPosition(self.svg.node(), offset);

        // Apply SVG transform on G element instead
        var gx = -center[0] * scale + (size.x / 2);
        var gy = -center[1] * scale + (size.y / 2);
        self.g.attr('transform', 'translate(' + gx + ',' + gy + ')scale(' + scale + ',' + scale + ')');
    }

    self.map.on('viewreset', self.updateSVG);
    self.map.on('moveend', self.updateSVG);
};

Map.drawLines = function(lines){
    var self = this;
    lines.forEach(function(feature){
        self.g
            .append('path')
            .datum(feature)
            .attr('d', self.path)
            .attr('class', 'edge');
    });
};

Map.drawNodes = function(nodes){
    var self = this;
    self.totNodes += nodes.length;
    nodes.forEach(function(node){
        var coordinates = self.projection([node.lon, node.lat]);
        self.g.append('svg:circle')
            .datum(node)
            .attr('cx', coordinates[0])
            .attr('cy', coordinates[1])
            .attr('r', 5)
            .attr('class', 'node');
    });
    self.updateSVG();
};

Map.updateSelected = function(){
    var selected = $('#map .node.selected').length;
    if (selected){
        $('#controls_selected').text(selected + ' Nodes Selected').show();
    } else {
        $('#controls_selected').hide();
    }
};

Map.escape = function(text){
    text = text || '';
    return text.replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
};

Map.selectedModal = function(){
    var selected = [];
    $('#map .node.selected').each(function(){
        var node = d3.select(this).data()[0];
        selected.push(node);
    });

    if (selected.length === 0) return;

    var node = selected[0];
    var headers = Object.keys(node);
    var html = '<table><thead><tr>';
    headers.forEach(function(header){
        html += '<th>' + this.escape(header) + '</th>';
    });
    html += '</tr></thead><tbody>';
    selected.forEach(function(node){
        html += '<tr>';
        headers.forEach(function(header){
            html += '<td>' + this.escape(node[header]) + '</td>';
        });
        html += '</tr>';
    });
    html += '</tbody></table>';

    $('#modal').html(html).show();
};

})(jQuery);



