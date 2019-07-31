#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from pykml import parser

with open(sys.argv[1],'rt') as f:
    kml = parser.parse(f).getroot()
slist = [u"白云区", u"从化区", u"东山区", u"番禺区", u"海珠区", u"花都区", u"黄埔区", u"荔湾区", u"南沙区", u"天河区", u"越秀区", u"增城区"]
cbfs = [u"综合业务接入局", u"综合业务接入区"]
SEPRATOR = ";"
folders = kml.findall('.//{http://www.opengis.net/kml/2.2}Folder')
#print(len(folders))
#linearrings = kml.findall('.//{http://www.opengis.net/kml/2.2}LinearRing')
#print(len(linearrings))
for each in folders:
    if (each.name in slist):
        for fd in each.Folder:
            if (fd.name == cbfs[0]):
                for pm in fd.Placemark:
                    row = ("" + each.name + SEPRATOR + cbfs[0] + SEPRATOR + pm.name)
                    if (hasattr(pm, 'LookAt')):
                        row +=  (SEPRATOR + str(pm.LookAt.longitude) + "," + str(pm.LookAt.latitude))
                    else:
                        row += (SEPRATOR + pm.Point.coordinates);
                    print(row)
            elif (fd.name == cbfs[1]):
                for pm in fd.Placemark:
                    if (hasattr(pm, 'Polygon')):
                        print("" + each.name + SEPRATOR + cbfs[1] + SEPRATOR + pm.name + SEPRATOR + str(pm.Polygon.outerBoundaryIs.LinearRing.coordinates).strip())
                    else:
                        print("" + each.name + SEPRATOR + cbfs[1] + SEPRATOR + pm.name + SEPRATOR + str(pm.MultiGeometry.Polygon.outerBoundaryIs.LinearRing.coordinates).strip())
            