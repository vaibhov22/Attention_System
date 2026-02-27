import numpy as np
import time

class FeatureExtractor:
    def __init__(self):
        self.blink_count = 0
        self.blink_frames = 0
        self.distraction_frames = 0
        self.closed_start_time = None
        self.distraction_start_time = None
        self.fatigue_events = 0

    def euclidean(self, p1, p2):
        return np.linalg.norm(np.array(p1) - np.array(p2))

    def calculate_EAR(self, eye):
        A = self.euclidean(eye[1], eye[5])
        B = self.euclidean(eye[2], eye[4])
        C = self.euclidean(eye[0], eye[3])

        if C < 1e-6:
            return 0

        return (A + B) / (2.0 * C)

    def detect_blink(self, EAR):
        if EAR < 0.22:
            self.blink_frames += 1
        else:
            if self.blink_frames > 4:
                self.blink_count += 1
            self.blink_frames = 0

        return self.blink_count

    def detect_distraction(self, nose_x, frame_width):
        frame_center_x = frame_width // 2
        deviation = nose_x - frame_center_x

        if abs(deviation) > 60:
            if self.distraction_start_time is None:
                self.distraction_start_time = time.time()
            looking_away = True
        else:
            self.distraction_start_time = None
            looking_away = False

        distraction_duration = 0
        if self.distraction_start_time:
            distraction_duration = time.time() - self.distraction_start_time

        return looking_away, deviation, distraction_duration

    def detect_fatigue(self, EAR):
        if EAR < 0.22:
            if self.closed_start_time is None:
                self.closed_start_time = time.time()
        else:
            if self.closed_start_time is not None:
                if time.time() - self.closed_start_time > 1.0:
                    self.fatigue_events += 1
            self.closed_start_time = None

        if self.closed_start_time is not None:
            if time.time() - self.closed_start_time > 1.0:
                return True

        return False
