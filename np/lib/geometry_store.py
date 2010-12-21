'GDAL wrapper for reading and writing geospatial data'
# Import system modules
import os
import itertools
from shapely import wkb, geometry
from osgeo import ogr, osr


# Set constants
driverPacks = [
    ('ESRI Shapefile', '.shp'),
    ('KML', '.kml'),
]
driverNameDefault = driverPacks[0][0]
proj4Default = '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'
proj4Google = '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs'


# Define shortcuts

def savePoints(targetPath, proj4, coordinateTuples, fieldPacks=None, fieldDefinitions=None, driverName=driverNameDefault):
    return save(targetPath, proj4, [geometry.Point(x) for x in coordinateTuples], fieldPacks, fieldDefinitions, driverName)

def loadPoints(targetPath, driverName=driverNameDefault):
    proj4, shapelyGeometries, fieldPacks, fieldDefinitions = load(targetPath, driverName)
    return proj4, [(point.x, point.y) for point in shapelyGeometries], fieldPacks, fieldDefinitions


# Define core

def save(targetPath, proj4, shapelyGeometries, fieldPacks=None, fieldDefinitions=None, driverName=driverNameDefault):
    'Save shapelyGeometries using the given proj4 and fields'
    # Validate arguments
    if not fieldPacks:
        fieldPacks = []
    if not fieldDefinitions:
        fieldDefinitions = []
    if fieldPacks and set(len(x) for x in fieldPacks) != set([len(fieldDefinitions)]):
        raise GeometryError('A field definition is required for each field')
    # Create dataSource
    targetBasePath = os.path.splitext(targetPath)[0]
    targetPath = targetBasePath + dict(driverPacks)[driverName]
    if os.path.exists(targetPath): 
        os.remove(targetPath)
    dataSource = ogr.GetDriverByName(driverName).CreateDataSource(targetPath)
    # Create layer
    srs = osr.SpatialReference()
    srs.ImportFromProj4(proj4)
    layer = dataSource.CreateLayer(os.path.basename(targetBasePath), srs)
    # Create fields
    for fieldName, fieldType in fieldDefinitions:
        layer.CreateField(ogr.FieldDefn(fieldName, fieldType))
    featureDefinition = layer.GetLayerDefn()
    # For each geometry,
    for shapelyGeometry, fieldPack in itertools.izip(shapelyGeometries, fieldPacks) if fieldPacks else ((x, []) for x in shapelyGeometries):
        # Create feature
        feature = ogr.Feature(featureDefinition)
        feature.SetGeometry(ogr.CreateGeometryFromWkb(shapelyGeometry.wkb))
        for fieldIndex, fieldValue in enumerate(fieldPack):
            feature.SetField(fieldIndex, fieldValue)
        # Save feature
        layer.CreateFeature(feature)
        feature.Destroy()
    # Return
    return targetPath

def load(sourcePath, driverName=driverNameDefault):
    'Load proj4, shapelyGeometries, fields'
    # Initialize
    shapelyGeometries, fieldPacks, fieldDefinitions = [], [], []
    # Load 
    dataSource = ogr.Open(os.path.splitext(sourcePath)[0] + dict(driverPacks)[driverName])
    layer = dataSource.GetLayer()
    featureDefinition = layer.GetLayerDefn()
    fieldIndices = xrange(featureDefinition.GetFieldCount())
    for fieldIndex in fieldIndices:
        fieldDefinition = featureDefinition.GetFieldDefn(fieldIndex)
        fieldDefinitions.append((fieldDefinition.GetName(), fieldDefinition.GetType()))
    feature = layer.GetNextFeature()
    # While there are more features,
    while feature:
        # Append
        shapelyGeometries.append(wkb.loads(feature.GetGeometryRef().ExportToWkb()))
        fieldPacks.append([feature.GetField(x) for x in fieldIndices])
        # Get the next feature
        feature = layer.GetNextFeature()
    # Return
    return layer.GetSpatialRef().ExportToProj4(), shapelyGeometries, fieldPacks, fieldDefinitions

def getTransformPoint(sourceProj4, targetProj4=proj4Default):
    'Return a function that transforms coordinates from one spatial reference to another'
    if sourceProj4 == targetProj4:
        return lambda x, y: (x, y)
    sourceSRS = osr.SpatialReference()
    sourceSRS.ImportFromProj4(sourceProj4)
    targetSRS = osr.SpatialReference()
    targetSRS.ImportFromProj4(targetProj4)
    return lambda x, y: osr.CoordinateTransformation(sourceSRS, targetSRS).TransformPoint(x, y)[:2]


# Define errors

class GeometryError(Exception):
    pass
