<?xml version="1.0" encoding="UTF-8"?>
<!-- Processes ArcGIS metadata to remove empty XML elements to avoid exporting and validation errors. -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" >
	<xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes" omit-xml-declaration="no" />

	<!-- start processing all nodes and attributes in the XML document -->
	<!-- any CDATA blocks in the original XML will be lost because they can't be handled by XSLT -->
	<xsl:template match="/">
		<xsl:apply-templates select="node() | @*" />
	</xsl:template>

	<!-- copy all nodes and attributes in the XML document -->
	<xsl:template match="node() | @*" priority="0">
		<xsl:copy>
			<xsl:apply-templates select="node() | @*" />
		</xsl:copy>
	</xsl:template>

	<!-- templates below override the default template above that copies all nodes and attributes -->
	
	<!-- exclude geoprocessing history -->
	<xsl:template match="/metadata/Esri/DataProperties/lineage" priority="1"> 
	</xsl:template>
	<xsl:template match="mdMaint | resMaint" priority="2"> <!-- Maintenance Information (B.2.5 MD_MaintenanceInformation - line142) -->
	</xsl:template>
	<xsl:template match="/metadata/eainfo" priority="3"> <!-- Entity and Attribute -->
	</xsl:template>	
	<xsl:template match="coordRef" priority="11"> <!-- 	ESRI SPATIAL PROPERTIES -->
	</xsl:template>		
	<xsl:template match="VectSpatRep" priority="20"> <!-- Vector Information (B.2.6  MD_VectorSpatialRepresentation - line176) -->
	</xsl:template>
	<xsl:template match="dataExt | scpExt | srcExt" priority="25"> <!-- Extent Information (B.3.1 EX_Extent - line334) -->
	</xsl:template>
	<xsl:template match="mdContact" priority="25">   <!-- Metadat contact Information (B.3.1 EX_Extent - line334) -->
	</xsl:template>	
</xsl:stylesheet>
