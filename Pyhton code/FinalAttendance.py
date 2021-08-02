import face_recognition
import cv2
import datetime
import wiotp.sdk.device
import time
import random
myConfig = { 
    "identity": {
        "orgId": "6teby0",
        "typeId": "attendance",
        "deviceId":"98765"
    },
    "auth": {
        "token": "W-027b0eRPv+Hg1@@f"
    }
}
def myCommandCallback(cmd):
    print("Message received from IBM IoT Platform: %s" % cmd.data['command'])
    print()
# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
chintu_image = face_recognition.load_image_file(r"C:\Users\DELL\Desktop\Attendance\chintu1.jpeg")
chintu_face_encoding = face_recognition.face_encodings(chintu_image)[0]

# Load a second sample picture and learn how to recognize it.
amrith_image = face_recognition.load_image_file(r"C:\Users\DELL\Desktop\Attendance\amrith1.jpeg")
amrith_face_encoding = face_recognition.face_encodings(amrith_image)[0]

ganesh_image = face_recognition.load_image_file(r"C:\Users\DELL\Desktop\Attendance\ganesh1.jpeg")
ganesh_face_encoding = face_recognition.face_encodings(ganesh_image)[0]

tanishq_image = face_recognition.load_image_file(r"C:\Users\DELL\Desktop\Attendance\tanishq1.jpg")
tanishq_face_encoding = face_recognition.face_encodings(tanishq_image)[0]

'''biden_image1 = face_recognition.load_image_file("nikhil.jpg")
biden_face_encoding1 = face_recognition.face_encodings(biden_image1)[0]'''

# Create arrays of known face encodings and their names
known_face_encodings = [
    chintu_face_encoding,
    amrith_face_encoding,
    ganesh_face_encoding,
    tanishq_face_encoding
]
known_face_names = [
    "chintu",
    "amrith",
    "ganesh",
    "tanishq"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
client.connect()
while True:
    # Grab a single frame of video
    cnt=0
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

       
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                #print(name)
            if name not in face_names:
                face_names.append(name)
        print(face_names)
        client.publishEvent(eventId="status", msgFormat="json", data=face_names, qos=0, onPublish=None)
        print("Published data Successfully: %s", face_names)
        time.sleep(2)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    
    # Display the resulting image
    cv2.imshow('Video', frame)
    cnt+=1
    if cnt >=3:
        break
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
