# -*- coding: UTF-8 -*-
def isPtInPoly(aLon, aLat, pointList):
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

def getPolyArr(plpts):
    '''
    : param plpts, a string that contains cordinates like "113.3222422776304,23.12154694922328,0 113.3300172328068,23.12091861653966,0",
    which is from kml file
    : return value, a multiple array like [[113.2, 23.2], [113.3, 23.3]], if input param is not in
    right format, an empty array will be returned
    '''
    plpts = plpts.replace(",0 ", ",").replace(",0", "")
    plpts_array = plpts.split(",")
    plpts = map(eval, plpts_array)
    poly = []
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
    return poly