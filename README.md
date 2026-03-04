Perfect. 🔥
Now we package this like a **real engineering project**.

Below is a **complete professional README.md** you can copy-paste into your GitHub repo.

---

# 📄 `README.md`

```markdown
# 🧠 Real-Time AI Attention & Fatigue Monitoring Web Application

A full-stack AI-powered web application that monitors user attention levels in real-time using computer vision and facial landmark analysis.

Built using Flask, OpenCV, MediaPipe, Pandas, and Docker.

---

## 🚀 Project Overview

This system analyzes facial landmarks from a live webcam feed to:

- Detect blinks using Eye Aspect Ratio (EAR)
- Identify distraction based on head deviation
- Detect fatigue through prolonged eye closure
- Calculate a real-time attention score
- Log session data for analytics
- Generate attention graphs
- Export session data as CSV
- Run inside a Docker container

The application provides a live dashboard and a post-session analytics report.

---

## 🏗️ System Architecture

```

Webcam → OpenCV → MediaPipe FaceMesh → Feature Extraction →
Scoring Engine → Flask Backend → Web Dashboard →
Analytics Engine → Graph + CSV Export

```

---

## 🧠 Core Features

### 1️⃣ Real-Time Facial Landmark Detection
Uses MediaPipe FaceMesh to detect 468 facial landmarks per frame.

---

### 2️⃣ Blink Detection (Eye Aspect Ratio - EAR)

EAR formula:

EAR = (||p2 − p6|| + ||p3 − p5||) / (2 × ||p1 − p4||)

Used to detect:
- Normal blinking
- Prolonged eye closure (fatigue)

---

### 3️⃣ Distraction Detection

Head deviation calculated using nose landmark relative to frame center.

If deviation persists for multiple frames → marked as distracted.

---

### 4️⃣ Fatigue Detection

If eyes remain closed beyond threshold duration → fatigue event recorded.

---

### 5️⃣ Attention Scoring Engine

Attention score is calculated based on:

- Blink behavior
- Distraction detection
- Fatigue detection

Smoothed using exponential smoothing:

```

display_score = 0.8 * previous + 0.2 * current

```

---

### 6️⃣ Session Analytics

At the end of a session:

- Session duration
- Average attention score
- Total blinks
- Fatigue events
- Percentage time distracted
- Attention vs Time graph
- CSV export

---

## 🌐 Web Application Features

- Live video streaming via Flask
- REST endpoint for real-time stats
- Summary dashboard page
- Graph generation (Matplotlib)
- CSV report download
- Clean dark UI

---

## 📦 Docker Support

The application is fully containerized.

### Build Docker Image

```

docker build -t attention-system .

```

### Run Container

```

docker run -p 5000:5000 attention-system

```

Access:

```

[http://localhost:5000](http://localhost:5000)

```

⚠ Note: Webcam access inside Docker may not work on Windows due to device isolation.

---

## 🗂️ Project Structure

```

Attention_Mechanism/
│
├── app.py
├── vision.py
├── features.py
├── scoring.py
├── logger.py
├── static/
│   ├── attention_plot.png
│   └── session_data.csv
├── templates/
│   ├── index.html
│   └── summary.html
├── Dockerfile
├── requirements.txt
└── README.md

```

---

## 🛠️ Technologies Used

- Python
- Flask
- OpenCV
- MediaPipe
- NumPy
- Pandas
- Matplotlib
- Docker

---

## 🎯 Key Engineering Concepts Demonstrated

- Real-time computer vision processing
- Facial landmark geometry analysis
- Feature extraction pipelines
- Stateful scoring logic
- REST API development
- Web streaming architecture
- Data logging & analytics
- Containerization with Docker
- Cross-platform dependency debugging

---

## 💡 Real-World Applications

- Online exam proctoring
- E-learning engagement tracking
- Driver drowsiness detection
- Workplace productivity monitoring
- Human behavioral analytics

---

## 📊 Sample Output

- Live attention score
- Blink counter
- Fatigue detection alerts
- Session summary dashboard
- Attention graph
- Downloadable CSV analytics

---

## 🧪 How to Run Without Docker

### 1️⃣ Create virtual environment

```

python -m venv .venv

```

### 2️⃣ Install dependencies

```

pip install -r requirements.txt

```

### 3️⃣ Run app

```

python app.py

```

---

## 👨‍💻 Author

Vaibhov Soni  
Final Year B.Tech Student | AI/ML Enthusiast  
Passionate about building production-level AI systems.

---

## ⭐ Future Improvements

- User authentication system
- Cloud deployment
- Database-backed session storage
- Multi-user analytics
- Attention heatmap visualization
- WebRTC integration
- GPU acceleration support

---

## 📜 License

This project is built for educational and research purposes.
```

---

## Run Locally

Clone the repository

git clone https://github.com/vaibhov22/Attention_System.git

Go into the project folder

cd Attention_System

Create virtual environment

python -m venv venv

Activate environment

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

Install dependencies

pip install -r requirements.txt

Run the application

python Attention_mechanishm/app.py
