import cv2
import time
from vision import VisionSystem
from features import FeatureExtractor
from scoring import AttentionScorer
from logger import SessionLogger
from analytics import generate_report

start_time = time.time()

vision = VisionSystem()
features = FeatureExtractor()
scorer = AttentionScorer()
logger = SessionLogger()

display_score = 100  # smoothed score

while True:
    frame, results = vision.get_frame()
    if frame is None:
        break

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:

            left_eye, right_eye, nose_x, nose_y, w = vision.extract_landmarks(frame, face_landmarks)

            # --- Feature Extraction ---
            left_EAR = features.calculate_EAR(left_eye)
            right_EAR = features.calculate_EAR(right_eye)
            EAR = (left_EAR + right_EAR) / 2.0

            blink_count = features.detect_blink(EAR)
            looking_away, deviation, distraction_duration = features.detect_distraction(nose_x, w)
            fatigue = features.detect_fatigue(EAR)

            # --- Raw Scoring ---
            raw_score = scorer.calculate_score(EAR, looking_away)

            if fatigue:
                raw_score -= 40

            raw_score = max(0, raw_score)

            # --- Smooth Score ---
            display_score = int(0.8 * display_score + 0.2 * raw_score)

            # --- Logging ---
            current_time = time.time() - start_time
            logger.log(current_time, EAR, blink_count, deviation, display_score, looking_away)

            # --- Display ---
            cv2.putText(frame, f"Blinks: {blink_count}", (50,100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

            cv2.putText(frame, f"Attention: {display_score}", (50,150),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

            if looking_away:
                cv2.putText(frame, "Distracted", (50,200),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            else:
                cv2.putText(frame, "Focused", (50,200),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            if fatigue:
                cv2.putText(frame, "Fatigue Detected", (50,250),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.imshow("Attention System", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# After exiting loop
generate_report(logger, start_time, features)
logger.save()
vision.release()