# -*- coding: utf-8 -*-
#Iterate over feature classes and tables in a geodatabase and create xml, html, and pdf outputs


#Configurable parameters. For detials see urther below.
#path_wkthmltopdf, include_list, gdb, customXSLT, output_dirXML, output_dirHTML, output_dirPDF


###################
# Import Modules  #
###################

import arcpy    #used for ArcGIS stuff
import tempfile #used to control the output directory of the export metadata gp tool 
import os       #used for joining path and file names
"""
INFO FOR GETTING THE PDF EXPORT TO WORK WITH PDFKIT
1.download pdfkit or get it via pip 
2.copy paste pdfkit into C:\Python27\ArcGIS10.4\Lib
3.now import pdfkit should not throw error
4. but you need to download http://wkhtmltopdf.org/downloads.html (32bit)
5.in your sript before you can use pdfkit to create pdf you need to do :
 >>> path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
 >>> config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
6. then can create pdf like this:
 >>> pdfkit.from_file(r'G:\Tobias\testGPOutput\metadataXMLsandHTTPs\EGISADMIN.ALL_CAMPUS_LOCATIONS_XSLTransform_conversion.html', r'G:\Tobias\testGPOutput\metadataXMLsandHTTPs\EGISADMIN.ALL_CAMPUS_LOCATIONS_XSLTransform_conversion.pdf', configuration=config)
"""
try:
    import pdfkit
    print("pdfkit package imported!!")
except:
    print("Failed to import pdfkit package!!")
    

###################
#Define Parameters#
###################

path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

#inlcude list is a list of feature class or table names that should be included.
#if it is an empty string or an empty list this parameter is ignored and all feature
#classes and geodatabase tables will be included.
include_list = []#['EGISADMIN.Structure_Footprint','EGISADMIN.Parking','CIVILUTIL.wHydrant','EGISADMIN.Signs_Demo']

#the geodatabase for which to export one XML file per feature class or table
#gdb = r'Database Connections\EGISADMIN to PROD.sde'
gdb = r'Database Connections\UServices GIS.sde'

#the output directory where the metadata XML fles should be written to
output_dirXML = r'G:\metadataExporter\xml'
output_dirHTML = r'G:\metadataExporter\html'
output_dirPDF = r'G:\metadataExporter\pdf'

#path to custom XSLT file that removes certain metadata sections from the output xml, html, and pdf file
customXSLT = r'G:\metadataExporter\remove geoprocessing history.xslt'

##################
#Define functions#
##################

##################
#Begin processing#
##################
#set the workspace, get the feature class names (incl. the ones that are in feature datasets),
#the table names, and create a list of all of them
print('\n ...now building a list of all the feature classes, geodatabsae tables, and rasters that are available in the workspace: ' + gdb)

arcpy.env.workspace = gdb

featureclasses = arcpy.ListFeatureClasses()
featuredatasets = arcpy.ListDatasets()
for featuredataset in featuredatasets:
    featureclasses_in_featuredataset = arcpy.ListFeatureClasses(feature_dataset=featuredataset)
    for featureclass in featureclasses_in_featuredataset:
        if featureclass in include_list:
            featureclasses = featureclasses + [featureclass]
tables = arcpy.ListTables()
rasters = arcpy.ListRasters()

featureclasses_and_tables = featureclasses + tables + rasters #sorry name is misleading. Rasters are included as well.

#if the include_list parameter is specified remove from featureclasses_and_tables everything
#except for the items specified in the include_list
print('\n...narrowing dow this list based on the include_list parameter')
filtered_list_of_featureclasses_and_tables = []
if len(include_list)>0:
    for item in featureclasses_and_tables:
        if str(item) in include_list:
            filtered_list_of_featureclasses_and_tables.append(item)
else:
    filtered_list_of_featureclasses_and_tables = featureclasses_and_tables

#prepend the workspace path becasue we need to switch the workspace for the export metadata tool output.
#create nested list so we can keep the feature class name to name the output file of the export metadata tool.
filtered_list_of_featureclasses_and_tables_with_gdbpath = []
for item in filtered_list_of_featureclasses_and_tables:
    filtered_list_of_featureclasses_and_tables_with_gdbpath = filtered_list_of_featureclasses_and_tables_with_gdbpath + [[str(item),os.path.join(gdb, str(item))]]

#these are the items we are outputtng metadata for
print('\n...these are the items we are outputtng metadata for:')
print(filtered_list_of_featureclasses_and_tables_with_gdbpath)


arcpy.env.workspace = output_dirXML
ArcGIS_install_dir = arcpy.GetInstallInfo("desktop")["InstallDir"]
xslt = ArcGIS_install_dir + "Metadata/Stylesheets/ArcGIS.xsl"
print('\n...now iterating over this list and exporting the metadata to files')
for item in filtered_list_of_featureclasses_and_tables_with_gdbpath:

    print('\n\n\n...now processing '+item[0])
    
    try:
        #create an XML file with certain metadata elements removed using a custom xslt stylesheet
        inFC = item[1]
        outXML = os.path.join(output_dirXML , item[0]+".xml")
        #if the file already exists delete it before exporting the new one
        if os.path.exists(outXML):
            os.remove(outXML)
            print('Deleted existing '+ outXML)
        arcpy.XSLTransform_conversion(inFC, customXSLT , outXML, "#")
        print('Created '+ outXML)

        #turn the XML file int oan html file
        inXML = outXML
        outHTML = os.path.join(output_dirHTML , item[0]+".html")
        #if the file already exists delete it before exporting the new one
        if os.path.exists(outHTML):
            os.remove(outHTML)
            print('Deleted existing '+ outHTML)
        arcpy.XSLTransform_conversion(inXML, xslt, outHTML, "#")
        print('Created '+ outHTML)

        #turn the  html file into a pdf file
        inHTML = outHTML
        outPDF = os.path.join(output_dirPDF , item[0]+".pdf")
        #if the file already exists delete it before exporting the new one
        if os.path.exists(outPDF):
            os.remove(outPDF)
            print('Deleted existing '+ outPDF)
        pdfkit.from_file(inHTML, outPDF, configuration=config)
        print('Created '+ outPDF)
        
    except:
        print('Unable to output metadata for ' + item[0])
        
print('Finished.')
