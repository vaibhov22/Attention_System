import pandas as pd

class SessionLogger:
    def __init__(self):
        self.data = []

    def log(self, time, ear, blink_count, deviation, score, looking_away):
        self.data.append([
            time,
            ear,
            blink_count,
            deviation,
            score,
            int(looking_away)
        ])

    def save(self, filename="attention_session.csv"):
        df = pd.DataFrame(self.data, columns=[
            "Time",
            "EAR",
            "Blink_Count",
            "Deviation",
            "Attention_Score",
            "Looking_Away"
        ])
        df.to_csv(filename, index=False)