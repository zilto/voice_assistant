import asyncio
import base64
import json
import websockets

import numpy as np
import whisper


MODEL_NAME = "small.en"
LANGUAGE = "english"


async def server_handler(websocket):
    model = whisper.load_model(MODEL_NAME)

    async for message in websocket:
        event = json.loads(message)
        assert event["type"] == "audio_input"

        try:
            audio_bytes = base64.b64decode(event["data"].encode("ascii"))
            data = np.frombuffer(audio_bytes, np.int16) \
                     .flatten() \
                     .astype(np.float32) / 32768
            result = model.transcribe(data, language=LANGUAGE)
        except Exception as e:
            event = {"type": "error", "data": str(e)}
            await websocket.send(json.dumps(event))
            continue

        event = {"type": "transcript", "data": result["text"]}
        await websocket.send(json.dumps(event))


async def main():
    async with websockets.serve(server_handler, "localhost", 8001):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
