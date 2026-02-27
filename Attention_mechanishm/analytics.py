import time
import pandas as pd
import matplotlib.pyplot as plt

def generate_report(logger, start_time, features):
    if len(logger.data) == 0:
        print("No session data recorded.")
        return

    session_duration = time.time() - start_time

    df = pd.DataFrame(logger.data, columns=[
        "Time",
        "EAR",
        "Blink_Count",
        "Deviation",
        "Attention_Score",
        "Looking_Away"
    ])

    avg_attention = df["Attention_Score"].mean()
    distraction_percentage = df["Looking_Away"].mean() * 100

    print("\n===== SESSION SUMMARY =====")
    print(f"Session Duration: {session_duration:.2f} seconds")
    print(f"Average Attention: {avg_attention:.2f}")
    print(f"Total Blinks: {features.blink_count}")
    print(f"Fatigue Events: {features.fatigue_events}")
    print(f"Time Distracted: {distraction_percentage:.2f}%")
    print("===========================\n")

    # Plot attention over time
    plt.figure(figsize=(8,4))
    plt.plot(df["Time"], df["Attention_Score"])
    plt.xlabel("Time (seconds)")
    plt.ylabel("Attention Score")
    plt.title("Attention Over Time")
    plt.grid()
    plt.tight_layout()
    plt.savefig("attention_plot.png")
    plt.show()