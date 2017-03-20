# -*- coding:utf-8 -*-
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
import os
import sys
import shutil

from ogr2vrt import *
gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8","YES")
gdal.SetConfigOption("SHAPE_ENCODING","UTF-8")
#################################################################################################
VRT_Temp = "./cache/temp.vrt"
raster_Temp = "./cache/temp.tif"
extent_Temp = "./cache/temp_extent.shp"
# 对外接口
inputFileNameList = ["F:/GDALpdf/data/road_1.shp"]
displayName = ["connectIDs","ID"] #在模型树上显示的名称
outputPDFname = "F:/GDALpdf/11111.pdf"
##################################################################################################
# 缓存目录处理
def createCache():
    if not os.path.exists('cache'):
        os.mkdir('cache')
def deleteCache():
    shutil.rmtree('./cache')
##################################################################################################
createCache() # 建立缓存目录
#2.生成vrt文件
Ogr2vrt(inputFileNameList,VRT_Temp)
#3 生成范围的空白shp文件
os.system("ogrtindex -accept_different_schemas ./cache/temp_extent.shp "+ inputFileNameList[0])
#4 生成空白底图
os.system("gdal_rasterize -burn 255 -ot Byte -ts 4000 4000 ./cache/temp_extent.shp ./cache/temp.tif")
#5 生成PDF
driver = gdal.GetDriverByName( "PDF" )
ds = gdal.Open(raster_Temp)
createPDF = driver.CreateCopy( outputPDFname, ds, 0 ,\
    [ 'OGR_DATASOURCE=./cache/temp.vrt', "OGR_DISPLAY_FIELD=" + displayName[0] ])
ds = None
createPDF = None

# deleteCache() # 清空缓存
