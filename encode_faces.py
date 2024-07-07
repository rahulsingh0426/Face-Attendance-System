# encode_faces.py
import face_recognition
import os
import pickle

def encode_known_faces():
    known_faces_dir = 'images/known_faces'
    known_encodings = []
    known_names = []

    for name in os.listdir(known_faces_dir):
        for filename in os.listdir(f"{known_faces_dir}/{name}"):
            image = face_recognition.load_image_file(f"{known_faces_dir}/{name}/{filename}")
            encoding = face_recognition.face_encodings(image)[0]
            known_encodings.append(encoding)
            known_names.append(name)

    with open('encodings.pkl', 'wb') as f:
        pickle.dump((known_encodings, known_names), f)

if __name__ == "__main__":
    encode_known_faces()
