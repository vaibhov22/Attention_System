from flask import Flask, render_template, Response, jsonify, send_file
import cv2
import time
import pandas as pd
import os

import matplotlib
matplotlib.use('Agg')   # IMPORTANT: Disable GUI backend
import matplotlib.pyplot as plt

from vision import VisionSystem
from features import FeatureExtractor
from scoring import AttentionScorer
from logger import SessionLogger

app = Flask(__name__)

# Absolute base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_FOLDER = os.path.join(BASE_DIR, "static")
os.makedirs(STATIC_FOLDER, exist_ok=True)

vision = VisionSystem()
features = FeatureExtractor()
scorer = AttentionScorer()
logger = SessionLogger()

display_score = 100
start_time = time.time()

current_stats = {
    "attention": 100,
    "blink_count": 0,
    "fatigue": False,
    "state": "Focused"
}

def generate_frames():
    global display_score, current_stats

    while True:
        frame, results = vision.get_frame()
        if frame is None:
            break

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:

                left_eye, right_eye, nose_x, nose_y, w = vision.extract_landmarks(frame, face_landmarks)

                left_EAR = features.calculate_EAR(left_eye)
                right_EAR = features.calculate_EAR(right_eye)
                EAR = (left_EAR + right_EAR) / 2.0

                blink_count = features.detect_blink(EAR)
                looking_away, deviation, distraction_duration = features.detect_distraction(nose_x, w)
                fatigue = features.detect_fatigue(EAR)

                raw_score = scorer.calculate_score(EAR, looking_away)
                if fatigue:
                    raw_score -= 40

                raw_score = max(0, raw_score)
                display_score = int(0.8 * display_score + 0.2 * raw_score)

                current_time = time.time() - start_time
                logger.log(current_time, EAR, blink_count, deviation, display_score, looking_away)

                state = "Distracted" if looking_away else "Focused"

                current_stats.update({
                    "attention": display_score,
                    "blink_count": blink_count,
                    "fatigue": fatigue,
                    "state": state
                })

                cv2.putText(frame, f"Attention: {display_score}", (30,40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stats')
def stats():
    return jsonify(current_stats)


@app.route('/stop')
def stop():

    if len(logger.data) == 0:
        return "No session data"

    df = pd.DataFrame(logger.data, columns=[
        "Time",
        "EAR",
        "Blink_Count",
        "Deviation",
        "Attention_Score",
        "Looking_Away"
    ])

    # ---- Generate Graph ----
    plt.figure(figsize=(8,4))
    plt.plot(df["Time"], df["Attention_Score"])
    plt.xlabel("Time (seconds)")
    plt.ylabel("Attention Score")
    plt.title("Attention Over Time")
    plt.grid()
    plt.tight_layout()

    graph_path = os.path.join(STATIC_FOLDER, "attention_plot.png")
    plt.savefig(graph_path)
    plt.close()

    # ---- Save CSV ----
    csv_path = os.path.join(STATIC_FOLDER, "session_data.csv")
    df.to_csv(csv_path, index=False)

    session_duration = df["Time"].iloc[-1]
    avg_attention = df["Attention_Score"].mean()
    distraction_percentage = df["Looking_Away"].mean() * 100

    summary_data = {
        "duration": round(session_duration, 2),
        "avg_attention": round(avg_attention, 2),
        "blinks": features.blink_count,
        "fatigue": features.fatigue_events,
        "distraction": round(distraction_percentage, 2)
    }

    # Reset session data
    logger.data.clear()
    features.blink_count = 0
    features.fatigue_events = 0

    return render_template("summary.html", data=summary_data)


@app.route('/download')
def download_csv():
    file_path = os.path.join(STATIC_FOLDER, "session_data.csv")

    if not os.path.exists(file_path):
        return "CSV file not found"

    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)