import re
import os
import tarfile
from zipfile import ZipFile
from rest_framework.exceptions import ValidationError

from geoserver.catalog import Catalog

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

shp_exts = ['.shp', ]
csv_exts = ['.csv']
kml_exts = ['.kml']
json_exts = ['.json', '.geojson']
vec_exts = shp_exts + csv_exts + kml_exts + json_exts
cov_exts = ['.tif', '.tiff', '.geotiff', '.geotif', '.asc', '.jpg', '.jpeg', '.png', '.vrt', '.grd']


def layer_type(filename):
    """Finds out if a filename is raster or a vector
    """
    base_name, extension = os.path.splitext(filename)

    if extension.lower() == '.zip':
        zf = ZipFile(filename)
        # ZipFile doesn't support with statement in 2.6, so don't do it
        try:
            for n in zf.namelist():
                b, e = os.path.splitext(n.lower())
                if e in vec_exts or e in cov_exts:
                    extension = e
        finally:
            zf.close()

    if extension.lower() in vec_exts:
        return 'vector'
    elif extension.lower() in cov_exts:
        return 'raster'


def get_catalog():
    gs_user = os.environ.get('GEOSERVER_USERNAME', 'admin')
    gs_pass = os.environ.get('GEOSERVER_PASSWORD', 'geoserver')
    cat = Catalog("http://geoserver:8080/geoserver/rest/", gs_user, gs_pass)
    return cat


def send_email(emaildata ,emailtype):

    text_content = ''
    htmly = get_template('../templates/app/' + emailtype + '.html')
    html_content = htmly.render(emaildata)
    subject = 'New comment in your narrative'

    msg = EmailMultiAlternatives(subject, text_content, 'geospatial.gri@gmail.com', emaildata['mailing_list'])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def SLDfilterByAttrib(legend_list, field):

	mysld = StyledLayerDescriptor()
	nl = mysld.create_namedlayer('myLayer')
	ustyle = nl.create_userstyle()
	ustyle.Title = 'Style Title'
	fts = ustyle.create_featuretypestyle()

	for c in legend_list:

		rule = fts.create_rule(c)

		f = Filter(rule)
		f.PropertyIsEqualTo = PropertyCriterion(f, 'PropertyIsEqualTo')
		f.PropertyIsEqualTo.PropertyName = field
		f.PropertyIsEqualTo.Literal = c

		rule.Filter = f

		psymb = PointSymbolizer(rule)
		graphic = Graphic(psymb)
		mark = Mark(graphic)
		mark.WellKnownName = 'circle'

		fillstyle = Fill(mark)
		strokestyle = Stroke(mark)

		color = '#%06X' % random.randint(0,256**3-1)

		fillstyle.create_cssparameter('fill', color)
		strokestyle.create_cssparameter('stroke', '#000000')

		#print fillstyle.CssParameters[0].Value
		mark.Fill = fillstyle.CssParameters[0]
		mark.Stroke = strokestyle.CssParameters[0]

		#graphic.Mark = mark
		graphic.Size = str(6).decode("utf-8")
		#psymb.Graphic = graphic
		#rule.PointSymbolizer = psymb

	# generate SLD content
	content = mysld.as_sld(pretty_print=True)
	index = content.find('<sld:StyledLayerDescriptor') + len('<sld:StyledLayerDescriptor') + 1
	content[:index] + 'xmlns:sld="http://www.opengis.net/sld"' + content[index:]

	return content
