#!/usr/bin/env python
import sys
import os
import numpy as np
from face_recognition_system.videocamera import VideoCamera
from face_recognition_system.detectors import FaceDetector
import face_recognition_system.operations as op
import cv2
from sklearn.ensemble import VotingClassifier
from cv2 import __version__
import DAO

students={}
students=set(students)

def get_images(frame, faces_coord, shape):
    
    faces_img = op.cut_face_rectangle(frame, faces_coord)
    frame = op.draw_face_rectangle(frame, faces_coord)
    faces_img = op.normalize_intensity(faces_img)
    faces_img = op.resize(faces_img)
    return (frame, faces_img)

def add_person(people_folder, shape):

    person_name = input('Please give the name of the new person: ').lower()
    folder = people_folder + person_name
    if not os.path.exists(folder):
        input("Press ENTER when ready.")
        os.mkdir(folder)
        video = VideoCamera()
        detector = FaceDetector('face_recognition_system/frontal_face.xml')
        counter = 1
        timer = 0
        cv2.namedWindow('Video Feed', cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow('Saved Face', cv2.WINDOW_NORMAL)
        while counter < 21:
            frame = video.get_frame()
            face_coord = detector.detect(frame)
            if len(face_coord):
                frame, face_img = get_images(frame, face_coord, shape)
                # save a face every second, we start from an offset '5' because
                # the first frame of the camera gets very high intensity
                # readings.
                if timer % 100 == 5:
                    cv2.imwrite(folder + '/' + str(counter) + '.jpg',
                                face_img[0])
                    print ('Images Saved:' + str(counter))
                    counter += 1
                    cv2.imshow('Saved Face', face_img[0])

            cv2.imshow('Video Feed', frame)
            cv2.waitKey(50)
            timer += 5
    else:
        print ("This name already exists.")
        sys.exit()

def recognize_people(people_folder, shape):
    
    try:
        people = [person for person in os.listdir(people_folder)]
    except:
        print ("Have you added at least one person to the system?")
        sys.exit()
    print ("This are the people in the Recognition System:")
    for person in people:
        print ("-" + person)
    print ("   POSSIBLE RECOGNIZERS TO USE")
    print ("1. EigenFaces")
    print ("2. FisherFaces")
    print ("3. LBPHFaces")

    choice = check_choice()

    detector = FaceDetector('face_recognition_system/frontal_face.xml')
    if choice == 1:
        recognizer = cv2.face.EigenFaceRecognizer_create()
        threshold = 4000
    elif choice == 2:
        recognizer = cv2.face.FisherFaceRecognizer_create()
        threshold = 300
    elif choice == 3:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        threshold = 105
        #recognizer=VotingClassifier([('eigen',recognizer1),('lbph',recognizer2),('fisher',recognizer3)],voting='soft')	
		
    images = []
    labels = []
    labels_people = {}
    for i, person in enumerate(people):
        labels_people[i] = person
        for image in os.listdir(people_folder + person):
            images.append(cv2.imread(people_folder + person + '/' + image, 0))
            labels.append(i)
    try:
        #print("printing images"+"   "+"  "+str(images))
        #print("printing labesl"+"   "+"  "+str(labels)+"   "+str(np.array(labels)))
        recognizer.train(images, np.array(labels))
    except:
        print ("\nOpenCV Error: Do you have at least two people in the database?\n")
        sys.exit()

    video = VideoCamera()
    while True:
        frame = video.get_frame()
        faces_coord = detector.detect(frame, False)
        if len(faces_coord):
            frame, faces_img = get_images(frame, faces_coord, shape)
            for i, face_img in enumerate(faces_img):
                #if __version__ == "3.1.0":
                global students
                collector = cv2.face.StandardCollector_create()
                #recognizer.predict(face_img)
                #conf = collector.getDist()
                #pred = collector.getLabel()
		#print ("Prediction: " +pred)
                #else:
                pred, conf = recognizer.predict(face_img)
                print ("Prediction: " + str(pred))
                students.add(pred)
                print(students)
                print ('Confidence: ' + str(round(conf)))
                print ('Threshold: ' + str(threshold))
                if conf < threshold:
                    cv2.putText(frame, labels_people[pred].capitalize(),
                                (faces_coord[i][0], faces_coord[i][1] - 2),
                                cv2.FONT_HERSHEY_PLAIN, 1.7, (206, 0, 209), 2,
                                cv2.LINE_AA)
                else:
                    cv2.putText(frame, "Unknown",
                                (faces_coord[i][0], faces_coord[i][1]),
                                cv2.FONT_HERSHEY_PLAIN, 1.7, (206, 0, 209), 2,
                                cv2.LINE_AA)

        cv2.putText(frame, "ESC to exit", (5, frame.shape[0] - 5),
                    cv2.FONT_HERSHEY_PLAIN, 1.2, (206, 0, 209), 2, cv2.LINE_AA)
        cv2.imshow('Video', frame)
        if cv2.waitKey(100) & 0xFF == 27:

            dao=DAO(students)
            dao.dbOperations()
            print("*******************************Attendence Updated ****************************")
            #dao.__del__()
            sys.exit()

def check_choice():
    is_valid = 0
    while not is_valid:
        try:
            choice = int(input('Enter your choice [1-3] : '))
            if choice in [1, 2, 3]:
                is_valid = 1
            else:
                print ("'%d' is not an option.\n" % choice)
        except ValueError:
            print ("%s is not an option.\n" % str(error).split(": ")[1])
    return choice

if __name__ == '__main__':
    
    print ("   POSSIBLE ACTIONS")
    print ("1. Add person to the recognizer system")
    print ("2. Start recognizer")
    print ("3. Exit")

    CHOICE = check_choice()

    PEOPLE_FOLDER = "face_recognition_system/people/"
    SHAPE = "rectangle"

    if CHOICE == 1:
        if not os.path.exists(PEOPLE_FOLDER):
            os.makedirs(PEOPLE_FOLDER)
        add_person(PEOPLE_FOLDER, SHAPE)
    elif CHOICE == 2:
        recognize_people(PEOPLE_FOLDER, SHAPE)
    elif CHOICE == 3:
        sys.exit()
