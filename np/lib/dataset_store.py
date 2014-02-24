'Routines for manipulating the dataset of nodes and segments'
# Import system modules
import sqlalchemy as sa
from sqlalchemy import orm
import re
import os
import csv
import math
import numpy
import osgeo.ogr
import osgeo.osr
import geojson
import itertools
import collections
import shapely.geometry
# Import custom modules
from np.lib import store, geometry_store
from np.lib import variable_store as VS


def create(targetPath, sourcePath):
    'Import the sourcePath to create the dataset'
    # Initialize
    digestByExtension = {
        '.csv': digestNodesFromCSV,
        '.zip': digestNodesFromZIP,
    }
    # Prepare
    sourceExtension = os.path.splitext(sourcePath)[1].lower()
    if sourceExtension not in digestByExtension:
        raise DatasetError('Only the following formats are currently supported: ' + ' '.join(digestByExtension))
    # Import
    proj4, nodePacks = digestByExtension[sourceExtension](sourcePath)
    # Save
    store.removeSafely(store.replaceFileExtension(targetPath, 'db'))
    dataset = Store(targetPath, proj4)
    dataset.addNodes(nodePacks)
    # Return
    return dataset


def load(datasetPath):
    'Load the given dataset'
    return Store(datasetPath)


class Store(object):
    'Dataset wrapper'

    debug = False

    def __init__(self, datasetPath, proj4=None):
        # Connect
        datasetPath = store.replaceFileExtension(datasetPath, 'db')
        engine = sa.create_engine('sqlite:///' + datasetPath, echo=self.debug)
        metadata.create_all(engine)
        # Set
        self.session = orm.sessionmaker(bind=engine)()
        self.datasetPath = datasetPath
        # Set proj4
        if proj4:
            self.session.execute(spatial_references_table.delete())
            self.session.add(SpatialReference(proj4))
            self.session.commit()
        self.proj4 = str(self.session.query(SpatialReference).first().proj4)
        self.transform_point = geometry_store.get_transform_point(self.proj4)

    def getBasePath(self):
        return os.path.dirname(self.getDatasetPath())

    def getDatasetPath(self):
        return self.datasetPath

    def getProj4(self):
        'Return the default spatial reference for the dataset'
        return self.proj4

    # Node

    def addNode(self, coordinates, nodePack=None, is_fake=False):
        # Compute longitude and latitude
        longitude, latitude = self.transform_point(*coordinates)
        # Add the node
        node = Node(coordinates, (longitude, latitude), nodePack, is_fake)
        self.session.add(node)
        # Return
        return node

    def addNodes(self, nodePacks):
        # Check for duplicates
        nodePacksByCoordinates = collections.defaultdict(list)
        for nodePack in nodePacks:
            coordinates = float(nodePack['x']), float(nodePack['y'])
            nodePacksByCoordinates[coordinates].append(nodePack)
        # For each row,
        for coordinates, nodePacks in nodePacksByCoordinates.iteritems():
            # If there are duplicates,
            if len(nodePacks) > 1:
                print 'Duplicate nodes' 
                for nodePack in nodePacks:
                    print '(%s) %s' % (str(coordinates), nodePack)
            # Add
            self.addNode(coordinates, nodePacks[0])
        # Commit
        self.session.commit()

    def addNodesFromNodeDict(self, nodeDict):
        """
        Add all nodes from a node dict of form:
        {'id': id, {'input': inputNodes, 'output': outputNodes}}
        """
        
        for key in nodeDict.keys():
            node = nodeDict[key]
            inputNodePack = node['input']
            outputNodePack = node['input']
            id = int(key)
            x = float(inputNodePack['x'])
            y = float(inputNodePack['y'])
            newNode = Node((x, y), (x, y), inputNodePack)
            #TODO:  Derive is_fake
            newNode.id = id
            newNode.output = outputNodePack
            self.session.add(newNode)

        self.session.commit()


    def countNodes(self):
        return self.session.query(Node).filter_by(is_fake=False).count()

    def cycleNodes(self, isFake=False):
        'Return nodes in dataset one at a time; set isFake=True to return fake nodes'
        # For each node,
        for node in self.session.query(Node).filter_by(is_fake=isFake).order_by(Node.id):
            # If the node does not have the desired spatial reference,
            yield node

    def getNodeStatistics(self):
        maxLongitude, meanLongitude, minLongitude, maxLatitude, meanLatitude, minLatitude = self.session.query(sa.func.max(Node.longitude), sa.func.avg(Node.longitude), sa.func.min(Node.longitude), sa.func.max(Node.latitude), sa.func.avg(Node.latitude), sa.func.min(Node.latitude)).first()
        return {
            'node count': self.session.query(Node).filter_by(is_fake=False).count(),
            'maximum longitude': maxLongitude,
            'mean longitude': meanLongitude,
            'minimum longitude': minLongitude,
            'maximum latitude': maxLatitude,
            'mean latitude': meanLatitude,
            'minimum latitude': minLatitude,
        }

    def saveNodesSHP(self, targetPath, isFake=False):
        'Save nodes to a shapefile'
        geometry_store.save(store.replaceFileExtension(targetPath, 'shp'), self.getProj4(), [shapely.geometry.asShape(node) for node in self.cycleNodes(isFake)])

    def saveNodesCSV(self, targetPath, isFake=False):
        'Save nodes to a csv'
        # Initialize
        node = self.cycleNodes(isFake).next()
        csvWriter = csv.writer(open(store.replaceFileExtension(targetPath, 'csv'), 'wb'))
        # Write spatial reference
        csvWriter.writerow(['PROJ.4 ' + self.getProj4()])
        # Write column headers
        customHeaders = sorted(set(node.input) - set(['name', 'x', 'y']))
        csvWriter.writerow(['Name', 'X', 'Y'] + [x.capitalize() for x in customHeaders])
        # For each node,
        for node in self.cycleNodes(isFake):
            # Write row
            csvWriter.writerow([node.input.get('name', ''), node.getX(), node.getY()] + [node.input.get(x, '') for x in customHeaders])

    # Metric
    def applyMetric(self, metricModel, metricValueByOptionBySection):
        'Compute a metric for each node'
        # Load job-level configuration
        jobVS = metricModel.VariableStore(metricValueByOptionBySection)
        # For each real node,
        for node in self.session.query(Node).filter_by(is_fake=False):
            # Load node-level configuration
            nodeVS = metricModel.VariableStore(node.getValueByOptionBySection(), jobVS)
            # Save results
            node.metric = nodeVS.get(metricModel.Metric)
            node.output = nodeVS.getValueByOptionBySection()
        # Commit
        self.session.commit()
        # Return outputs
        return jobVS.getValueByOptionBySection()

    def getMetricStatistics(self):
        'Compute metric statistics'
        # Prepare metrics
        metrics = [x[0] for x in self.session.query(Node.metric).filter_by(is_fake=False)]
        # Aggregate
        populations = []
        countBySystem = collections.defaultdict(int)
        for node in self.cycleNodes():
            nodeOutput = node.output
            countBySystem[nodeOutput['metric']['system']] += 1
            populations.append(int(nodeOutput['demographics']['population count']))
        # Process
        populations1, populations2 = store.splitList(populations, 2)
        # Return
        return {
            'minimum metric': min(metrics),
            'maximum metric': max(metrics),
            'mean metric': numpy.mean(metrics),
            'count by system': countBySystem,
            'population quartiles': [numpy.median(populations1), numpy.median(populations), numpy.median(populations2)],
        }

    def saveMetricsCSV(self, targetPath, metricModel, headerType=VS.HEADER_TYPE_SECTION_OPTION):
        'Save node-level metrics in CSV format'
        # Make sure that nodes exist
        if not self.countNodes():
            return

        # Prepare column headers in order
        # Use the 1st node's input to get the "pass-through" fields 
        node = self.cycleNodes().next()
        nodeInput = node.input
        headerPacks = [('', key) for key in sorted(nodeInput)]

        # get the section/option values in order from the model
        # and append to the headerPacks
        # Note:  metricModel.VariableStore.variableClasses should have all the
        #        the variableClasses associated with the model as long as 
        #        metricModel.VariableStore() has been called.
        baseVars = metricModel.VariableStore.variableClasses
        baseVarHeaders = [(var.section, var.option) for var in 
                          sorted(baseVars, key=lambda v: (v.section, v.option))]
        headerPacks.extend(baseVarHeaders)
        headerPacksToNames = VS.getFieldNamesForHeaderPacks(metricModel, 
                                headerPacks, headerType)
       
        csvWriter = csv.writer(open(store.replaceFileExtension(targetPath, 'csv'), 'wb'))
        csvWriter.writerow(['PROJ.4 ' + self.getProj4()])

        csvWriter.writerow([headerPacksToNames[(section, option)] for 
                            section, option in headerPacks])
    
        # csvWriter.writerow(['%s > %s' % (section.capitalize(), option.capitalize()) if section else option.capitalize() for section, option in headerPacks])
        # For each node,
        for node in self.cycleNodes():
            # Write row
            csvWriter.writerow([node.output.get(section, {}).get(option, '') if section else node.input.get(option, '') for section, option in headerPacks])

    # Network
    def buildNetwork(self, networkModel, networkValueByOptionBySection, jobLogger=None):
        'Build a network using the nodes and network building algorithm'
        # Load job-level configuration
        # NOTE:  state[0] is the current dataset_store which is used in the network
        #        model to retrieve the basePath of the archive.
        #        This seems like an anti-pattern, coupling the dataset_store to the 
        #        network model in a non-transparent way. 
        jobVS = networkModel.VariableStore(networkValueByOptionBySection, state=[self])
        # Build network
        net = jobVS.buildNetworkFromNodes(list(self.cycleNodes()), self.getProj4(), jobLogger=jobLogger)
        # For each subnet in the generated network,
        for networkSubnet in net.cycleSubnets():
            # Create the subnet in our dataset
            datasetSubnet = Subnet()
            self.session.add(datasetSubnet)
            self.session.commit()
            # For each segment in the subnetwork,
            for networkSegment in networkSubnet.cycleSegments():
                # Save fake nodes if we have any
                for networkNode in (x for x in networkSegment.getNodes() if x.getID() < 0):
                    # Create the fake node in our dataset
                    datasetNode = self.addNode(networkNode.getCoordinates(), is_fake=True)
                    self.session.add(datasetNode)
                    self.session.commit()
                    # Store the id
                    networkNode.setID(datasetNode.id)
                # Add segment
                segment = Segment(*networkSegment.getSortedNodeIDs())
                segment.subnet_id = datasetSubnet.id
                segment.is_existing = networkSegment.is_existing
                segment.weight = networkSegment.getWeight()
                self.session.add(segment)
        # Commit
        self.session.commit()
        # Return outputs
        return jobVS.getValueByOptionBySection()

    # Segment

    def getSegmentQuery(self, is_existing=None):
        'Return SQLAlchemy query'
        # Initialize
        segmentQuery = self.session.query(Segment)
        # If the user wants to filter existing segments,
        if is_existing != None:
            # Do it
            segmentQuery = segmentQuery.filter(Segment.is_existing==is_existing)
        # Return
        return segmentQuery

    def countSegments(self, is_existing=None):
        'Count segments'
        return self.getSegmentQuery(is_existing).count()

    def cycleSegments(self, is_existing=None):
        'Generate segments'
        for segment in self.getSegmentQuery(is_existing):
            yield segment

    def countSubnets(self):
        return self.session.query(Subnet).count()

    def cycleSubnets(self):
        for subnet in self.session.query(Subnet):
            yield subnet

    def cycleConnections(self, node, is_existing=None):
        'Cycle through segments connected to the node'
        for connection in self.getSegmentQuery(is_existing).filter((Segment.node1_id==node.id) | (Segment.node2_id==node.id)):
            yield connection

    def isNodeConnected(self, node):
        return True if self.session.query(Segment).filter((Segment.node1_id==node.id) | (Segment.node2_id==node.id)).first() else False

    def wasNodeAlreadyConnected(self, node):
        return True if self.session.query(Segment).filter(Segment.is_existing==True).filter((Segment.node1_id==node.id) | (Segment.node2_id==node.id)).first() else False

    def sumNetworkWeight(self, is_existing=None):
        'Get the weight of the network, where weight corresponds to length in most cases'
        # Initialize query
        query = self.session.query(sa.func.sum(Segment.weight))
        # If the user wants to filter existing segments,
        if is_existing != None:
            value = query.filter(Segment.is_existing==is_existing).first()[0]
        # If the user wants the weight of the entire network,
        else:
            value = query.first()[0]
        # Return
        return value if value else 0

    def getNetworkStatistics(self):
        return {
            'segment count': self.session.query(Segment).count(),
            'new segment weight': self.sumNetworkWeight(is_existing=False),
            'old segment weight':  self.sumNetworkWeight(is_existing=True),
        }

    def saveSegmentsSHP(self, targetPath, is_existing=None):
        # If there are no segments,
        if not self.countSegments(is_existing):
            return
        # Save
        return geometry_store.save(store.replaceFileExtension(targetPath, 'shp'), self.getProj4(), [shapely.geometry.asShape(x) for x in self.cycleSegments(is_existing)])

    def saveSubnetsSHP(self, targetPath):
        'Save subnets to a shapefile'
        # If there are no subnets,
        if not self.countSubnets():
            return
        # Save
        geometry_store.save(store.replaceFileExtension(targetPath, 'shp'), self.getProj4(), [shapely.geometry.asShape(x) for x in self.cycleSubnets()])

    # Output

    def updateMetric(self, metricModel, metricValueByOptionBySection):
        'Add outputs that can only be determined after we have both the metric and network'
        # Load job-level configuration
        jobVS = metricModel.VariableStore(metricValueByOptionBySection, state=[self])
        jobVS.initializeAggregates()
        # For each real node,
        for node in self.session.query(Node).filter_by(is_fake=False):
            # Restore node-level configuration
            nodeVS = metricModel.VariableStore(node.output, state=[self, node])
            # Compute more
            nodeVS.get(metricModel.System)
            jobVS.updateAggregates(nodeVS)
            # Set output
            node.output = nodeVS.getValueByOptionBySection()
        # Compute summary variables
        jobVS.processAggregates()
        # Commit
        self.session.commit()
        # Return
        return jobVS.getValueByOptionBySection()
    
    def exportGeoJSON(self, transform_point=None):
        # Initialize features as a list
        features = []
        # For each node,
        for node in self.cycleNodes():
            # Load node
            nodeOutput = node.output
            # Append a geojson feature using the node's id and other desired properties
            features.append(geojson.Feature(
                id='n%s' % node.id, 
                geometry=node.exportGeoJSONGeometry(transform_point), 
                properties={
                    'population': nodeOutput['demographics']['population count'],
                    'system': nodeOutput['metric']['system'],
                },
            ))
        # For each segment,
        for segment in self.cycleSegments():
            # Append a geojson feature using the segment's id and other desired properties
            features.append(geojson.Feature(
                id='s%s-%s' % (segment.node1_id, segment.node2_id), 
                geometry=segment.exportGeoJSONGeometry(transform_point),
                properties={
                    'subnet_id': segment.subnet_id,
                    'is_existing': 1 if segment.is_existing else 0,
                    'weight': int(math.ceil(segment.weight)),
                },
            ))
        # Return
        return geojson.dumps(geojson.FeatureCollection(features))


# Digest
def digestNodesFromCSV(sourcePath):
    'Import nodes from a comma separated values file'
    csvStream = open(sourcePath, 'rU')
    proj4, nodePacks = digestNodesFromCSVStream(csvStream)
    csvStream.close()
    return proj4, nodePacks


def digestNodesFromCSVStream(sourceStream):
    'Import nodes from a comma separated values stream'
    # Initialize
    rowGenerator = csv.reader(sourceStream)
    try:
        row = rowGenerator.next()
    except StopIteration:
        raise DatasetError('The CSV file is empty')
    # Prepare spatial reference
    match = re.match('PROJ.4 (.*)', row[0], re.IGNORECASE)
    if match:
        proj4 = match.group(1).strip()
        row = rowGenerator.next()
    else:
        proj4 = geometry_store.proj4LL
    # Prepare labels
    labels = []
    for label in row:
        # We allow for case-insensitive matches to field names by lower-casing the 
        # field name and comparing to the existing alias or option/section (which are
        # all lower-case)
        label = label.lower() 
        if label == 'longitude':
            label = 'x'
        elif label == 'latitude':
            label = 'y'
        labels.append(label)
    # Check whether we do in fact have labels
    if not set(labels).intersection(['name', 'x', 'y']):
        raise DatasetError('Expected spatial reference or labels but found this instead: %s' % labels)
    # Prepare nodePacks
    nodePacks = [dict(itertools.izip(labels, values)) for values in rowGenerator]
    ignoreNodesWithMissingCoordinates = lambda x: x['x'] != '' and x['y'] != ''
    # Return
    return proj4, filter(ignoreNodesWithMissingCoordinates, nodePacks)

def digestNodesFromSHP(sourcePath):
    'Import nodes from a shapefile'
    # Initialize
    shapeData = osgeo.ogr.Open(sourcePath)
    layer = shapeData.GetLayer()
    # Prepare spatial reference
    proj4 = layer.GetSpatialRef().ExportToProj4()
    # Prepare nodePacks
    nodePacks = []
    for featureIndex in xrange(layer.GetFeatureCount()):
        # Get feature
        feature = layer.GetFeature(featureIndex)
        geometry = feature.GetGeometryRef()
        # Build nodePack
        valueByLabel = feature.items()
        nodePack = dict((label.lower(), value) for label, value in valueByLabel.iteritems() if value not in ['', None])
        nodePack['x'] = geometry.GetX()
        nodePack['y'] = geometry.GetY()
        # Append
        nodePacks.append(nodePack)
    # Return
    return proj4, nodePacks

def digestNodesFromZIP(sourcePath):
    # Shape
    hasShapeFile, shapePath = store.unzip(sourcePath, '.shp')
    if not hasShapeFile:
        raise DatasetError('Archive does not contain a shapefile')
    # Digest
    return digestNodesFromSHP(shapePath)


# Define tables

metadata = sa.MetaData()

spatial_references_table = sa.Table('spatial_references', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('proj4', sa.String, unique=True),
)

nodes_table = sa.Table('nodes', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('x', sa.Float),
    sa.Column('y', sa.Float),
    sa.Column('longitude', sa.Float),
    sa.Column('latitude', sa.Float),
    sa.Column('metric', sa.Float),
    sa.Column('is_fake', sa.Boolean, default=False),
    # We can use mutable=False because we always assign new objects to these variables
    sa.Column('input', sa.types.PickleType(mutable=False)),
    sa.Column('output', sa.types.PickleType(mutable=False)),
)

segments_table = sa.Table('segments', metadata,
    sa.Column('node1_id', sa.ForeignKey('nodes.id'), primary_key=True),
    sa.Column('node2_id', sa.ForeignKey('nodes.id'), primary_key=True),
    sa.Column('subnet_id', sa.ForeignKey('subnets.id')),
    sa.Column('is_existing', sa.Boolean, default=False),
    sa.Column('weight', sa.Float),
)

subnets_table = sa.Table('subnets', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
)


class SpatialReference(object):

    def __init__(self, proj4):
        self.proj4 = proj4

    def __repr__(self):
        return '<SpatialReference(%s)>' % self.proj4


class Node(object):

    def __init__(self, (x, y), (longitude, latitude), nodePack, is_fake=False):
        # Set
        self.x, self.y = x, y
        self.longitude, self.latitude = longitude, latitude
        if nodePack:
            self.input = nodePack
        self.is_fake = is_fake

    # Coordinates

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getCoordinates(self):
        return self.getX(), self.getY()

    def getCommonCoordinates(self):
        return self.longitude, self.latitude

    def getValueByOptionBySection(self):
        # Initialize
        valueByOptionBySection = collections.defaultdict(dict)
        # Prepare pattern to detect node-level overrides
        pattern = re.compile(r'(.*?)\s*>\s*(.*)')
        # For each attribute,
        for name, value in self.input.iteritems():
            # Check whether the attribute is a node-level override
            match = pattern.match(name)
            # If the attribute is a node-level override,
            if match:
                # Get section and option
                section, option = match.groups()
                # Store it
                valueByOptionBySection[section][option] = value
            else:
                # Store it in case it is an alias
                valueByOptionBySection[name] = value
        # Return
        return valueByOptionBySection

    @property
    def __geo_interface__(self):
        return {'type': 'Point', 'coordinates': self.getCoordinates()}

    def exportGeoJSONGeometry(self, transform_point=None):
        coordinates = self.getCommonCoordinates()
        if transform_point:
            coordinates = transform_point(*coordinates)
        return geojson.Point(coordinates)

    # Display

    def __repr__(self):
        return '<Node(longitude=%s, latitude=%s)>' % (self.longitude, self.latitude)

    def exportJSON(self):
        pass


class Segment(object):

    def __init__(self, node1_id, node2_id):
        self.node1_id = node1_id
        self.node2_id = node2_id

    def __repr__(self):
        return '<Segment(%s-%s)>' % (self.node1_id, self.node2_id)

    def __hash__(self):
        return hash(self.getCoordinates())

    def __eq__(self, other):
        return self.getCoordinates() == other.getCoordinates()

    def __ne__(self, other):
        return not self.__eq__(other)

    def getCoordinates(self):
        return self.node1.getCoordinates(), self.node2.getCoordinates()

    def getCommonCoordinates(self):
        return self.node1.getCommonCoordinates(), self.node2.getCommonCoordinates()

    @property
    def __geo_interface__(self):
        return {'type': 'LineString', 'coordinates': self.getCoordinates()}

    def exportGeoJSONGeometry(self, transform_point=None):
        coordinates = self.getCommonCoordinates()
        if transform_point:
            coordinates = [transform_point(*x) for x in coordinates]
        return geojson.LineString(coordinates)


class Subnet(object):

    def getCoordinates(self):
        return [x.getCoordinates() for x in self.segments]

    def getCommonCoordinates(self):
        return [x.getCommonCoordinates() for x in self.segments]

    @property
    def __geo_interface__(self):
        return {'type': 'MultiLineString', 'coordinates': self.getCoordinates()}

    def exportGeoJSONGeometry(self, transform_point=None):
        coordinates = self.getCommonCoordinates()
        if transform_point:
            coordinates = [(transform_point(*x[0]), transform_point(*x[1])) for x in coordinates]
        return geojson.MultiLineString(coordinates)


# Map tables to classes

orm.mapper(SpatialReference, spatial_references_table)
orm.mapper(Node, nodes_table, properties={
    'input': orm.deferred(nodes_table.c.input, group='pickled'),
    'output': orm.deferred(nodes_table.c.output, group='pickled'),
})
orm.mapper(Segment, segments_table, properties={
    'node1': orm.relation(Node, primaryjoin=segments_table.c.node1_id==nodes_table.c.id, lazy=False),
    'node2': orm.relation(Node, primaryjoin=segments_table.c.node2_id==nodes_table.c.id, lazy=False),
})
orm.mapper(Subnet, subnets_table, properties={
    'segments': orm.relation(Segment, backref='subnet', lazy=False),
})


# Error

class DatasetError(Exception):
    pass
