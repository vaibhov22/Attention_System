import cv2
import mediapipe as mp

class VisionSystem:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh()
        self.cap = cv2.VideoCapture(0)

        self.left_eye_indices = [33,160,158,133,153,144]
        self.right_eye_indices = [362,385,387,263,373,380]
        self.nose_index = 1

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, None

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)
        return frame, results

    def extract_landmarks(self, frame, face_landmarks):
        h, w, _ = frame.shape

        left_eye = []
        right_eye = []

        for idx in self.left_eye_indices:
            landmark = face_landmarks.landmark[idx]
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            left_eye.append((x, y))

        for idx in self.right_eye_indices:
            landmark = face_landmarks.landmark[idx]
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            right_eye.append((x, y))

        nose = face_landmarks.landmark[self.nose_index]
        nose_x = int(nose.x * w)
        nose_y = int(nose.y * h)

        return left_eye, right_eye, nose_x, nose_y, w

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()