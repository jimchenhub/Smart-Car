# -*- coding: utf-8 -*-
import numpy as np
from xml.dom import minidom
from xml.etree import ElementTree as ET

def createXML( path, ret_val, mtx1_val, dist1_val, mtx2_val, dist2_val, R_val, T_val, E_val, F_val):
    doc=minidom.Document()
    root = doc.createElement('root')
    ret = doc.createElement('ret')
    ret.appendChild(doc.createTextNode(str(ret_val)))
    root.appendChild(ret)
    mtx1 = doc.createElement('mtx1')
    mtx1.appendChild(doc.createTextNode(str(mtx1_val)))
    root.appendChild(mtx1)
    mtx2 = doc.createElement('mtx2')
    mtx2.appendChild(doc.createTextNode(str(mtx2_val)))
    root.appendChild(mtx2)
    dist1 = doc.createElement('dist1')
    dist1.appendChild(doc.createTextNode(str(dist1_val)))
    root.appendChild(dist1)
    dist2 = doc.createElement('dist2')
    dist2.appendChild(doc.createTextNode(str(dist2_val)))
    root.appendChild(dist2)
    R = doc.createElement('R')
    R.appendChild(doc.createTextNode(str(R_val)))
    root.appendChild(R)
    T = doc.createElement('T')
    T.appendChild(doc.createTextNode(str(T_val)))
    root.appendChild(T)
    E = doc.createElement('E')
    E.appendChild(doc.createTextNode(str(E_val)))
    root.appendChild(E)
    F = doc.createElement('F')
    F.appendChild(doc.createTextNode(str(F_val)))
    root.appendChild(F)
    doc.appendChild(root)
    f = open(path, 'w')
    f.write(doc.toprettyxml(indent = ''))

def parseXML(path):
    root = ET.parse(path)
    ret_str = root.find('ret').text
    mtx1_str = root.find('mtx1').text
    dist1_str = root.find('dist1').text
    mtx2_str = root.find('mtx2').text
    dist2_str = root.find('dist2').text
    R_str = root.find('R').text
    T_str = root.find('T').text
    E_str = root.find('E').text
    F_str = root.find('F').text
    ret = float(ret_str)
    mtx1 = str2mat(mtx1_str)
    dist1 = str2mat(dist1_str)
    mtx2 = str2mat(mtx2_str)
    dist2 = str2mat(dist2_str)
    R = str2mat(R_str)
    T = str2mat(T_str)
    E = str2mat(E_str)
    F = str2mat(F_str)
    return \
        {'ret':ret, 'mtx1':mtx1, 'dist1':dist1,
         'mtx2':mtx2, 'dist2':dist2,
         'R':R, 'T':T, 'E':E, 'F':F,
         }

def str2mat(list_str):
    list_str = list_str.strip('[]')
    list_str = list_str.replace(']',';')
    list_str = list_str.replace('[','')
    mat = np.matrix(list_str)
    return mat

