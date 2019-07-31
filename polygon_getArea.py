#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import pyproj
import shapely
import shapely.ops as ops
from shapely.geometry.polygon import Polygon
from functools import partial

def polygon_area(points):
    #返回多边形面积
    area = 0

    geom = Polygon([
        (113.3229642216917,23.13612639347015), 
        (113.322559275276,23.13005230049122), 
        (113.3306848084265,23.12939050720481),
        (113.3301245455429,23.13597562831565),
        (113.3229642216917,23.13612639347015)
    ])
    geom_area = ops.transform(
        partial(
            pyproj.transform,
            pyproj.Proj(init='EPSG:4362'),
            pyproj.Proj(
                proj = 'aea',
                lat_1 = geom.bounds[1],
                lat_2 = geom.bounds[3]
            )
        ),
        geom
    )

    return geom_area.area

print(polygon_area([]))