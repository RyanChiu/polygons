#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time
import datetime
import pandas as pd

'''
输入——
必须两个参数：
第一个指向包含了单点位置的excel文件(必须包括字段DP、AC_NUM、LON、LAT），
第二个指向包含了多边形区域信息的excel文件（必须包括字段DP、SEC_NUM、NAME、POLYGON）
（分别有模板对应）
输出——
屏幕输出进度、错误信息等；同时将结果输出到以第一个文件名+时间戳的一个txt文件，
比如如果第一个文件名是“/tmp/123.xls”，则输出文件名将为“/tmp/123.xls_201907281223.txt”
'''
def IsPtInPoly(aLon, aLat, pointList):
    '''
    :param aLon: double 经度
    :param aLat: double 纬度
    :param pointList: list [(lon, lat)...] 多边形点的顺序需根据顺时针或逆时针，不能乱
    '''
    
    iSum = 0
    iCount = len(pointList)
    
    if(iCount < 3):
        return False
    
    
    for i in range(iCount):
        
        pLon1 = pointList[i][0]
        pLat1 = pointList[i][1]
        
        if(i == iCount - 1):
            
            pLon2 = pointList[0][0]
            pLat2 = pointList[0][1]
        else:
            pLon2 = pointList[i + 1][0]
            pLat2 = pointList[i + 1][1]
        
        if ((aLat >= pLat1) and (aLat < pLat2)) or ((aLat>=pLat2) and (aLat < pLat1)):
            
            if (abs(pLat1 - pLat2) > 0):
                
                pLon = pLon1 - ((pLon1 - pLon2) * (pLat1 - aLat)) / (pLat1 - pLat2);
                
                if(pLon < aLon):
                    iSum += 1
 
    if(iSum % 2 != 0):
        return True
    else:
        return False

'''
# the following lines are for debug
poly = [
    [113.3229642216917,23.13612639347015], 
    [113.322559275276,23.13005230049122], 
    [113.3306848084265,23.12939050720481],
    [113.3301245455429,23.13597562831565],
    [113.3229642216917,23.13612639347015]
]

if (IsPtInPoly(113.31791,23.135187, poly)):
    print("IN!")
else:
    print("OUT!")
# exit() #for debug
'''

def isPtIn():
    starttime = time
    print(starttime.strftime('%Y%m%d-%H:%M:%S') + ", starts:")
    # main process starts
    if (len(sys.argv) != 3):
        print("Please give 2 xls/xlsx files, the 1st one continas the points, and the 2nd one contains the polygons.")
        exit()
    print("reading 2 files...")
    pts = pd.read_excel(sys.argv[1], encoding = "utf-8")
    pts.fillna("empty", inplace = True)
    pls = pd.read_excel(sys.argv[2], encoding = "utf-8")
    pls.fillna("empty", inplace = True)
    print(time.strftime('%Y%m%d-%H:%M:%S') + ", done.")

    # deal with the imported polygons, put those long/lat serials into a 2 dementions array
    print("deal with the polygons...")
    IAAs = []# (Integrated Access Area, IAA)
    for pl in pls.itertuples(index=True, name='Pandas'):
        plpts = getattr(pl, 'POLYGON')
        # print(getattr(pl, 'NAME') + ":" + poly)
        # print("*****")
        plpts = plpts.replace(",0 ", ",").replace(",0", "")
        plpts_array = plpts.split(",")
        plpts = map(eval, plpts_array)
        poly = []
        iaa = []
        if (len(plpts) % 2 == 0):
            i = 0
            parray = []
            for plpt in plpts:
                i += 1
                if (i % 2 != 0):
                    parray.append(plpt)
                else:
                    parray.append(plpt)
                    poly.append(parray)
                    parray = []
        else:
            print("worng" + len(plpts))
        iaa.append(poly)
        iaa.append(getattr(pl, 'DP'))
        iaa.append(getattr(pl, 'SEC_NUM'))
        iaa.append(getattr(pl, 'NAME'))
        IAAs.append(iaa)
    # print(IAAs[0]) # for debug

    pg_i = 0
    pg_total = len(pts)
    lines = []
    print("judging...")
    for pt in pts.itertuples(index=True, name='Pandas'):
        # print(getattr(pt, 'DP') + ";" + str(getattr(pt, 'LON')) + "," + str(getattr(pt, 'LAT'))) # for debug
        pg_i += 1
        perc = '{:.2f}'.format(float(pg_i) / float(pg_total) * 100)
        # continue # for debug
        for iaa in IAAs:
            if (IsPtInPoly(getattr(pt, 'LON'), getattr(pt, 'LAT'), iaa[0])):
                line = (
                    getattr(pt, 'DP') + ";" + getattr(pt, 'AC_NUM') + ";"
                    + str(getattr(pt, 'LON')) + ";" + str(getattr(pt, 'LAT')) + ";"
                    + iaa[1] + ";" + iaa[2] + ";" + iaa[3]
                )
                # print(line)
                lines.append(line + "\n")
        sys.stdout.write("\r" + str(pg_i) + "/" + str(pg_total) + ", " + str(perc) + "%")
        sys.stdout.flush()

    print("\nwriting...")
    dtnow = datetime.datetime.now()
    fh = open(sys.argv[1] + "-" + dtnow.strftime('%Y%m%d%H%M%S') + "_ptinpl.txt", mode = 'w')
    fh.writelines(lines)
    # main process ends

    endtime = time
    print(endtime.strftime('%Y%m%d-%H:%M:%S') + ", all processed.")

if __name__ == '__main__':
    isPtIn()