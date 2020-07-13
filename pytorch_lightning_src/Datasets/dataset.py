import torch
from torch.utils.data import Dataset

import pandas as pd
import numpy as np

from math import floor

class DatasetProtein(Dataset):

    def __init__(self, input_df, error_df=None, nb_nodes=350, nb_features=29, nb_classes=2, split=(0.7,0.1,0.2), shuffle=True, path='pdb_extractor/HRAS_KRAS/Tensors', fuzzy_radius=0, augment=1):

        self.input_df = input_df
        self.fuzzy_radius = fuzzy_radius
        self.augment = augment
        self.path = path if path[-1] != '/' else path + '/'
        self.nb_nodes = nb_nodes
        self.nb_features = nb_features
        self.nb_classes = nb_classes

        if error_df is not None:
             input_df = pd.concat([input_df, error_df, error_df]).drop_duplicates(keep=False)
             self.input_df = input_df

        self.input_df = self.input_df.reset_index(drop=True)

    def __getitem__(self, index):
        pdb_id, chain, target = self.input_df.iloc[index].values

        try:
            np_chain = np.load(f'{self.path}{str.upper(pdb_id)}_{str.upper(chain)}.npy')
            np_chain = np_chain.astype('float32')

        except ValueError:
            print(pdb_id, chain, 'Value Error')

        except TypeError:
            print(pdb_id, chain, 'Type Error')

        res = np.zeros([np_chain.shape[0], 23])
        for i in range(np_chain.shape[0]):
            res[i, int(np_chain[i,2])] = 1

        v = np_chain[:,3:5]
        c = np_chain[:,-3:]

        s = sequence_encode(np_chain[:,1],4)


        v = np.concatenate([res,v, s], axis=-1)

        c -= c.mean(axis=0)

        m = np_chain[:,0]

        if self.augment != 1:
             random_shift = np.random.normal(0.0, self.fuzzy_radius, c.shape)
             c += random_shift

        if v.shape[0] < self.get_sizes()[1]:
             v_ = np.zeros((self.get_sizes()[1], v.shape[1]))
             v_[:v.shape[0], :v.shape[1]] = v

             c_ = np.zeros((self.get_sizes()[1], c.shape[1]))
             c_[:c.shape[0], :c.shape[1]] = c

             m_ = np.zeros((self.get_sizes()[1]))
             m_[:m.shape[0]] = m

             v = v_
             c = c_
             m = m_

        else :
             v = v[:self.get_sizes()[1], :v.shape[1]]
             c = c[:self.get_sizes()[1], :c.shape[1]]
             m = m[:self.get_sizes()[1]]

        m = np.repeat(np.expand_dims(m, axis=-1), len(m), axis=-1)
        m = (m * m.T) + np.eye(self.get_sizes()[1])
        m[m>1] = 1


        # print(v.shape, c.shape, m.shape)
        v = v.astype('float32')
        c = c.astype('float32')
        m = m.astype('float32')
        # target = target.astype('float32')
        # print(v.dtype, c.dtype, m.dtype)
        if target in [1,2,3] and self.nb_classes==2:
            target = 1

        return v, c, m, target

    def __len__(self):
        return self.input_df.shape[0]

    def get_sizes(self):
        return self.__len__(), self.nb_nodes, self.nb_features

def sequence_encode(seq, nb_dims):
    sequence_enc = np.array([
        [pos / np.power(10000, 2 * (j // 2) / nb_dims) for j in range(nb_dims)]
        if pos != 0 else np.zeros(nb_dims) for pos in seq])
    sequence_enc[1:, 0::2] = np.sin(sequence_enc[1:, 0::2]) # dim 2i
    sequence_enc[1:, 1::2] = np.cos(sequence_enc[1:, 1::2]) # dim 2i+1

    return sequence_enc
