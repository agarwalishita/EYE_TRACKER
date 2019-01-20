import numpy as np
import cv2
import time



cap = cv2.VideoCapture(0) 
def thresholding( value ):  
	global left_counter
	global right_counter
	
	if (value<=38):   
		print 'RIGHT'  
	elif(value>=70):  
		print 'LEFT'
	else:
		print 'CENTER'
while 1:
	ret, frame = cap.read()
	cv2.line(frame, (320,0), (320,480), (0,200,0), 2)
	cv2.line(frame, (0,200), (640,200), (0,200,0), 2)
	if ret==True:
		col=frame
		
		frame = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
		pupilFrame=frame
		clahe=frame
		blur=frame
		edges=frame
		eyes = cv2.CascadeClassifier('haarcascade_eye.xml')
		detected = eyes.detectMultiScale(frame, 1.3, 5)
		for (x,y,w,h) in detected: #similar to face detection
			cv2.rectangle(frame, (x,y), ((x+w),(y+h)), (0,0,255),1)	 #draw rectangle around eyes
			cv2.line(frame, (x,y), ((x+w,y+h)), (0,0,255),1)   #draw cross
			cv2.line(frame, (x+w,y), ((x,y+h)), (0,0,255),1)
			pupilFrame = cv2.equalizeHist(frame[int(y+(h*.25)):(y+h), x:(x+w)]) #using histogram equalization of better image. 
			cl1 = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)) #set grid size
			clahe = cl1.apply(pupilFrame)  #clahe
			blur = cv2.medianBlur(clahe, 7)  #median blur
			circles = cv2.HoughCircles(blur ,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=7,maxRadius=21) #houghcircles
			if circles is not None:
				#continue
				 #if atleast 1 is detected
				circles = np.round(circles[0, :]).astype("int") #change float to integer
				print 'integer',circles
				for (x,y,r) in circles:
					cv2.circle(pupilFrame, (x, y), r, (0, 255, 255), 2)
					cv2.rectangle(pupilFrame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
					#set thresholds
					thresholding(x)
		
		cv2.imshow('image',pupilFrame)
		#cv2.imshow('clahe', clahe)
		#cv2.imshow('blur', blur)
		if cv2.waitKey(1) & 0xFF == ord('q'):
	       	 break

cap.release()
cv2.destroyAllWindows()
