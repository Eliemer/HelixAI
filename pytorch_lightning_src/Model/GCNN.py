import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import WeightedRandomSampler, DataLoader

from collections import OrderedDict
import pandas as pd
import pprint

pp = pprint.PrettyPrinter(indent=2)

try:
	from Model.GCNN_Layers import *
	from Datasets.tools import get_subsets, fetch_pdb, tensorize_pdb
	from Datasets.dataset import DatasetProtein

except ModuleNotFoundError:
	from pytorch_lightning_src.Model.GCNN_Layers import *
	from pytorch_lightning_src.Datasets.tools import get_subsets, fetch_pdb, tensorize_pdb
	from pytorch_lightning_src.Datasets.dataset import DatasetProtein

import pytorch_lightning as pl
from pytorch_lightning.metrics.functional import accuracy, precision, recall, f1_score

class GCNN(pl.LightningModule):

	def __init__(self, config_dict):
		super(GCNN, self).__init__()

		self.config = config_dict
		# print(len(self.config))

		self.conv_layers = OrderedDict()

		for_nb_nodes = config_dict['nb_nodes']
		for_nb_features = config_dict['nb_features']

		self.adj = AdjacencyMatrix()

		# print(for_nb_nodes, for_nb_features)
		for i in range(config_dict['nb_conv_layers']):
			self.conv_layers[f'kernel_{i}'] = GraphKernels(
				nb_kernels=config_dict['nb_kernels'],
				nb_nodes=for_nb_nodes,               # X.size()[1],
				nb_features=for_nb_features,            # X.size()[2],
				kernel_limit=config_dict['kernel_limit'],
				batch_size=config_dict['batch'],             # X.size()[0],
				training=None)
			self.conv_layers[f'conv_{i}'] = GraphConv(
				nb_filters=config_dict['nb_filters'],
				nb_nodes=for_nb_nodes,               # X.size()[1],
				nb_features=for_nb_features,            # X.size()[2],
				support=config_dict['nb_kernels'],
				batch_size=config_dict['batch'],
				activation=nn.LeakyReLU(),
				training=None)
			for_nb_nodes = max(for_nb_nodes // config_dict['pool_size'], 1)
			for_nb_features = config_dict['nb_filters']

		self.conv_layers = nn.ModuleDict(self.conv_layers)
		self.convdrop = nn.Dropout(p=config_dict['conv_dropout'])
		self.avgpool = AverageSeqGraphPool(pool_size=config_dict['pool_size'])

		self.attention = Attention(
			nb_nodes=config_dict['nb_nodes'] // (config_dict['pool_size'] ** config_dict['nb_conv_layers']),
			nb_features=config_dict['nb_filters'],
			batch_size=config_dict['batch']
		)


		self.flat = Flatten()

		self.activation = nn.LeakyReLU()

		self.lin_layers = OrderedDict()
		self.lin_layers['lin_0'] = nn.Linear((config_dict['nb_nodes']
				// (config_dict['pool_size'] ** config_dict['nb_conv_layers']))
				* config_dict['nb_filters'],
				config_dict['lin_size'])


		for j in range(1, config_dict['nb_linear_layers']):
			self.lin_layers[f'lin_{j}'] = nn.Linear(config_dict['lin_size'], config_dict['lin_size'])

		self.lin_drop = nn.Dropout(config_dict['lin_dropout'])

		for k in range(config_dict['nb_linear_layers']):
			self.lin_layers[f'norm_{k}'] = nn.BatchNorm1d(config_dict['lin_size'])
		self.lin_layers = nn.ModuleDict(self.lin_layers)

		self.answer = nn.Linear(config_dict['lin_size'], config_dict['nb_classes'])

	def prepare_data(self):

		fetch_pdb(self.config)
		tensorize_pdb(self.config)

	def setup(self, step):

		path = self.config['tensors']
		if path[-1] != '/': path += '/'

		self.data = DatasetProtein(
			input_df = pd.read_csv(self.config['input_csv']),
			error_df = pd.read_csv(self.config['error_csv']),
			nb_nodes = self.config['nb_nodes'],
			nb_features = self.config['nb_features'],
			nb_classes = self.config['nb_classes'],
			path = path,
			split = self.config['split'],
			shuffle = self.config['shuffle'],
			fuzzy_radius = self.config['fuzzy_radius'],
			augment = self.config['augment']
		)

		self.subsets, self.weights, self.class_weights = get_subsets(self.data, self.config['split'], self.config['augment'])

	def configure_optimizers(self):
		return torch.optim.Adam(self.parameters(), lr=self.config['learning_rate'])

	def train_dataloader(self):
		train_sampler = None
		if self.config['is_weighted']:
			train_sampler = WeightedRandomSampler(
				self.weights[0],
				num_samples=len(self.subsets[0]),
				replacement=True
			)

		data_ld = DataLoader(self.subsets[0],
			batch_size=self.config['batch'],
			sampler=train_sampler,
			shuffle=(not self.config['is_weighted']),
			num_workers=self.config['workers']
		)

		return data_ld

	def val_dataloader(self):

		val_sampler = None
		if self.config['is_weighted']:
				val_sampler = WeightedRandomSampler(
				self.weights[2],
				num_samples=len(self.subsets[2]),
				replacement=True
			)

		data_ld = DataLoader(self.subsets[1],
			batch_size=self.config['batch'],
			sampler=val_sampler,
			shuffle=(not self.config['is_weighted']),
			num_workers=self.config['workers']
		)

		return data_ld

	def test_dataloader(self):

		test_sampler = None
		if self.config['is_weighted']:
			test_sampler = WeightedRandomSampler(
				self.weights[1],
				num_samples=len(self.subsets[1]),
				replacement=True
			)

		data_ld = DataLoader(self.subsets[1],
			batch_size=self.config['batch'],
			sampler=test_sampler,
			shuffle=(not self.config['is_weighted']),
			num_workers=self.config['workers']
		)

		return data_ld

	def forward(self, v, c, mask=None):

		adj = self.adj(c) # Batch, 2(l2 dist, cos dist), nodes, nodes
		v_prime = v # Batch, nodes, features
		c_prime = c # Batch, nodes, number of coords

		for i in range(self.config['nb_conv_layers']):
		    # print(f'###### Conv loop {i+1} ######')

		    # print('###### graph kernel ######')
		    a_prime = self.conv_layers[f'kernel_{i}'](v_prime, adj[:,0,:,:], mask)

		    mask = F.max_pool2d(mask, kernel_size=self.config['pool_size'], stride=self.config['pool_size'])
		    a_prime = torch.cat([a_prime, adj[:,1:2,:,:]], dim=1)

		    # print('###### graph convolution ######')
		    v_prime = self.conv_layers[f'conv_{i}'](v_prime, a_prime)

		    # print('###### convolution dropout ######')
		    v_prime = self.convdrop(v_prime)

		    # print('###### average pool ######')
		    v_prime, c_prime, adj = self.avgpool(v_prime, c_prime)

		# print('###### attention ######')
		v_prime = self.attention(v_prime)

		# print('###### flatten ######')
		v_flat = self.flat(v_prime)

		for i in range(self.config['nb_linear_layers']):
		    # print(f'###### linear loop {i+1} ######')
		    v_flat = self.lin_layers[f'lin_{i}'](v_flat)
		    v_flat = self.lin_layers[f'norm_{i}'](v_flat)
		    v_flat = self.activation(v_flat)
		    v_flat = self.lin_drop(v_flat)

		answer = self.answer(v_flat)
		return answer

	def model_loss(self, logits, labels):
		return F.cross_entropy(logits, labels)

	def training_step(self, batch, batch_idx):
		v, c, m, target = batch
		logits = self.forward(v,c,m)
		loss = self.model_loss(logits, target)


		logs = {'train_loss'  : loss,
				'train_acc'   : accuracy(logits, target),
				'train_recall': recall(logits, target),
				'train_prec'  : precision(logits, target)}

		# pp.pprint(logs)
		return {'loss': loss, 'log': logs}

	def training_epoch_end(self, outputs):
		logs = {}

		logs['train_loss_mean']    = torch.stack([x['log']['train_loss'] for x in outputs]).mean()
		logs['train_acc_mean']     = torch.stack([x['log']['train_acc'] for x in outputs]).mean()
		logs['train_recall_mean']  = torch.stack([x['log']['train_recall'] for x in outputs]).mean()
		logs['train_prec_mean']    = torch.stack([x['log']['train_prec'] for x in outputs]).mean()

		return {"log": logs}

	def validation_step(self, batch, batch_idx):
		v, c, m, target = batch
		logits = self.forward(v,c,m)
		loss = self.model_loss(logits, target)

		logs = {'val_loss'  : loss,
				'val_acc'   : accuracy(logits, target),
				'val_recall': recall(logits, target),
				'val_prec'  : precision(logits, target)}

		# pp.pprint(logs)
		return {"loss": loss, 'log' : logs}

	def validation_epoch_end(self, outputs):
		logs = {}

		logs['val_loss_mean']    = torch.stack([x['log']['val_loss'] for x in outputs]).mean()
		logs['val_acc_mean']     = torch.stack([x['log']['val_acc'] for x in outputs]).mean()
		logs['val_recall_mean']  = torch.stack([x['log']['val_recall'] for x in outputs]).mean()
		logs['val_prec_mean']    = torch.stack([x['log']['val_prec'] for x in outputs]).mean()

		return {"log": logs}

	def test_step(self, batch, batch_idx):
		v, c, m, target = batch
		logits = self.forward(v,c,m)
		loss = self.model_loss(logits, target)

		logs = {'test_loss'  : loss,
				'test_acc'   : accuracy(logits, target),
				'test_recall': recall(logits, target),
				'test_prec'  : precision(logits, target)}

		# pp.pprint(logs)
		return {'loss': loss, 'log' : logs}

	def test_epoch_end(self, outputs):
		logs = {}

		logs['test_loss_mean']    = torch.stack([x['log']['test_loss'] for x in outputs]).mean()
		logs['test_acc_mean']     = torch.stack([x['log']['test_acc'] for x in outputs]).mean()
		logs['test_recall_mean']  = torch.stack([x['log']['test_recall'] for x in outputs]).mean()
		logs['test_prec_mean']    = torch.stack([x['log']['test_prec'] for x in outputs]).mean()

		return {"log": logs}