from loguru import logger
from .tts_interface import TTSInterface
from loguru import logger
from elevenlabs.client import ElevenLabs




class ElevenLabsTTSEngine(TTSInterface):
    def __init__(
        self, api_key=None, voice_id=None, model_id=None, output_format="mp3_44100_128"
    ):
        self.client = ElevenLabs(api_key=api_key)

        self.voice_id = voice_id
        self.model_id = model_id
        self.output_format = output_format
        self.file_extension = "mp3"


    def generate_audio(self, text, file_name_no_ext=None):
        file_name = self.generate_cache_file_name(file_name_no_ext, self.file_extension)
        try:
            # Call the API to generate audio
            logger.debug(
                f"Generating audio with voice_id={self.voice_id}, model_id={self.model_id}"
            )
            audio_stream = self.client.text_to_speech.convert(
                text=text,
                voice_id=self.voice_id,
                model_id=self.model_id,
                output_format=self.output_format,
            )
            with open(file_name, 'wb') as audio_file:
                for chunk in audio_stream:
                    audio_file.write(chunk)

            logger.info(f"Successfully created audio file: {file_name}")
            return file_name

        except Exception as e:
            logger.error(f"Error generating audio with ElevenLabs: {str(e)}")
            return None
