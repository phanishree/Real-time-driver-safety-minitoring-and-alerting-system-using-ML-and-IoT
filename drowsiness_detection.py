from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2

#infinitely capture video


#phani
#connect to web cab
#capture frame


#rach
#detect face
#detect eye - coordinates

#tarun
#calculate ear - 

#hafsa
#count frames 
#ring the alarm

# dlib 
detect = dlib.get_frontal_face_detector()

predict = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")

# fetching the index of the facial landmarks of the left eye and right eye encoded in face utils 

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]


def getFaces():
  video_stream=cv2.VideoCapture(0)
  # grab the frame from the threaded video file stream, resize
	# it, and convert it to grayscale
	# channels)
  
	ret, frame=video_stream.read()
  global frame
	frame = imutils.resize(frame, width=450)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	return detect(gray, 0),gray
  
#calculates ear and draws contours for eyes in each given frame

def calculateEar(subject,gray):
  	shape = predict(gray, subject)
		shape = face_utils.shape_to_np(shape)#converting to NumPy Array
		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]
		leftEAR = eye_aspect_ratio(leftEye)
		rightEAR = eye_aspect_ratio(rightEye)
		ear = (leftEAR + rightEAR) / 2.0
		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)
		cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
    return ear


flag=0

#continuously loop over frames from the video stream
while True:

  subjects,gray = getFaces()

  #loop over the face detections
	for subject in subjects:
  
    ear = calculateEar(gray,subject)

		if ear < thresh:
			flag += 1
			print (flag)
			if flag >= frame_check:
				print ("Drowsy")
		else:
			flag = 0
      
      
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break
cv2.destroyAllWindows()
cap.release() 
