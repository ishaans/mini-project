#headtracking code that performs 3D transformations of a cube using head movement
#uses facetrack.py + displayWireframe3.py

#!/bin/env python


import cv2
import wireframe3 as wireframe
import pygame

HAAR_CASCADE_PATH = "haarcascade_frontalface_alt.xml"
CAMERA_INDEX = 1
matrix = [[[0 for x in xrange(4)] for x in xrange(1)] for x in xrange(20)]
matrix1 = [[[0 for x in xrange(4)] for x in xrange(1)] for x in xrange(1)]
matrix1[0][0][0] = 0
matrix1[0][0][1] = 0
matrix1[0][0][2] = 0
matrix1[0][0][3] = 0
a = 0

key_to_function = {
	0:   (lambda x: x.translateAll('x', -a)),
	1:  (lambda x: x.translateAll('x',  a)),
	2:   (lambda x: x.translateAll('y',  a)),
	3:     (lambda x: x.translateAll('y', -a)),
	4: (lambda x: x.scaleAll(a)),
	5:  (lambda x: x.scaleAll( a)),
	6:      (lambda x: x.rotateAll('X',  0.1)),
	7:      (lambda x: x.rotateAll('X', -0.1)),
	8:      (lambda x: x.rotateAll('Y',  0.1)),
	9:      (lambda x: x.rotateAll('Y', -0.1)),
	10:      (lambda x: x.rotateAll('Z',  0.1)),
	11:      (lambda x: x.rotateAll('Z', -0.1)) }

def detect_faces(image):
	faces = []
	detected = cascade.detectMultiScale(image,1.3,4,cv2.cv.CV_HAAR_SCALE_IMAGE,(20,20))

	if detected!=[]:
		for (x,y,w,h) in detected: #for (x,y,w,h),n in detected:
			faces.append((x,y,w,h))
	return faces


def get_motion(f_x,f_y,f_wid):
	#yaw is x-axis - horizontal axis
	#pitch is y-axis - depth axis
	#roll is z-axis - vertical axis

	#[0][0] - x, [0][1] - y, [0][2] - w, [0][3] - h
	
	#w,h are approx constant for U,D,L,R events
	#checking if w,h in range of origin(w,h)+/-5
	if (f_wid>(o_wid-20)) and (f_wid<(o_wid+20)):
		#possible events: UP, DOWN, LEFT, RIGHT
		""" do we support multi direction movement? If so, it'll be little more complicated. And I'm quite sure that this snippet I've written
		will be quite glitchy. Need to run it to know how to modify it. """
		#check x while y is same
	
		
		if f_y>(o_y-5) and f_y<(o_y+5):
			if f_x>(o_x-5) and f_x<(o_x+5):
				#user is in origin location
				print 'origin'
				return 25 #no motion
			else:
				if (f_x-o_x)>0:
					#LEFT motion event - S button
					print 'LEFT', a
					return 0
				elif (f_x-o_x)<0:
					#RIGHT motion event - A button
					print 'RIGHT', f_x-o_x
					return 1
		else:
			#check y while x is same
			if (f_y-o_y)>0:
				#DOWN motion event - Q button
				print 'DOWN'
				return 2
			elif (f_y-o_y)<0:
				#UP motion event - W button
				print 'UP'
				return 3
	else:
			#possible events: Zoom in, Zoom out
		if (f_wid-o_wid)>0:
			#ZOOM IN motion event - = button
			print 'ZOOM IN'
			return 4
		elif (f_wid-o_wid)<0:
			#ZOOM OUT motion event - -button
			print 'ZOOM OUT'
			return 5

class ProjectionViewer:
	""" Displays 3D objects on a Pygame screen """

	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption('Wireframe Display')
		self.background = (10,10,50)

		self.wireframes = {}
		self.displayNodes = True
		self.displayEdges = True
		self.nodeColour = (255,255,255)
		self.edgeColour = (200,200,200)
		self.nodeRadius = 4

	def addWireframe(self, name, wireframe):
		""" Add a named wireframe object. """

		self.wireframes[name] = wireframe

	def run(self):
		""" Create a pygame screen until it is closed. """

		running = True
		while running:
			retval, image = capture.read()

			global i, ctr, origin, faces, t, o_x, o_y, o_wid, a

			# Only run the Detection algorithm every 3 frames to improve performance
			for (x,y,w,h) in matrix1[0]:
				cv2.cv.Rectangle(cv2.cv.fromarray(image), (x,y), (x+w,y+h), 0)
			if i%3==0:
				faces = detect_faces(image)
				print 'current coords',faces
				
			if faces != []:
				if ctr < 20:
					matrix [ctr][0][0] = faces[0][0]
					matrix [ctr][0][1] = faces[0][1]
					matrix [ctr][0][2] = faces[0][2]
					matrix [ctr][0][3] = faces[0][3]
					print 'currentvalue and frame:', matrix [ctr], ctr
		   			ctr += 1
		   		if ctr==20:
					#approx 3 secs of config time
					for t in xrange(ctr):
						matrix1 [0][0][0] = matrix1[0][0][0] + matrix[t][0][0]
						matrix1 [0][0][1] = matrix1[0][0][1] + matrix[t][0][1]
						matrix1 [0][0][2] = matrix1[0][0][2] + matrix[t][0][2]
						matrix1 [0][0][3] = matrix1[0][0][3] + matrix[t][0][3]
					matrix1[0][0][0]= matrix1[0][0][0]/20
					matrix1[0][0][1]= matrix1[0][0][1]/20
					matrix1[0][0][2]= matrix1[0][0][2]/20
					matrix1[0][0][3]= matrix1[0][0][3]/20
					o_x = (matrix1[0][0][0] + matrix1[0][0][2])/2
					o_y = (matrix1[0][0][1] + matrix1[0][0][3])/2
					o_wid = matrix1[0][0][2]
					print 'origin is ',matrix1, o_x, o_y, o_wid
		   			ctr += 1

			for (x,y,w,h) in matrix1[0]:
				cv2.cv.Rectangle(cv2.cv.fromarray(image), (x,y), (x+w,y+h), 0)

			for (x,y,w,h) in faces:
				cv2.cv.Rectangle(cv2.cv.fromarray(image), (x,y), (x+w,y+h), 255)



			if o_x!= 0 and faces!=[]:
				f_x = (faces[0][0] + faces[0][2])/2
				f_y = (faces[0][1] + faces[0][3])/2
				f_wid = faces[0][2]
				dir = get_motion(f_x,f_y,f_wid)
				if (dir == 0 or dir == 1):
					a = (f_x-o_x)/float(10)
					round(a)
				elif (dir == 2 or dir == 3):
					a = (f_y-o_y)/float(10)
					round(a)
				elif (dir == 4 or dir == 5):
					a = (f_wid-o_wid)/float(30)
					round(a)
				else:
					print 'nothing.'
					a=0
				print 'direction vector',dir
				if dir in key_to_function:
					key_to_function[dir](self)
				print 'value:', a

			cv2.imshow("Video",image)
			i += 1
			if i>100:
				i=0
			c = cv2.waitKey(10)

			if c==27:
				break
			
			self.display()
			pygame.display.flip()
		
	def display(self):
		""" Draw the wireframes on the screen. """

		self.screen.fill(self.background)

		for wireframe in self.wireframes.values():
			if self.displayEdges:
				for edge in wireframe.edges:
					pygame.draw.aaline(self.screen, self.edgeColour, (edge.start.x, edge.start.y), (edge.stop.x, edge.stop.y), 1)

			if self.displayNodes:
				for node in wireframe.nodes:
					pygame.draw.circle(self.screen, self.nodeColour, (int(node.x), int(node.y)), self.nodeRadius, 0)

	def translateAll(self, axis, d):
		""" Translate all wireframes along a given axis by d units. """

		for wireframe in self.wireframes.itervalues():
			wireframe.translate(axis, d)

	def scaleAll(self, scale):
		""" Scale all wireframes by a given scale, centred on the centre of the screen. """

		centre_x = self.width/2
		centre_y = self.height/2

		for wireframe in self.wireframes.itervalues():
			wireframe.scale((centre_x, centre_y), scale)

	def rotateAll(self, axis, theta):
		""" Rotate all wireframe about their centre, along a given axis by a given angle. """

		rotateFunction = 'rotate' + axis

		for wireframe in self.wireframes.itervalues():
			centre = wireframe.findCentre()
			getattr(wireframe, rotateFunction)(centre, theta)

if __name__ == '__main__':
	pv = ProjectionViewer(640, 480)

	cube = wireframe.Wireframe()
	cube.addNodes([(x,y,z) for x in (50,250) for y in (50,250) for z in (50,250)])
	cube.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])

	cv2.namedWindow("Video",400)

	capture = cv2.VideoCapture(CAMERA_INDEX)
	cascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)
	faces = [] #var that stores face rect coords
	origin = [] #var that will store the origin coords
	o_x = 0
	o_y = 0
	o_wid = 0
	a = 0

	i = 0
	c = -1
	ctr = 0 #for counting the no. of detections
	t = 0
	
	pv.addWireframe('cube', cube)
	pv.run()
