# -*- coding: utf-8 -*-
try:
    from osgeo import osr, ogr, gdal
except ImportError:
    import osr, ogr, gdal
gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8","YES")
gdal.SetConfigOption("SHAPE_ENCODING","")
#############################################################################
class Ogr2vrt(object):
    def GeomType2Name(self, type):
        if type == ogr.wkbUnknown:
            return 'wkbUnknown'
        elif type == ogr.wkbPoint:
            return 'wkbPoint'
        elif type == ogr.wkbLineString:
            return 'wkbLineString'
        elif type == ogr.wkbPolygon:
            return 'wkbPolygon'
        elif type == ogr.wkbMultiPoint:
            return 'wkbMultiPoint'
        elif type == ogr.wkbMultiLineString:
            return 'wkbMultiLineString'
        elif type == ogr.wkbMultiPolygon:
            return 'wkbMultiPolygon'
        elif type == ogr.wkbGeometryCollection:
            return 'wkbGeometryCollection'
        elif type == ogr.wkbNone:
            return 'wkbNone'
        elif type == ogr.wkbLinearRing:
            return 'wkbLinearRing'
        else:
            return 'wkbUnknown'
    ##########################################
    def Esc(self, x):
        return x #return gdal.EscapeString(x, gdal.CPLES_XML )
    def cp2utf(self, x):
        return unicode(x, "cp936").encode('utf-8')
    #############################################################################
    # 1点:Symbol 2线:Pen 3面:Brush+Pen 4标签:Label
    """设置每个要素的样式
        dic:[类型,颜色,线形]
    """
    def styleSQL(self,dic,symbol):
        # <SrcSQL>SELECT *,'BRUSH(fc:#367C23);PEN(c:#B7B7B7,w:1px)' AS OGR_STYLE
    # FROM ne_10m_admin_0_countries</SrcSQL>
        sql = ' <SrcSQL>'
        sql += '</SrcSQL>'
        return
    def targetSRS(self,x):
        srs = '<TargetSRS>' + x + '</TargetSRS>' # EPSG:4326
        return srs
    #############################################################################
    # Argument processing.
    def __init__(self,infile,outfile,argv=" "):
        layer_list = []
        relative = "0"
        schema = 0
        feature_count = 0
        extent = 0
        argv = argv.split(",")
        if argv is None:
            i = 1
            while i < len(argv):
                arg = argv[i]
                if arg == '-relative':
                    relative = "1"
                elif arg == '-schema':
                    schema = 1
                elif arg == '-feature_count':
                    feature_count = 1
                elif arg == '-extent':
                    extent = 1
                else:
                    layer_list.append( arg )
                i = i + 1

        if schema and feature_count:
            sys.stderr.write('Ignoring -feature_count when used with -schema.\n')
            feature_count = 0

        if schema and extent:
            sys.stderr.write('Ignoring -extent when used with -schema.\n')
            extent = 0
        #############################################################################
        # Start the VRT file.

        vrt = '<OGRVRTDataSource>\n'

        #############################################################################
        # Open the datasource to read.
        for fileName in infile:
            layer_list=[]
            src_ds = ogr.Open( fileName, update = 0 )

            if schema:
                fileName = '@dummy@'

            for layer in src_ds:
                layer_list.append( layer.GetLayerDefn().GetName() )

            #############################################################################
            #	Process each source layer.
            for name in layer_list:
                layer = src_ds.GetLayerByName(name)
                layerdef = layer.GetLayerDefn()

                vrt += '  <OGRVRTLayer name="%s">\n' % self.Esc(name)
                vrt += '    <SrcDataSource relativeToVRT="%s" shared="%d">%s</SrcDataSource>\n' \
                       % (relative,not schema,self.Esc(fileName))
                if schema:
                    vrt += '    <SrcLayer>@dummy@</SrcLayer>\n'
                else:
                    vrt += '    <SrcLayer>%s</SrcLayer>\n' % self.Esc(name)

                # Historic format for mono-geometry layers
                if layerdef.GetGeomFieldCount() == 0:
                    vrt += '    <GeometryType>wkbNone</GeometryType>\n'
                elif layerdef.GetGeomFieldCount() == 1:
                    vrt += '    <GeometryType>%s</GeometryType>\n' \
                        % self.GeomType2Name(layerdef.GetGeomType())
                    srs = layer.GetSpatialRef()
                    if srs is not None:
                        vrt += '    <LayerSRS>%s</LayerSRS>\n' \
                            % (self.Esc(srs.ExportToWkt()))
                    if extent:
                        (xmin, xmax, ymin, ymax) = layer.GetExtent()
                        vrt += '    <ExtentXMin>%.15g</ExtentXMin>\n' % xmin
                        vrt += '    <ExtentYMin>%.15g</ExtentYMin>\n' % ymin
                        vrt += '    <ExtentXMax>%.15g</ExtentXMax>\n' % xmax
                        vrt += '    <ExtentYMax>%.15g</ExtentYMax>\n' % ymax

                # New format for multi-geometry field support
                else:
                    for fld_index in range(layerdef.GetGeomFieldCount()):
                        src_fd = layerdef.GetGeomFieldDefn( fld_index )
                        vrt += '    <GeometryField name="%s">\n' % src_fd.GetName()
                        vrt += '      <GeometryType>%s</GeometryType>\n' \
                                % self.GeomType2Name(src_fd.GetType())
                        srs = src_fd.GetSpatialRef()
                        if srs is not None:
                            vrt += '      <SRS>%s</SRS>\n' \
                                    % (self.Esc(srs.ExportToWkt()))
                        if extent:
                            (xmin, xmax, ymin, ymax) = layer.GetExtent(geom_field = fld_index)
                            vrt += '      <ExtentXMin>%.15g</ExtentXMin>\n' % xmin
                            vrt += '      <ExtentYMin>%.15g</ExtentYMin>\n' % ymin
                            vrt += '      <ExtentXMax>%.15g</ExtentXMax>\n' % xmax
                            vrt += '      <ExtentYMax>%.15g</ExtentYMax>\n' % ymax
                        vrt += '    </GeometryField>\n'

                # Process all the fields.
                for fld_index in range(layerdef.GetFieldCount()):
                    src_fd = layerdef.GetFieldDefn( fld_index )
                    if src_fd.GetType() == ogr.OFTInteger:
                        type = 'Integer'
                    elif src_fd.GetType() == ogr.OFTString:
                        type = 'String'
                    elif src_fd.GetType() == ogr.OFTReal:
                        type = 'Real'
                    elif src_fd.GetType() == ogr.OFTStringList:
                        type = 'StringList'
                    elif src_fd.GetType() == ogr.OFTIntegerList:
                        type = 'IntegerList'
                    elif src_fd.GetType() == ogr.OFTRealList:
                        type = 'RealList'
                    elif src_fd.GetType() == ogr.OFTBinary:
                        type = 'Binary'
                    elif src_fd.GetType() == ogr.OFTDate:
                        type = 'Date'
                    elif src_fd.GetType() == ogr.OFTTime:
                        type = 'Time'
                    elif src_fd.GetType() == ogr.OFTDateTime:
                        type = 'DateTime'
                    else:
                        type = 'String'
                    vrt += '    <Field name="%s" type="%s"' \
                           % (self.cp2utf(src_fd.GetName()), type) # 中文cp936转码
                    if not schema:
                        vrt += ' src="%s"' % self.Esc(src_fd.GetName())
                    if src_fd.GetWidth() > 0:
                        vrt += ' width="%d"' % src_fd.GetWidth()
                    if src_fd.GetPrecision() > 0:
                        vrt += ' precision="%d"' % src_fd.GetPrecision()
                    vrt += '/>\n'
                if feature_count:
                    vrt += '    <FeatureCount>%d</FeatureCount>\n' % layer.GetFeatureCount()
                #######################
                # 额外
                #
                # 添加SQL语句
                vrt += "    <SrcSQL>SELECT *,'BRUSH(fc:#367C23);PEN(c:\"#BB0000\",w:20px)' AS OGR_STYLE FROM "+name+" </SrcSQL>\n"
                vrt += "    <SrcSQL>SELECT *,'BRUSH(fc:#367C23);PEN(c:\"#B7B7B7\",w:1px)' AS OGR_STYLE FROM "+name+" WHERE bridge = '0'</SrcSQL>\n"
                vrt += '  </OGRVRTLayer>\n'

        vrt += '</OGRVRTDataSource>\n'

        #############################################################################
        # Write vrt
        open(outfile,'w').write(vrt)
