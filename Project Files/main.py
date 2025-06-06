import os
import pickle
import cv2
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
#python image library
import threading
import openpyxl


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':"https://facerecognitionrealtime-9d7a8-default-rtdb.firebaseio.com/",
    'storageBucket': "facerecognitionrealtime-9d7a8.appspot.com"
})
bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
imgBackground = cv2.imread('Resources/background.png')

folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in modePathList]

print("loading encode file")
file = open('EncodeFile.p', 'rb')

encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print("Encode file loaded successfully")

modeType = 0
counter = 0
id = -1
imgStudent = []

wb = openpyxl.Workbook()
ws = wb.active
ws.append(["ID", "Name", "Total Attendance", "Last Attendance Time"])

last_attendance_time_dict = {}

def start_recognition():
    global imgBackground, modeType, counter, id, imgStudent

    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        imgBackground[162:162 + 480, 55:55 + 640] = img
        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

        if faceCurFrame:
            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1

                    imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                    id = studentIds[matchIndex]

                    # Check if attendance can be marked
                    if can_mark_attendance(id):
                        print(f"Attendance marked for ID: {id}")
                        cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                        cv2.imshow("Face Attendance", imgBackground)
                        cv2.waitKey(1)
                        counter = 1
                        modeType = 1

                        # Write attendance to Excel file
                        student_info = db.reference(f'Students/{id}').get()
                        datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        ws.append([id, student_info['name'], student_info['total_attendance'], datetime_now])
                        wb.save("attendance_record.xlsx")

                        # Update the last attendance time in the dictionary
                        last_attendance_time_dict[id] = datetime.now()

            if counter != 0:
                if counter == 1:
                    # Get the Data
                    studentInfo = db.reference(f'Students/{id}').get()
                    print(studentInfo)
                    # Get the Image from the storage
                    blob = bucket.get_blob(f'Images/{id}.png')
                    array = np.frombuffer(blob.download_as_string(), np.uint8)
                    imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                    # Update data of attendance
                    datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                       "%Y-%m-%d %H:%M:%S")
                    secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                    print(secondsElapsed)

                    if secondsElapsed > 36000:
                        ref = db.reference(f'Students/{id}')
                        student_info['total_attendance'] += 1

                        ref.child('total_attendance').set(student_info['total_attendance'])
                        ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        modeType = 3
                        counter = 0
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if modeType != 3:
                    if 10 < counter < 20:
                        modeType = 2

                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                    if counter <= 10:
                        cv2.putText(imgBackground, str(student_info['total_attendance']), (861, 125),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

                        cv2.putText(imgBackground, str(student_info['major']), (1006, 550),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                        cv2.putText(imgBackground, str(id), (1006, 493),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                        cv2.putText(imgBackground, str(student_info['standing']), (910, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)

                        cv2.putText(imgBackground, str(student_info['year']), (1025, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                        cv2.putText(imgBackground, str(student_info['starting_year']), (1125, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        (w, h), _ = cv2.getTextSize(student_info['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)

                        offset = (414 - w) // 2

                        cv2.putText(imgBackground, str(student_info['name']), (808 + offset, 445),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                        imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                    counter += 1

                    if counter >= 20:
                        counter = 0
                        modeType = 0
                        student_info = []
                        imgStudent = []
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
        else:
            modeType = 0
            counter = 0

        cv2.imshow("Face Attendance", imgBackground)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def update_gui():
    _, img = cap.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (640, 480))
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(image=img)

    label_webcam.imgtk = img
    label_webcam.configure(image=img)

    root.update()

    root.after(10, update_gui)

def close_face_recognition():
    global cap
    cap.release()
    root.destroy()


def can_mark_attendance(student_id):
    if student_id in last_attendance_time_dict:
        datetimeObject = last_attendance_time_dict[student_id]
        secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
        return secondsElapsed > 30
    else:
        return True


root = tk.Tk()
root.title("Face Recognition Attendance System by Arhan mansoori pvt.Ltd")
root.geometry("800x600")


label_webcam = tk.Label(root)
label_webcam.pack(padx=10, pady=10)


start_button = tk.Button(root, text="Start Recognition", command=lambda: threading.Thread(target=start_recognition).start())
start_button.pack(pady=10)


close_button = tk.Button(root, text="Close Face Recognition", command=close_face_recognition)
close_button.pack(pady=10)


root.after(10, update_gui) #10 milliseconds in loop
root.mainloop()
