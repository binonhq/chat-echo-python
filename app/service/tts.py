import io
import os
import time
import torch
from TTS.api import TTS


def save_audio(byte_stream, file_path):
    with open(file_path, 'wb') as f:
        f.write(byte_stream)

    return True


class TTSService:
    def __init__(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = 'tts_models/multilingual/multi-dataset/xtts_v2'
        print(f'TTSService is being initialized by process ID: {os.getpid()}')
        self.tts = TTS(str(model)).to(device)
        print('init model done')
        self.model_manager = None
        os.environ["COQUI_TOS_AGREED"] = "1"

    async def get_own_voice_audio(self, text, file):
        start_time = time.time()
        if self.tts is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            model = 'tts_models/multilingual/multi-dataset/xtts_v2'
            self.tts = TTS(str(model)).to(device)

        check = save_audio(file, "app/tmp/input_file.wav")
        if not check:
            return None

        output_file = io.BytesIO()

        print("Time to load model: ", time.time() - start_time)

        self.tts.tts_to_file(text=text, speaker_wav="app/tmp/input_file.wav", language='en', file_path=output_file,
                             split_sentences=True)

        print("Time to generate audio: ", time.time() - start_time)
        return output_file
