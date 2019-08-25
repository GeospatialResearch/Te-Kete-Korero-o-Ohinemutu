
const sld_header = `<?xml version="1.0" encoding="ISO-8859-1"?>
                    <StyledLayerDescriptor version="1.0.0"
                    		xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd"
                    		xmlns="http://www.opengis.net/sld"
                    		xmlns:ogc="http://www.opengis.net/ogc"
                    		xmlns:xlink="http://www.w3.org/1999/xlink"
                    		xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                    		<!-- a named layer is the basic building block of an sld document -->
                    	<NamedLayer>
                        <Name>Default Style</Name>
                        <UserStyle>`

const sld_end = `</UserStyle>
              	 </NamedLayer>
              </StyledLayerDescriptor>`

var generatePointSLD = function (styleObj) {
  var sld = `<FeatureTypeStyle>
               <Rule>
                 <PointSymbolizer>
                   <Graphic>
                     <Mark>
                       <WellKnownName>circle</WellKnownName>
                       <Fill>
                         <CssParameter name="fill">` + styleObj.color + `</CssParameter>
                         <CssParameter name="fill-opacity">` + styleObj.opacity + `</CssParameter>
                       </Fill>
                       <Stroke>
                         <CssParameter name="stroke">` + styleObj.bordercolor + `</CssParameter>
                         <CssParameter name="stroke-width">` + styleObj.borderwidth + `</CssParameter>
                       </Stroke>
                     </Mark>
                     <Size>` + styleObj.pointsize + `</Size>
                   </Graphic>
                 </PointSymbolizer>
               </Rule>
             </FeatureTypeStyle>`

  return sld_header + sld + sld_end
}

var generateLineSLD = function (styleObj) {

  var sld = `<FeatureTypeStyle>
              <Rule>
               <LineSymbolizer>
               <Stroke>
                   <CssParameter name="stroke">` + styleObj.color + `</CssParameter>
                   <CssParameter name="stroke-width">` + styleObj.linewidth + `</CssParameter>`
                   + (styleObj.dashedline ? `<CssParameter name="stroke-dasharray">` + styleObj.drawnline + ` ` + styleObj.blankspace + `</CssParameter>` : ``) + `
                   <CssParameter name="stroke-opacity">` + styleObj.opacity + `</CssParameter>
                   <CssParameter name="stroke-linecap">round</CssParameter>
                 </Stroke>
               </LineSymbolizer>
              </Rule>
           </FeatureTypeStyle>`

  return sld_header + sld + sld_end
}

var generatePolygonSLD = function (styleObj) {

  var sld = `<FeatureTypeStyle>
               <Rule>
                 <PolygonSymbolizer>
                   <Fill>
                     <CssParameter name="fill">` + styleObj.color + `</CssParameter>
                     <CssParameter name="fill-opacity">` + styleObj.opacity + `</CssParameter>
                   </Fill>
                   <Stroke>
                     <CssParameter name="stroke">` + styleObj.bordercolor + `</CssParameter>
                     <CssParameter name="stroke-width">` + styleObj.borderwidth + `</CssParameter>`
                     + (styleObj.dashedline ? `<CssParameter name="stroke-dasharray">` + styleObj.drawnline + ` ` + styleObj.blankspace + `</CssParameter>` : ``) + `
                   </Stroke>
                 </PolygonSymbolizer>
               </Rule>
             </FeatureTypeStyle>`

  return sld_header + sld + sld_end
}

module.exports = { generatePointSLD, generateLineSLD, generatePolygonSLD }
