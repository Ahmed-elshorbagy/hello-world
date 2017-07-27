import cv2
import numpy as np
np.seterr(over='ignore')
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join
#open the image and split color channels
img = cv2.imread('asd.jpg')
b,g,r = cv2.split(img)
b=np.array(b)
g=np.array(g)
r=np.array(r)
##    
##  making histogram equlization for color channels and merging them again   
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
b=clahe.apply(b)
b=clahe.apply(b)
g= clahe.apply(g)
r= clahe.apply(r)
r= clahe.apply(r)
g= clahe.apply(g)
r= clahe.apply(r)
b=clahe.apply(b)
g= clahe.apply(g)
dd= cv2.merge((b,g,r))

##color detection :)
hsv = cv2.cvtColor(dd, cv2.COLOR_BGR2HSV)
h,s,v=cv2.split(hsv)
s=np.array(s)

s[s < 255] = 255
hsv= cv2.merge((h,s,v))
dd=cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
# define range of green color in HSV
lower_green = np.array([50,80,0])
upper_green = np.array([255,255,40])
# Threshold the HSV image to get only blue colors
mask = cv2.inRange(dd, lower_green, upper_green)
# Bitwise-AND mask and original image
dst1 = cv2.bitwise_and(dd,dd, mask= mask)
#    
dst2 = cv2.dilate(dst1,np.ones((5,5),np.uint8),iterations = 1)
kernel = np.ones((5,5),np.uint8)
rows,cols,channels = img.shape
roi = img[0:rows, 0:cols ]
k2= np.ones((7,7),np.uint8)
#smooth the grainsof selected color
dst = cv2.morphologyEx(dst2, cv2.MORPH_OPEN, kernel)
dst = cv2.morphologyEx(dst, cv2.MORPH_CLOSE, kernel)
dst = cv2.morphologyEx(dst, cv2.MORPH_OPEN, kernel)
dst = cv2.morphologyEx(dst, cv2.MORPH_CLOSE, kernel)
dst = cv2.morphologyEx(dst, cv2.MORPH_OPEN, k2)
dst = cv2.morphologyEx(dst, cv2.MORPH_CLOSE, kernel)
dst3 = cv2.morphologyEx(dst, cv2.MORPH_OPEN, k2)
#    
#creating color mask on the original image    
gr = cv2.cvtColor(dst3, cv2.COLOR_BGR2GRAY)

ret, maskgr = cv2.threshold(gr, 0, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(maskgr)
img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
img2_fg = cv2.bitwise_and(dst3,dst3,mask = maskgr)

fin_dst = cv2.add(img1_bg,img2_fg)
#making final image side by side the original
fin=np.hstack((img,fin_dst))
    
cv2.imwrite('clahe_2.jpg',fin)
