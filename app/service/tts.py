import io
import os
import time
import tempfile
import subprocess
import torch
from TTS.api import TTS


def save_audio(byte_stream, file_path):
    with open(file_path, 'wb') as f:
        f.write(byte_stream)

    return True


def re_encode_audio(input_file_path):
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_out_file:
        # Check if the file already exists and delete it to ensure overwrite
        if os.path.exists(temp_out_file.name):
            os.remove(temp_out_file.name)

        command = [
            'ffmpeg',
            '-i', input_file_path,
            '-acodec', 'pcm_s16le',
            '-ar', '44100',
            temp_out_file.name
        ]
        subprocess.run(command, check=True)
        return temp_out_file.name


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

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file.write(file)
            temp_input_file_path = temp_file.name

        re_encoded_file = re_encode_audio(temp_input_file_path)

        output_file = io.BytesIO()

        print("Time to load model: ", time.time() - start_time)

        self.tts.tts_to_file(text=text, speaker_wav=re_encoded_file, language='en', file_path=output_file,
                             split_sentences=True)

        print("Time to generate audio: ", time.time() - start_time)

        os.remove(temp_input_file_path)
        os.remove(re_encoded_file)
        return output_file
