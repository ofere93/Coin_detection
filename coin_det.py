import cv2
import bwLabel
import psColor
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.signal import argrelextrema





name = input('Insert the image name: ')
srcColor = cv2.imread(name)

src = cv2.imread(name,0)

nbins=256
v_range=[0,255]
hist=cv2.calcHist([src], [0], None, [nbins],v_range)
ind=np.arange(nbins)
width=3.0
#pl=plt.bar(ind,hist,width,color='green')
#plt.show()

val = np.where(hist == np.amax(hist,axis=0))
max=val[0]
max=max[0]
average=np.average(hist,axis=0)

min = argrelextrema(hist, np.less)
#print("max= ",max)
#print("mean= ",average)
#print("min= ",min)
val=hist[110]
val=val[0]
#print("hist: ",val)

minvec=min[0]
counter=range(0,len(minvec))
for i in counter:
	#print("minvec[i]= ",minvec[i])
	val=hist[minvec[i]]
	val=val[0]
	if(val<average and minvec[i]>max):
		val=minvec[i]
		break;
		
print("threshold value: ",val)
ret,thresh=cv2.threshold(src,val,255,cv2.THRESH_BINARY)
#cv2.imshow("Thresh",thresh)



kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(45,45))
morph=cv2.dilate(thresh,kernel)
#cv2.imshow("Morph_dilate1",morph)

kernel2=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(37,37))
morph=cv2.erode(morph,kernel2,iterations = 4)
#cv2.imshow("Morph_erode",morph)

kernel3=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(55,67))
morph=cv2.dilate(morph,kernel3)
#cv2.imshow("Morph_dilate2",morph)



lb,label=bwLabel.labeling(morph)
#print("\033[32mRegions: ",lb,"\033[37m") 
map=psColor.CreateColorMap(lb+1)
color=psColor.Gray2PseudoColor(label, map)
#cv2.imshow("colorMORPH",color)



im2, contourSeq, hierarchy=cv2.findContours(morph,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
#cv2.drawContours(srcColor,contourSeq,-1, (0,255,0), 2)


font                   = cv2.FONT_HERSHEY_SIMPLEX
fontScale              = 1
fontColor              = (0,255,255)
lineType               = 3

counter=range(0,lb)
distinct=0
coins=0
total=0

for i in counter:
	region=contourSeq[i]
	M = cv2.moments(region)
	Area=cv2.contourArea(region)
	cx = int(M['m10']/(M['m00']))
	cy = int(M['m01']/(M['m00']))
	r=math.sqrt(Area/math.pi)
	r=round(r,1)
	perimeter = cv2.arcLength(region,True)
	perimeter=round(perimeter,1)
	circularity=perimeter*perimeter/Area
	#print("Region: ",i+1,"Raggio: ",r," Area: ",Area," Perimeter: ",perimeter," Circularity: ", circularity)
	
	if(circularity<15.0):
		#1cent
		if(r>=34.9 and r<=38.4):
			position=(cx,cy)
			cv2.putText(srcColor,"1cent", position, font, fontScale, fontColor, lineType)
			coins=coins+1
			total=total+0.01
		
		#2cent
		elif(r>=45.4 and r<=47.7):
			position=(cx,cy)
			cv2.putText(srcColor,"2cent", position, font, fontScale, fontColor, lineType)
			coins=coins+1
			total=total+0.02
		
		#5cent
		elif(r>=52.7 and r<=55.3):
			position=(cx,cy)
			cv2.putText(srcColor,"5cent", position, font, fontScale, fontColor, lineType)
			coins=coins+1
			total=total+0.05
		
		#10cent
		elif(r>=47.8 and r<=51.7):
			position=(cx,cy)
			cv2.putText(srcColor,"10cent", position, font, fontScale, fontColor, lineType)
			coins=coins+1
			total=total+0.10
			
		#20cent
		elif(r>=56.3 and r<=60.2):
			position=(cx,cy)
			cv2.putText(srcColor,"20cent", position, font, fontScale, fontColor, lineType)
			coins=coins+1
			total=total+0.20
			
		#50cent
		elif(r>=64.9 and r<=67.9):
			position=(cx,cy)
			cv2.putText(srcColor,"50cent", position, font, fontScale, fontColor, lineType)
			coins=coins+1
			total=total+0.50
			
		#1euro
		elif(r>=60.3 and r<=64.8):
			position=(cx,cy)
			cv2.putText(srcColor,"1euro", position, font, fontScale, fontColor, lineType)
			coins=coins+1
			total=total+1.0
			

fontColor= (0,0,0)
position=(5,35)
lineType= 2
font= cv2.FONT_HERSHEY_COMPLEX
cv2.putText(srcColor,'Total value: %.2f' % total, position, font, fontScale, fontColor, lineType)
position=(5,75)
cv2.putText(srcColor,'Total coins: %d' % coins, position, font, fontScale, fontColor, lineType)		


cv2.imshow("contour",srcColor)

cv2.waitKey(0)
cv2.destroyAllWindows()
