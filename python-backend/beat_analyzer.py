import librosa
import json

def analyze_beats(audio_path):
    y, sr = librosa.load(audio_path)

    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    print(f"BPM: {tempo}")
    print(f"Beats at: {beat_times}")

    return {
        "bpm": float(tempo),
        "beats": beat_times.tolist()
    }

if __name__ == "__main__":
    data = analyze_beats("music.wav")

    with open("beat_data.json", "w") as f:
        json.dump(data, f, indent=2)