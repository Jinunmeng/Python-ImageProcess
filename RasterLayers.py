#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-13 11:31:12
# @Author  : mjj (jinunmeng@163.com)
# @Link    : https://github.com/Jiunmeng
# @Version : $Id$
from osgeo import gdal
from osgeo import ogr
import sys
# Open Dataset
ds = gdal.Open(r"D:/Python36/testdata/clip.tif")
if ds is None:
    print("Unable to open the file")
    sys.exit(1)
# 获取波段个数
print(ds.RasterCount)

for band in range(ds.RasterCount):
    band += 1
    print("Getting:", band)
    srcBand = ds.GetRasterBand(band)
    if srcBand is None:
        continue
    stats = srcBand.GetStatistics(True, True)
    if stats is None:
        continue
    print("[ STATS ] =  Minimum=%.3f, Maximum=%.3f, Mean=%.3f, StdDev=%.3f" % (
        stats[0], stats[1], stats[2], stats[3]))


# 矢量化栅格数据
srcBd = ds.GetRasterBand(1)
dst_layerName = "Polygonize_Clip"
driver = ogr.GetDriverByName("ESRI Shapefile")
dst_ds = driver.CreateDataSource(
    r"D:/Python36/testdata/Polygonize_Clip" + ".shp")
dst_layer = dst_ds.CreateLayer(dst_layerName, srs=None)
gdal.Polygonize(srcBand, None, dst_layer, -1, [], callback=None)

# Close Dataset
ds = None
