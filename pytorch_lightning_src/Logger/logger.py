from pytorch_lightning.loggers import LightningLoggerBase
import pytorch_lightning as pl
import os
import json


class JSONLogger(LightningLoggerBase):

	def __init__(self, path, name):
		super(JSONLogger, self).__init__()
		# self._save_dir = path

		self._name = name
		self._save_dir = os.path.join(path, name + ".json")

		os.makedirs(path, exist_ok=True)


		with open(self._save_dir, 'w') as fp:
			json.dump([], fp)

	def log_hyperparams(self, params):
		pass

	def log_metrics(self, metrics, step):
		
		with open(self._save_dir, 'r') as fp:
			data = json.load(fp)
			data.append(metrics)

		with open(self._save_dir, 'w') as fp:
			json.dump(data, fp)

	@property 
	def experiment(self):
		pass

	@property 
	def version(self):
		pass

	@property
	def name(self):
		return self._save_dir.split('.').pop(0)
