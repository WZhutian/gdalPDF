# -*- coding:utf-8 -*-
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
import os
import shutil
from ogr2vrt0 import *
import sys
reload(sys)
# sys.setdefaultencoding('utf-8')
# gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8","YES")
# gdal.SetConfigOption("SHAPE_ENCODING","UTF-8")
inputFileNameList = ["F:/GDALpdf/data/road_1.shp",'F:/GDALpdf/data/node.shp']
displayName = ["connectIDs","ID"] #在模型树上显示的名称
dst_filename = "F:/GDALpdf/11111.pdf"
outputVRT_Temp = "./cache/temp.vrt"
outputRaster_Temp = "./cache/temp.tif"
outputExtent = "./cache/temp_extent.shp"

def deleteCache():
    shutil.rmtree('./cache')
##################################################################################################
def createCache():
    if not os.path.exists('cache'):
        os.mkdir('cache')
##################################################################################################
createCache() # 建立缓存目录
#2.生成vrt文件 使用开源代码
# ogr2vrt("output.shp",outputVRT_Temp)
ogr2vrt(inputFileNameList,outputVRT_Temp)
# os.system("python ogr2vrt.py " + outputVRT + " " + inputFileName)
# os.system('gdalbuildvrt jlist.vrt /*.shp ')
# exit()

#3 生成范围
os.system("ogrtindex -accept_different_schemas " + outputExtent +" "+ inputFileNameList[0])

#4 生成空白底图
#使用python替换命令行
# option = gdal.RasterizeOptions(xRes="0.0001", yRes="0.0001", burnValues="0" , outputBounds="Byte" )
# print gdal.Rasterize(destNameOrDestDS="F:/GDALpdf/data/node_2.tif",srcDS='F:/GDALpdf/data/node_extent.shp', burnValues=0)
#原句
os.system("gdal_rasterize -burn 255 -ot Byte -ts 200 200 "  + outputExtent + " " + outputRaster_Temp)


#5 生成PDF
driver = gdal.GetDriverByName( "PDF" )
ds = gdal.Open(outputRaster_Temp)
dst_ds = driver.CreateCopy( dst_filename, ds, 0 ,[ 'OGR_DATASOURCE='+outputVRT_Temp,"OGR_DISPLAY_FIELD="+displayName[0]])
ds = None
dst_ds = None
deleteCache()#清空缓存
