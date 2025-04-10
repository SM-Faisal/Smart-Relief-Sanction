# Smart Relief Sanction

**Smart Relief Sanction** is a real-time face recognition system developed using **OpenCV** in **PyCharm**. It helps ensure accurate and transparent relief distribution in rural areas by verifying individuals' faces against a National ID (NID) database using Firebase Realtime Database and Storage.

---

## 🔍 Features

- Real-time face recognition using webcam and OpenCV
- Firebase integration for secure NID verification and attendance logging
- Tkinter-based GUI for user interaction
- Attendance record logging in Excel (.xlsx)
- Automatic prevention of duplicate entries within a short time window
- Beautiful UI with status display (Loading, Verified, etc.)

---

## 🛠️ Tech Stack

- **Python**
- **OpenCV**
- **face_recognition**
- **Firebase (Realtime DB + Storage)**
- **Tkinter**
- **cvzone**
- **openpyxl**
- **PyCharm IDE**

---

## 📁 Project Structure
SmartReliefSanction/ │ ├── .idea/ # PyCharm project settings ├── Images/ # Folder for storing captured images ├── Resources/ # Background images & mode UIs ├── venv/ # Python virtual environment │ ├── AddDataToDatabase.py # Script to add user data to Firebase ├── EncodeFile.p # Pickle file storing face encodings ├── EncodeGenerator.py # Script to generate face encodings ├── main.py # Main face recognition & GUI logic ├── serviceAccountKey.json # Firebase service account credentials ├── attendance_record.xlsx # Output Excel sheet with logs


## 🚀 How to Run

1. Clone the repository and open in **PyCharm**.
2. Install the required packages:
   ```bash
   pip install opencv-python face_recognition firebase-admin cvzone openpyxl pillow
3. Place your Firebase serviceAccountKey.json in the root directory.
4. Make sure your Firebase Realtime Database and Storage are properly set up.
5. Run EncodeGenerator.py to generate encodings from Firebase images.
6. Run main.py to launch the GUI and start face recognition.


## 📦 Output
Excel file with:

- ID  
- Name  
- Total Attendance  
- Last Attendance Time  

GUI with webcam feed and recognition status overlays

---

## 👨‍💻 Developed By
**Arhan Mansoori Pvt. Ltd.**

---

## 🧠 Use Case
This system ensures that relief or aid is only distributed to verified individuals in rural areas, reducing fraud and ensuring proper distribution through biometric authentication.

---

## 📷 Screenshot
*(Ensure the image file is named `image.png` and placed in the root folder)*

---

## 📜 License
This project is for educational and nonprofit use.
