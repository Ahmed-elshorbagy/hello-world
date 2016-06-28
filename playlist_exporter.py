# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 14:03:42 2016

"""
def lst2dir(lst,dst): 
    lst=raw(str(lst))
    dst=raw(str(dst))
    n=lst.split(".")[-1]
    if n=="xspf":
        return xspf2dir(lst,dst)
    elif n=="m3u"or n=="m3u8":
        return m3u2dir(lst,dst)

escape_dict={'\a':r'\a',
           '\b':r'\b',
           '\c':r'\c',
           '\f':r'\f',
           '\n':r'\n',
           '\r':r'\r',
           '\t':r'\t',
           '\v':r'\v',
           '\'':r'\'',
           '\"':r'\"',
           '\0':r'\000',
'\1':r'\001',
'\2':r'\002',
'\3':r'\003',
'\4':r'\004',
'\5':r'\005',
'\6':r'\006'}

def raw(text):
    """Returns a raw string representation of text"""
    new_string=''
    for char in text:
        try: new_string+=escape_dict[char]
        except KeyError: new_string+=char
    return new_string
    
def xspf2dir(lst,dst):
    """exports tracks from xspf playlists to destination folder"""
    import shutil 
    import urllib
    import xml.etree.ElementTree as ET
    tree = ET.parse(lst)
    root = tree.getroot()
    
    s=[]
    for i in range(len( root[1])):
        s.append(root[1][i][0].text)
    z=[]
    for i in s:
        z.append(urllib.unquote_plus(i))
    for i in z:
        n=i.split("/")[-1]
        i.replace("/","\\")
        i=i.strip( 'file:///' )
        shutil.copy2(i, dst+"\\"+n)

def m3u2dir(lst,dst):
    """exports tracks from m3u or m3u8 playlists to destination folder"""
    import shutil 
    route = []

    for line in open(lst, 'r'):
        route.append(line.strip().split('>')) 
    z=route[2::2]
    for i in z:
        n=i[0].split("\\")[-1]
        shutil.copy2(i[0], dst+"\\"+n)
