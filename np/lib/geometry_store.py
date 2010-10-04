# Import system modules
import os
import osgeo.ogr
import osgeo.osr
import shapely.wkb
# Import custom modules
import store


# Set
extensionByName = {'ESRI Shapefile': 'shp'}
proj4Default = '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'
proj4Google = '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs'


def save(targetPath, shapelyGeometries, proj4, driverName='ESRI Shapefile'):
    'Save shapelyGeometries'
    # Get driver
    driver = osgeo.ogr.GetDriverByName(driverName)
    # Create data
    targetPath = store.replaceFileExtension(targetPath, extensionByName[driverName])
    if os.path.exists(targetPath): 
        os.remove(targetPath)
    dataSource = driver.CreateDataSource(targetPath)
    # Create spatialReference
    spatialReference = osgeo.osr.SpatialReference()
    spatialReference.ImportFromProj4(proj4)
    # Create layer
    layerName = store.extractFileBaseName(targetPath)
    layer = dataSource.CreateLayer(layerName, spatialReference)
    layerDefinition = layer.GetLayerDefn()
    # For each geometry,
    for shapelyGeometry in shapelyGeometries:
        # Create feature
        feature = osgeo.ogr.Feature(layerDefinition)
        feature.SetGeometry(osgeo.ogr.CreateGeometryFromWkb(shapelyGeometry.wkb))
        # Save feature
        layer.CreateFeature(feature)
    # Return
    return targetPath


def load(sourcePath, driverName='ESRI Shapefile'):
    'Load shapelyGeometries'
    # Prepare the return set
    shapelyGeometries = []
    # Open
    sourcePath = store.replaceFileExtension(sourcePath, extensionByName[driverName])
    dataSource = osgeo.ogr.Open(sourcePath)
    # Get the first layer
    layer = dataSource.GetLayer()
    # Get the first feature
    feature = layer.GetNextFeature()
    # While there are more features,
    while feature:
        # Append 
        shapelyGeometries.append(shapely.wkb.loads(feature.GetGeometryRef().ExportToWkb()))
        # Get the next feature
        feature = layer.GetNextFeature()
    # Return
    return shapelyGeometries, layer.GetSpatialRef().ExportToProj4()


def getTransformPoint(sourceProj4, targetProj4=proj4Default):
    'Return a function that transforms coordinates from one spatial reference to another'
    if sourceProj4 == targetProj4:
        return lambda x, y: (x, y)
    sourceSRS = osgeo.osr.SpatialReference()
    sourceSRS.ImportFromProj4(sourceProj4)
    targetSRS = osgeo.osr.SpatialReference()
    targetSRS.ImportFromProj4(targetProj4)
    return lambda x, y: osgeo.osr.CoordinateTransformation(sourceSRS, targetSRS).TransformPoint(x, y)[:2]
