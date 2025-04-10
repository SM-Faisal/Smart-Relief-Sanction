import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facerecognitionrealtime-9d7a8-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "1903167":
        {
            "name": "S. M. Faisal",
            "major": "Event-1",
            "starting_year": 2023,
            "total_attendance": 0,
            "standing": "0",
            "year": 0,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "133061":
        {
            "name": "Md. Zahirul Islam",
            "major": "Event-1",
            "starting_year": 2023,
            "total_attendance": 0,
            "standing": "0",
            "year": 0,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1903010":
        {
            "name": "Emly Blunt",
            "major": "Event-1",
            "starting_year": 2023,
            "total_attendance": 0,
            "standing": "0",
            "year": 0,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1903020":
        {
            "name": "Elon Musk",
            "major": "Event-1",
            "starting_year": 2023,
            "total_attendance": 0,
            "standing": "0",
            "year": 0,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1903030":
        {
            "name": "Anamul Haque",
            "major": "Event-1",
            "starting_year": 2023,
            "total_attendance": 0,
            "standing": "0",
            "year": 0,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1903040":
        {
            "name": "Sakib Al Hasan",
            "major": "Event-1",
            "starting_year": 2023,
            "total_attendance": 0,
            "standing": "0",
            "year": 0,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1903050":
        {
            "name": "Towhid Hridoy",
            "major": "Event-1",
            "starting_year": 2023,
            "total_attendance": 0,
            "standing": "0",
            "year": 0,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1903060":
        {
            "name": "Mark Zuckerberg",
            "major": "Event-1",
            "starting_year": 2023,
            "total_attendance": 0,
            "standing": "0",
            "year": 0,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1903070":
        {
            "name": "Christiano Ronaldo",
            "major": "Event-1",
            "starting_year": 2023,
            "total_attendance": 0,
            "standing": "0",
            "year": 0,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1903080":
        {
            "name": "Lionel Messi",
            "major": "Event-1",
            "starting_year": 2023,
            "total_attendance": 0,
            "standing": "0",
            "year": 0,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1903090":
        {
            "name": "Neymar Jr",
            "major": "Event-1",
            "starting_year": 2023,
            "total_attendance": 0,
            "standing": "0",
            "year": 0,
            "last_attendance_time": "2022-12-11 00:54:34"
        }
}

for key, value in data.items():
    ref.child(key).set(value)