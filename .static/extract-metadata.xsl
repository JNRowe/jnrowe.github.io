<?xml version="1.0"?>
<xsl:stylesheet 
  version="1.0" 
  xmlns:cc="http://web.resource.org/cc/"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:dcterms="http://purl.org/dc/terms/"
  xmlns:foaf="http://xmlns.com/foaf/0.1/" 
  xmlns:html="http://www.w3.org/1999/xhtml"
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
>

  <xsl:output method="xml" indent="yes" />

  <xsl:template match="html:html">
    <rdf:RDF>
      <cc:Work rdf:about="">
        <dc:format>application/xhtml+xml</dc:format>
        <dc:resource-type>document</dc:resource-type>
        <xsl:apply-templates />
      </cc:Work>
      <xsl:for-each select=".//html:link[@rel='license' and starts-with(@href,'http://creativecommons.org/licenses/')]">
        <xsl:copy-of select="document('')/xsl:stylesheet/rdf:RDF/cc:License[@rdf:about=current()/@href]"/>
      </xsl:for-each>
    </rdf:RDF>
  </xsl:template>

  <xsl:template match="html:head">
    <dc:title><xsl:value-of select="substring-before(html:title, ' &#8212;')" /></dc:title>
    <xsl:for-each select="html:link[@title = 'FOAF']">
      <foaf:creator rdf:resource="{@href}" />
    </xsl:for-each>
    <xsl:for-each select="html:meta[@name = 'description']">
      <dc:description><xsl:value-of select='@content'/></dc:description>
    </xsl:for-each>
    <xsl:for-each select="html:meta[@name = 'language']">
      <dc:language><xsl:value-of select='@content'/></dc:language>
    </xsl:for-each>
    <xsl:for-each select="html:link[@rel='license' and starts-with(@href,'http://creativecommons.org/licenses/')]">
      <cc:license rdf:resource="{@href}" />
    </xsl:for-each>
  </xsl:template>

  <xsl:template match="html:a[contains(@class, 'fn')]">
    <dc:creator><xsl:value-of select="." /></dc:creator>
  </xsl:template>
  <xsl:template match="html:a[contains(@class, 'email')]">
    <dc:creator.address><xsl:value-of select="@href" /></dc:creator.address>
  </xsl:template>

  <xsl:template match="html:a[contains(@rel, 'bookmark')]">
    <dc:identifier><xsl:value-of select="@href" /></dc:identifier>
  </xsl:template>

  <xsl:template match="html:span[@class = 'tags']">
    <xsl:for-each select="html:a[contains(@rel, 'tag')]">
      <dc:subject><xsl:value-of select="." /></dc:subject>
    </xsl:for-each>
  </xsl:template>

  <xsl:template match="html:abbr[@class = 'updated']">
    <dcterms:modified><xsl:value-of select="@title" /></dcterms:modified>
  </xsl:template>
  <xsl:template match="html:abbr[@class = 'published']">
    <dcterms:created><xsl:value-of select="@title" /></dcterms:created>
    <dcterms:issued><xsl:value-of select="@title" /></dcterms:issued>
  </xsl:template>

  <xsl:template match="text()|@*" />

  <rdf:RDF>
    <!-- Taken from http://creativecommons.org/technology/cc:Licenseoutput -->

    <cc:License rdf:about="http://creativecommons.org/licenses/by/2.5/">
      <cc:requires rdf:resource="http://web.resource.org/cc/Attribution" />
      <cc:permits rdf:resource="http://web.resource.org/cc/Reproduction" />
      <cc:permits rdf:resource="http://web.resource.org/cc/Distribution" />
      <cc:permits rdf:resource="http://web.resource.org/cc/DerivativeWorks" />
      <cc:requires rdf:resource="http://web.resource.org/cc/Notice" />
    </cc:License>

    <cc:License rdf:about="http://creativecommons.org/licenses/by-nd/2.5/">
      <cc:requires rdf:resource="http://web.resource.org/cc/Attribution" />
      <cc:permits rdf:resource="http://web.resource.org/cc/Reproduction" />
      <cc:permits rdf:resource="http://web.resource.org/cc/Distribution" />
      <cc:requires rdf:resource="http://web.resource.org/cc/Notice" />
    </cc:License>

    <cc:License rdf:about="http://creativecommons.org/licenses/by-nc-nd/2.5/">
      <cc:requires rdf:resource="http://web.resource.org/cc/Attribution" />
      <cc:permits rdf:resource="http://web.resource.org/cc/Reproduction" />
      <cc:permits rdf:resource="http://web.resource.org/cc/Distribution" />
      <cc:prohibits rdf:resource="http://web.resource.org/cc/CommercialUse" />
      <cc:requires rdf:resource="http://web.resource.org/cc/Notice" />
    </cc:License>

    <cc:License rdf:about="http://creativecommons.org/licenses/by-nc/2.5/">
      <cc:requires rdf:resource="http://web.resource.org/cc/Attribution" />
      <cc:permits rdf:resource="http://web.resource.org/cc/Reproduction" />
      <cc:permits rdf:resource="http://web.resource.org/cc/Distribution" />
      <cc:permits rdf:resource="http://web.resource.org/cc/DerivativeWorks" />
      <cc:prohibits rdf:resource="http://web.resource.org/cc/CommercialUse" />
      <cc:requires rdf:resource="http://web.resource.org/cc/Notice" />
    </cc:License>

    <cc:License rdf:about="http://creativecommons.org/licenses/by-nc-sa/2.5/">
      <cc:requires rdf:resource="http://web.resource.org/cc/Attribution" />
      <cc:permits rdf:resource="http://web.resource.org/cc/Reproduction" />
      <cc:permits rdf:resource="http://web.resource.org/cc/Distribution" />
      <cc:permits rdf:resource="http://web.resource.org/cc/DerivativeWorks" />
      <cc:requires rdf:resource="http://web.resource.org/cc/ShareAlike" />
      <cc:prohibits rdf:resource="http://web.resource.org/cc/CommercialUse" />
      <cc:requires rdf:resource="http://web.resource.org/cc/Notice" />
    </cc:License>

    <cc:License rdf:about="http://creativecommons.org/licenses/by-sa/2.5/">
      <cc:requires rdf:resource="http://web.resource.org/cc/Attribution" />
      <cc:permits rdf:resource="http://web.resource.org/cc/Reproduction" />
      <cc:permits rdf:resource="http://web.resource.org/cc/Distribution" />
      <cc:permits rdf:resource="http://web.resource.org/cc/DerivativeWorks" />
      <cc:requires rdf:resource="http://web.resource.org/cc/ShareAlike" />
      <cc:requires rdf:resource="http://web.resource.org/cc/Notice" />
    </cc:License>

    <cc:License rdf:about="http://web.resource.org/cc/PublicDomain">
      <cc:permits rdf:resource="http://web.resource.org/cc/Reproduction" />
      <cc:permits rdf:resource="http://web.resource.org/cc/Distribution" />
      <cc:permits rdf:resource="http://web.resource.org/cc/DerivativeWorks" />
    </cc:License>

  </rdf:RDF>

</xsl:stylesheet>

