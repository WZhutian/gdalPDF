# -*- coding:utf-8 -*-
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
import os,math,sys
import shutil

from styleList import *
from ogr2vrt import *
gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8","YES")
gdal.SetConfigOption("SHAPE_ENCODING","UTF-8")
#################################################################################################
VRT_Temp = "./cache/temp.vrt"
raster_Temp = "./cache/temp.tif"
extent_Temp = "./cache/temp_extent.shp"
# 对外接口
inputFileNameList = ["F:/GDALpdf/data/China.shp","F:/GDALpdf/data/road_1.shp"]
displayName = ["name","ID"] #在模型树上显示的名称
outputPDFname = "F:/GDALpdf/11111.pdf"

test = OgrFeatureStyle('polygon')
test.setBrush("#ff0000","#ff0000")
test.setPen("#1382e9","1px")
sqlStyleList = [test.getSQL(),test.getSQL()]
##################################################################################################
# 缓存目录处理
def createCache():
    if not os.path.exists('cache'):
        os.mkdir('cache')
def deleteCache():
    shutil.rmtree('./cache')

# 矢量栅格化接口,输入出图的宽和高,默认为平铺,若为适应模式,则只取width作为放大倍数
#ps 生成的缓存文件大小与width,height有关,大约值 = width*height(KB),建议不要太大
def rasterize(vector_fn,raster_fn,width,height,type = "tile"):
    inGridSize = float(2)/110575# 从GCS坐标转换到2米的网格
    # 打开 shp 并获取范围
    source_ds = ogr.Open(vector_fn)
    source_layer = source_ds.GetLayer()
    x_min, x_max, y_min, y_max = source_layer.GetExtent()
    # 计算高度宽度
    x_res = int((x_max - x_min) / inGridSize)
    y_res = int((y_max - y_min) / inGridSize)

    pix_width = inGridSize/(float(width)/x_res)
    pix_height = inGridSize/(float(height)/y_res)
    if type == "tile":
        pix_width = max(pix_width,pix_height)
        pix_height = pix_width
    elif type == "fit":
        height = width * y_res / x_res
        pix_height = pix_width
    #创建临时的raster并设置地理位置信息
    target_ds = gdal.GetDriverByName('GTiff').Create(raster_fn, width, height, 1, gdal.GDT_Byte)
    target_ds.SetProjection(source_layer.GetSpatialRef().ExportToWkt())# 设置SRS
    target_ds.SetGeoTransform((x_min, pix_width, 0, y_max,0, -pix_height))# 转换图像空间参考
    # 更新Tif
    gdal.RasterizeLayer(target_ds, [1], source_layer,burn_values = [255]) #设置灰度值,255-白色

# 创建地理参考范围的矩形要素
def createExtent(vector_fn,extfile):
    source_ds = ogr.Open(vector_fn)
    source_layer = source_ds.GetLayer()
    driver = ogr.GetDriverByName("ESRI Shapefile")
    if os.access( extfile, os.F_OK ):
        driver.DeleteDataSource( extfile )
    extent = source_layer.GetExtent()
    newds = driver.CreateDataSource(extfile)
    layernew = newds.CreateLayer('rect',source_layer.GetSpatialRef(),ogr.wkbPolygon)
    width = math.fabs(extent[1]-extent[0])
    height = math.fabs(extent[3]-extent[2])
    tw = width/2
    th = width/2
    extnew = extent[0]+tw
    wkt = 'POLYGON ((%f %f,%f %f,%f %f,%f %f,%f %f))' % (extent[0],extent[3],
        extent[1],extent[3], extent[1],extent[2],
        extent[0],extent[2], extent[0],extent[3])
    geom = ogr.CreateGeometryFromWkt(wkt)
    feat = ogr.Feature(layernew.GetLayerDefn())
    feat.SetGeometry(geom)
    layernew.CreateFeature(feat)
    newds.Destroy()

##################################################################################################
createCache() # 建立缓存目录
#2.生成vrt文件
Ogr2vrt(inputFileNameList,VRT_Temp,sqlStyleList)
#3 生成范围的空白shp文件
# os.system("ogrtindex -accept_different_schemas ./cache/temp_extent.shp "+ inputFileNameList[0])
createExtent(inputFileNameList[0],"./cache/temp_extent.shp")
#4 生成空白底图
# os.system("gdal_rasterize -burn 255 -ot Byte -ts 4000 4000 ./cache/temp_extent.shp ./cache/temp.tif")
rasterize("./cache/temp_extent.shp", "./cache/temp.tif",4000 , 4000,'fit')
# exit()
#5 生成PDF
driver = gdal.GetDriverByName( "PDF" )
ds = gdal.Open(raster_Temp)
createPDF = driver.CreateCopy( outputPDFname, ds, 0 ,\
    [ 'OGR_DATASOURCE=./cache/temp.vrt', "OGR_DISPLAY_FIELD=" + displayName[0] ])
ds = None
createPDF = None

# deleteCache() # 清空缓存
