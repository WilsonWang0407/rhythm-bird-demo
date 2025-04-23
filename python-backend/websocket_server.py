import asyncio
import json
import websockets
import time

with open("beat_data.json", "r") as f:
    beat_data = json.load(f)

beats = beat_data["beats"]
bpm = beat_data["bpm"]

print(f"Loaded {len(beats)} beats at {bpm} BPM")

# WebSocket handler
async def send_beats(websocket, path):
    print("Client connected.")
    for beat_time in beats:
        message = json.dumps({"beat": beat_time})
        await websocket.send(message)
        print(f"Sent beat: {beat_time}")
        await asyncio.sleep(60.0 / bpm)
    print("All beats sent.")

async def main():
    print("WebSocket server starting on ws://localhost:6789 ...")
    async with websockets.serve(send_beats, "localhost", 6789):
        await asyncio.Future()

asyncio.run(main())