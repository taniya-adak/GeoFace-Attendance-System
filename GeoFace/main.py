import cv2
import face_recognition  # Add this import
from modules.face_recognition import recognize_face
from modules.geolocation import get_current_location
from modules.database import add_attendance_record
import os

def main():
    # Initialize face recognition
    known_faces, known_names = recognize_face()
    
    # Initialize camera
    cap = cv2.VideoCapture(0)
    
    print("Press 'A' to mark attendance when face is detected")
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
                
                # Draw rectangle and name
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            # Mark attendance on 'A' key press
            if cv2.waitKey(1) & 0xFF == ord('a') and name != "Unknown":
                location = get_current_location()
                if location:
                    img_path = f"faces/{name.lower().replace(' ', '_')}.jpg"
                    add_attendance_record(
                        name=name,
                        lat=location["latitude"],
                        lon=location["longitude"],
                        place=location["place"],
                        img_path=img_path
                    )
                    print(f"Attendance marked for {name} at {location['place']}")
        
        cv2.imshow("Face Recognition Attendance", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()