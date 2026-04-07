import cv2
import numpy as np
import face_recognition
from deepface import DeepFace
from ultralytics import YOLO
import requests

class ASDDetector:
    def __init__(self):
        print("Loading YOLO model...")
        self.yolo = YOLO('yolov8n.pt')
        self.cap = cv2.VideoCapture(0)
        self.running = True
        self.current_emotion = "neutral"
        print("✅ YOLO model loaded")
        
    def detect_emotion(self, face_img):
        try:
            result = DeepFace.analyze(face_img, actions=['emotion'], enforce_detection=False)
            return result[0]['dominant_emotion']
        except:
            return "neutral"
    
    def detect_face(self, frame):
        face_locations = face_recognition.face_locations(frame)
        return face_locations
    
    def detect_objects(self, frame):
        results = self.yolo(frame)
        objects = []
        for r in results:
            if r.boxes is not None:
                for box in r.boxes:
                    class_id = int(box.cls[0])
                    class_name = self.yolo.names[class_id]
                    objects.append({'name': class_name, 'confidence': float(box.conf[0])})
        return objects
    
    def update_child_state(self, emotion, objects):
        try:
            requests.post('http://localhost:5001/api/update-child-state', 
                         json={'child': 'lam', 'emotion': emotion, 
                               'objects': [o['name'] for o in objects[:3]]}, timeout=1)
        except:
            pass
    
    def run(self):
        print("🔍 Detection started - Emotion, Face, Object Detection")
        print("   Press 'q' to stop")
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break
            face_locations = self.detect_face(frame)
            if face_locations:
                for (top, right, bottom, left) in face_locations:
                    face_img = frame[top:bottom, left:right]
                    if face_img.size > 0:
                        emotion = self.detect_emotion(face_img)
                        self.current_emotion = emotion
                        print(f"😊 Emotion: {emotion}")
            objects = self.detect_objects(frame)
            if objects:
                obj_names = [o['name'] for o in objects[:5]]
                print(f"📦 Objects: {obj_names}")
            self.update_child_state(self.current_emotion, objects)
            cv2.imshow('ASD Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    detector = ASDDetector()
    try:
        detector.run()
    except KeyboardInterrupt:
        print("\n🛑 Detection stopped")
