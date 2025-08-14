import os
import cv2
import numpy as np
import face_recognition
from PIL import Image

def validate_image(img_path):
    """Validate and convert image to proper format for face recognition"""
    try:
        # First check if file exists and is readable
        if not os.path.isfile(img_path):
            print(f"File not found: {img_path}")
            return None
            
        # Try with PIL first
        try:
            pil_img = Image.open(img_path)
            if pil_img.mode != 'RGB':
                pil_img = pil_img.convert('RGB')
            img_array = np.array(pil_img)
            
            if img_array.dtype != 'uint8':
                img_array = img_array.astype('uint8')
                
            return img_array
        except Exception as e:
            print(f"PIL processing failed for {img_path}: {str(e)}")
            
        # Fallback to OpenCV
        try:
            img = cv2.imread(img_path)
            if img is not None:
                return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        except Exception as e:
            print(f"OpenCV processing failed for {img_path}: {str(e)}")
            
    except Exception as e:
        print(f"General image validation error for {img_path}: {str(e)}")
        
    return None

def align_face(image):
    """Align face based on eye positions"""
    try:
        face_landmarks = face_recognition.face_landmarks(image)
        if face_landmarks:
            left_eye = face_landmarks[0]['left_eye']
            right_eye = face_landmarks[0]['right_eye']
            
            left_eye_center = np.mean(left_eye, axis=0).astype("int")
            right_eye_center = np.mean(right_eye, axis=0).astype("int")
            
            dy = right_eye_center[1] - left_eye_center[1]
            dx = right_eye_center[0] - left_eye_center[0]
            angle = np.degrees(np.arctan2(dy, dx))
            
            eyes_center = ((left_eye_center[0] + right_eye_center[0]) // 2,
                          (left_eye_center[1] + right_eye_center[1]) // 2)
            
            M = cv2.getRotationMatrix2D(eyes_center, angle, 1)
            aligned = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
            return aligned
    except Exception as e:
        print(f"Alignment error: {str(e)}")
    
    return image

def load_employee_encodings(data_dir='data'):
    """Load and process all employee face encodings"""
    encodings = []
    employees = []
    
    if not os.path.exists(data_dir):
        return [], []
    
    for emp_id in os.listdir(data_dir):
        emp_folder = os.path.join(data_dir, emp_id)
        if not os.path.isdir(emp_folder):
            continue
            
        emp_encodings = []
        valid_images = 0
        
        for img_name in os.listdir(emp_folder):
            if not img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
                
            img_path = os.path.join(emp_folder, img_name)
            img_array = validate_image(img_path)
            
            if img_array is None:
                continue
                
            try:
                aligned_img = align_face(img_array)
                face_encs = face_recognition.face_encodings(aligned_img)
                if face_encs:
                    emp_encodings.append(face_encs[0])
                    valid_images += 1
            except Exception as e:
                print(f"Error processing {img_path}: {str(e)}")
                continue
        
        if emp_encodings:
            avg_encoding = np.mean(emp_encodings, axis=0)
            encodings.append(avg_encoding)
            employees.append(emp_id)
            print(f"Loaded {valid_images} images for employee {emp_id}")
    
    return employees, encodings

def recognize_face(frame, known_encodings, known_ids, tolerance=0.5):
    """Recognize faces in a video frame"""
    try:
        # Convert and validate frame
        if len(frame.shape) == 3:  # Color image
            if frame.shape[2] == 3:  # BGR → RGB
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            elif frame.shape[2] == 4:  # BGRA → RGB
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
            else:  # Assume already RGB
                rgb = frame.copy()
        else:  # Grayscale
            rgb = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        
        # Ensure uint8
        if rgb.dtype != 'uint8':
            rgb = rgb.astype('uint8')

        face_locations = face_recognition.face_locations(rgb)
        face_encodings = face_recognition.face_encodings(rgb, face_locations)
        
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance)
            if True in matches:
                first_match_index = matches.index(True)
                return known_ids[first_match_index]
    except Exception as e:
        print(f"Recognition error: {str(e)}")
    
    return None