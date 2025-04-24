import librosa
import json

def analyze_onsets(audio_path):
    y, sr = librosa.load(audio_path)

    onset_frames = librosa.onset.onset_detect(y=y, sr=sr, backtrack=True)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    print(f"Detected {len(onset_times)} onsets")
    print(f"Onsets at: {onset_times}")

    return {
        "bpm": None,
        "beats": onset_times.tolist()
    }

if __name__ == "__main__":
    data = analyze_onsets("output/music/vocals.wav")
    with open("beat_data.json", "w") as f:
        json.dump(data, f, indent=2)