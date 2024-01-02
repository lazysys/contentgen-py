from dataclasses import dataclass
from TTS.api import TTS as TTSApi

@dataclass
class TTS:
	_model: str = "tts_models/multilingual/multi-dataset/your_tts"
	reference: str = "ref.wav"
	language: str = "en"
		
	@property
	def model(self):
		return self._model
	@model.setter
	def model(self, model):
		self._model = model
		self.__post_init__()
	
	def __post_init__(self):
		self._tts = TTSApi(model_name=self.model, progress_bar=True)

	def tts(self, text, output):
		tts.tts_to_file(text, speaker_wav=self.reference, language=self.language, file_path=output)
