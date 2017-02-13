#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-13 09:11:58
# @Author  : mjj (jinunmeng@163.com)
# @Link    : https://github.com/Jiunmeng
# @Version : $Id$
from osgeo import osr
from osgeo import ogr

# 创建投影坐标系
spatialRef = osr.SpatialReference()
spatialRef.ImportFromEPSG(4326)


# 几何重投影
source = osr.SpatialReference()
source.ImportFromEPSG(2927)
target = osr.SpatialReference()
target.ImportFromEPSG(4326)
transform = osr.CoordinateTransformation(source, target)
print(target.ExportToPrettyWkt())

point = ogr.CreateGeometryFromWkt("POINT (1120351.57 741921.42)")
point.Transform(transform)
print(point.ExportToWkt())

# 获取投影信息
driver = ogr.GetDriverByName("ESRI Shapefile")
dataset = driver.Open(r"D:/Python36/testdata/hancock.shp")
# 1、from layer
layer = dataset.GetLayer()
spatialRefLy = layer.GetSpatialRef()
print(spatialRefLy.ExportToPrettyWkt())

# 2、from geometry
feature = layer.GetNextFeature()
geom = feature.GetGeometryRef()
spatialRefGeo = geom.GetSpatialReference()
print(spatialRefGeo.ExportToPrettyWkt())


# Create an ESRI.prj file
spatialRefESRI = osr.SpatialReference()
spatialRefESRI.ImportFromEPSG(26912)
spatialRef.MorphFromESRI()
file = open(r"D:/Python36/testdata/myShapefile.prj", 'w')
file.write(spatialRef.ExportToPrettyWkt())
file.close()
