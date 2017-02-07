#!/usr/bin/env python
""" this is test python """
from osgeo import ogr
from osgeo import gdal
from osgeo import osr
import os
import sys
import shutil
srcName = "./testdata/NYC_MUSEUMS_LAMBERT.shp"
tgtName = "./testdata/DST_Prj.shp"
tgt_spatRef = osr.SpatialReference()
tgt_spatRef.ImportFromEPSG(4326)
driver = gdal.GetDriverByName("ESRI Shapefile")
if driver is None:
    print("%s driver not available.\n" % driverName)
    sys.exit(1)

src = gdal.Open()
srcLyr = src.GetLayer
src_spatRef = srcLyr.GetSpatialRef()
if os.path.exists(tgtName):
    driver.DeleteDataSource(tgtName)
tgt = driver.CreateDataSource(tgtName)
lyrName = os.path.splitext(tgtName)[0]
# Use well-known binary format (WKB) to specify geometry
tgtLyr = tgt.CreateLayer(lyrName, geom_type=ogr.wkbPoint)
featDef = srcLyr.GetLayerDefn()
trans = osr.CoordinateTransformation(src_spatRef, tgt_spatRef)
srcFeat = srcLyr.GetNextFeature()
while srcFeat:
    geom = srcFeat.GetGeometryRef()
    geom.Transform(trans)
    feature = ogr.Feature(featDef)
    feature.SetGeometry(geom)
    tgtLyr.CreateFeature(feature)
    feature.Destroy()
    srcFeat.Destroy()
    srcFeat = srcLyr.GetNextFeature()
src.Destroy()
tgt.Destroy()
# Convert geometry to Esri flavor of Well-Known Text (WKT) format
# for export to the projection (prj) file.
tgt_spatRef.MorphToESRI()
prj = open(lyrName + ".prj", "w")
prj.write(tgt_spatRef.ExportToWkt())
prj.close()
srcDbf = os.path.splitext(srcName)[0] + ".dbf"
tgtDbf = lyrName + ".dbf"
shutil.copyfile(srcDbf, tgtDbf)
