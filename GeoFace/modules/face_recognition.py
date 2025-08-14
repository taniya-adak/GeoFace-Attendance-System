import cv2
import face_recognition
import os
from datetime import datetime

def register_face(name):
    """Register a new employee face"""
    os.makedirs("faces", exist_ok=True)
    cap = cv2.VideoCapture(0)
    
    print(f"Press 'S' to capture {name}'s face...")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        cv2.imshow(f"Register {name} (Press 'S')", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('s'):
            rgb_frame = frame[:, :, ::-1]  # Convert BGR to RGB
            face_locations = face_recognition.face_locations(rgb_frame)
            
            if face_locations:
                top, right, bottom, left = face_locations[0]
                face_img = frame[top:bottom, left:right]
                
                img_path = f"faces/{name.lower().replace(' ', '_')}.jpg"
                cv2.imwrite(img_path, face_img)
                print(f"Face saved to {img_path}")
                break
    
    cap.release()
    cv2.destroyAllWindows()
    return img_path

def recognize_face():
    """Recognize faces and return matches"""
    known_faces = []
    known_names = []
    
    # Load registered faces
    for img_file in os.listdir("faces"):
        name = os.path.splitext(img_file)[0].replace('_', ' ')
        img_path = os.path.join("faces", img_file)
        img = face_recognition.load_image_file(img_path)
        encoding = face_recognition.face_encodings(img)[0]
        known_faces.append(encoding)
        known_names.append(name)
    
    return known_faces, known_names

def detect_faces(known_faces, known_names):
    """Detect and recognize faces in real-time"""
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        rgb_frame = frame[:, :, ::-1]  # BGR to RGB
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.6)
            name = "Unknown"
            
            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]
            
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        cv2.imshow("Face Recognition", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()