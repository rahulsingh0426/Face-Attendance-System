import face_recognition
import cv2
import datetime
import pickle
import os
import database

def mark_attendance():
    if os.path.exists('encodings.pkl'):
        with open('encodings.pkl', 'rb') as f:
            known_encodings, known_names = pickle.load(f)
    else:
        known_encodings = []
        known_names = []

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = face_distances.argmin()
            if matches[best_match_index]:
                name = known_names[best_match_index]

            if name != "Unknown":
                now = datetime.datetime.now()
                date_string = now.strftime("%Y-%m-%d")
                time_string = now.strftime("%H:%M:%S")
                user_id = database.get_user_id(name)

                if user_id:
                    if not database.is_attendance_marked(user_id, date_string):
                        database.add_attendance(user_id, date_string, time_string)
                        cv2.putText(frame, f"Attendance marked for {name}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    else:
                        cv2.putText(frame, f"Attendance already marked for {name}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('Mark Attendance', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    mark_attendance()
