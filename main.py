# -*- coding:utf-8 -*-
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
import os
from ogr2vrt import *
import sys
reload(sys)
# sys.setdefaultencoding('utf-8')
# gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8","YES")
# gdal.SetConfigOption("SHAPE_ENCODING","UTF-8")
inputFilePath = "F:/GDALpdf/data/"
inputFileName = "road_1.shp"
outputFilePath = "F:/GDALpdf/"
dst_filename = "11111.pdf"
displayName = "connectIDs" #在模型树上显示的名称

#1 中文测试不需要!!
# os.system('ogr2ogr  -f "ESRI Shapefile" output.shp '+inputFilePath + inputFileName+' -lco ENCODING=UTF-8 ')
# exit()

#2.生成vrt文件 使用开源代码
outputVRT_Temp = "temp.vrt"
# ogr2vrt("output.shp",outputVRT_Temp)
ogr2vrt(inputFilePath+inputFileName,outputVRT_Temp)
# os.system("python ogr2vrt.py " + outputVRT + " " + inputFileName)
# os.system('gdalbuildvrt jlist.vrt /*.shp ')
# exit()

#3 生成范围
outputExtent = "temp_extent.shp"
os.system("ogrtindex -accept_different_schemas " + outputExtent +" "+ inputFilePath + inputFileName)

#4 生成空白底图
#使用python替换命令行
# option = gdal.RasterizeOptions(xRes="0.0001", yRes="0.0001", burnValues="0" , outputBounds="Byte" )
# print gdal.Rasterize(destNameOrDestDS="F:/GDALpdf/data/node_2.tif",srcDS='F:/GDALpdf/data/node_extent.shp', burnValues=0)
#原句
outputRaster_Temp = "temp.tif"
os.system("gdal_rasterize -burn 255 -ot Byte -ts 2000 2000 "  + outputExtent + " " + outputRaster_Temp)


#5 生成PDF
driver = gdal.GetDriverByName( "PDF" )
ds = gdal.Open(outputRaster_Temp)
dst_ds = driver.CreateCopy( outputFilePath + dst_filename, ds, 0 ,[ 'OGR_DATASOURCE='+outputVRT_Temp,"OGR_DISPLAY_FIELD="+displayName])
ds = None
dst_ds = None
