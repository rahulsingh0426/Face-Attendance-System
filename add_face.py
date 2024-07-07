import os
import cv2
import face_recognition
import pickle
import shutil
import database  # Import database module to use its functions

def add_face(name):
    known_faces_dir = 'images/known_faces'
    if not os.path.exists(known_faces_dir):
        os.makedirs(known_faces_dir)

    user_dir = os.path.join(known_faces_dir, name)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('Add Face', frame)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.imwrite(os.path.join(user_dir, f'{name}.jpg'), frame)
            break
    cap.release()
    cv2.destroyAllWindows()

    if os.path.exists('encodings.pkl'):
        with open('encodings.pkl', 'rb') as f:
            known_encodings, known_names = pickle.load(f)
    else:
        known_encodings = []
        known_names = []

    image_path = os.path.join(user_dir, f'{name}.jpg')
    image = face_recognition.load_image_file(image_path)
    face_encoding = face_recognition.face_encodings(image)[0]

    known_encodings.append(face_encoding)
    known_names.append(name)

    with open('encodings.pkl', 'wb') as f:
        pickle.dump((known_encodings, known_names), f)

    database.add_user(name)

def clear_faces_and_data():
    known_faces_dir = 'images/known_faces'
    if os.path.exists(known_faces_dir):
        shutil.rmtree(known_faces_dir)
    os.makedirs(known_faces_dir)
    
    encodings_file = 'encodings.pkl'
    if os.path.exists(encodings_file):
        os.remove(encodings_file)

    database.clear_database()  # Clear the database

if __name__ == "__main__":
    name = input("Enter the name of the person: ")
    add_face(name)
