#code for face tracking

import cv2

HAAR_CASCADE_PATH = "haarcascade_frontalface_alt.xml"
CAMERA_INDEX = 1

def detect_faces(image):
	faces = []
	detected = cascade.detectMultiScale(image,1.3,4,cv2.cv.CV_HAAR_SCALE_IMAGE,(20,20))

	if detected!=[]:
		for (x,y,w,h) in detected: #for (x,y,w,h),n in detected:
			faces.append((x,y,w,h))
	return faces

def get_motion(face):
	#yaw is x-axis - horizontal axis
	#pitch is y-axis - depth axis
	#roll is z-axis - vertical axis

	#[0][0] - x, [0][1] - y, [0][2] - w, [0][3] - h

	#w,h are approx constant for U,D,L,R events
	#checking if w,h in range of origin(w,h)+/-5
	if (face[0][2]>(origin[0][2]-5)) and (face[0][2]<(origin[0][2]+5)) and (face[0][3]>(origin[0][3]-5)) and (face[0][3]<(origin[0][3]+5)):
		#possible events: UP, DOWN, LEFT, RIGHT
		""" do we support multi direction movement? If so, it'll be little more complicated. And I'm quite sure that this snippet I've written
		will be quite glitchy. Need to run it to know how to modify it. """
		#check x while y is same
		if face[0][1]>(origin[0][1]-5) and face[0][1]<(origin[0][1]+5):
			if face[0][0]>(origin[0][0]-5) and face[0][0]<(origin[0][0]+5):
				#user is in origin location
				print 'origin'
			else:
				if (face[0][0]-origin[0][0])>0:
					#LEFT motion event
					print 'LEFT'
				elif (face[0][0]-origin[0][0])<0:
					#RIGHT motion event
					print 'RIGHT'
		else:
			#check y while x is same
			if (face[0][1]-origin[0][1])>0:
				#DOWN motion event
				print 'DOWN'
			elif (face[0][1]-origin[0][1])<0:
				#UP motion event
				print 'UP'
	else:
		#possible events: Zoom in, Zoom out
		if (face[0][2]-origin[0][2])>0:
			#ZOOM IN motion event
			print 'ZOOM IN'
		elif (face[0][2]-origin[0][2])<0:
			#ZOOM OUT motion event
			print 'ZOOM OUT'

if __name__ == "__main__":
	cv2.namedWindow("Video")

	capture = cv2.VideoCapture(CAMERA_INDEX)
	cascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)
	faces = [] #var that stores face rect coords
	origin = [] #var that will store the origin coords

	i = 0
	c = -1
	ctr = 0 #for counting the no. of detections

	"""
	assuming that camera feed is at 24fps:
	facedetect/3 frames
	8 detections per second
	config phase - 2 secs - 16 detections - take avg to set origin
	"""

	while (c == -1):
		retval, image = capture.read()

		# Only run the Detection algorithm every 3 frames to improve performance
		if i%3==0:
			faces = detect_faces(image)
			print 'current coords',faces
			ctr += 1

		for (x,y,w,h) in faces:
			cv2.cv.Rectangle(cv2.cv.fromarray(image), (x,y), (x+w,y+h), 255)

		if ctr==20:
			#approx 3 secs of config time
			origin = faces
			print 'origin is ',origin

		if origin!=[] and faces!=[]:
			get_motion(faces)

		cv2.imshow("Video",image)
		i += 1
		c = cv2.waitKey(10)
		if(c==27):
			#escape
			break;
