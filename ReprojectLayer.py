#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-13 09:35:43
# @Author  : mjj (jinunmeng@163.com)
# @Link    : https://github.com/Jiunmeng
# @Version : $Id$
from osgeo import osr
from osgeo import ogr
import os
driver = ogr.GetDriverByName("ESRI Shapefile")
inSpatialRef = osr.SpatialReference()
inSpatialRef.ImportFromEPSG(4326)

outSpatialRef = osr.SpatialReference()
outSpatialRef.ImportFromEPSG(2927)
# 创建坐标转换关系
coordTrans = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)
# 获取输入的数据
inDataset = driver.Open(r"D:/Python36/testdata/hancock.shp")
inLayer = inDataset.GetLayer()
# 创建输出的数据
outputShp = r"D:/Python36/testdata/hancock_2927.shp"
if os.path.exists(outputShp):
    driver.DeleteDataSource(outputShp)
outDataset = driver.CreateDataSource(outputShp)
outLayer = outDataset.CreateLayer(
    "hancock_2927", geom_type=ogr.wkbMultiPolygon)
# add fields
inLayerDefn = inLayer.GetLayerDefn()
for i in range(0, inLayerDefn.GetFieldCount()):
    fieldDefn = inLayerDefn.GetFieldDefn(i)
    outLayer.CreateField(fieldDefn)

outLayerDefn = outLayer.GetLayerDefn()

inFeature = inLayer.GetNextFeature()
while inFeature:
    geom = inFeature.GetGeometryRef()
    geom.Transform(coordTrans)
    # Create a new Feature
    outFeature = ogr.Feature(outLayerDefn)
    # set the geometry and attribute
    outFeature.SetGeometry(geom)
    for i in range(0, outLayerDefn.GetFieldCount()):
        outFeature.SetField(
            outLayerDefn.GetFieldDefn(i).GetNameRef(), inFeature.GetField(i))
    outLayer.CreateFeature(outFeature)
    outFeature = None
    inFeature = inLayer.GetNextFeature()
inDataset = None
outDataset = None
