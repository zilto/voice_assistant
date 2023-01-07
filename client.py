import asyncio
import base64
import json
from queue import Queue
import websockets

import speech_recognition as sr

from commands import register_commands, execute_command


KEYWORD = "yoshi"
SAMPLE_RATE = 16000
CHUNK_SIZE = 2048

audio_queue = Queue()
commands_config = register_commands(["command_library"])


async def produce_audio(websocket):
    audio_bytes = audio_queue.get()
    event = {"type": "audio_input", "data": base64.b64encode(audio_bytes).decode("ascii")}
    await websocket.send(json.dumps(event))


async def consume_transcript(websocket):
    async for message in websocket:
        event = json.loads(message)
        if (event_type := event.get("type")) != "transcript":
            raise TypeError(f"client received event type {event_type}")

        print(f"> {event['data']}")
        execute_command(event["data"], KEYWORD, commands_config)


async def main():
    def callback(r, audio):
        audio_queue.put_nowait(audio.get_raw_data())

    r = sr.Recognizer()
    m = sr.Microphone(sample_rate=SAMPLE_RATE, chunk_size=CHUNK_SIZE)
    with m as source:
        r.adjust_for_ambient_noise(source)

    stop_listening = r.listen_in_background(m, callback)

    async with websockets.connect("ws://localhost:8001/") as websocket:
        await asyncio.gather(produce_audio(websocket), consume_transcript(websocket))


if __name__ == "__main__":
    asyncio.run(main())
