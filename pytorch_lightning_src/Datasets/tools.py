import numpy as np
from scipy.spatial.distance import euclidean, cosine
from scipy.stats import percentileofscore as perc
import pandas as pd
import itertools
import os
import csv
import sys
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from urllib.error import HTTPError
import requests

from torch.utils.data import Subset


residues = ['ALA', 'ARG', 'ASN', 'ASP', 'ASX', 'CYS', 'GLN',
            'GLU', 'GLX', 'GLY', 'HIS', 'ILE', 'LEU', 'LYS',
            'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP', 'TYR',
            'UNK', 'VAL']


def fetch_pdb(config):
    def fetch(pdb_row, path):

        if path[-1] != '/' : path += '/'

        pdb_id = pdb_row['PDB_ID']
        # print(path)
        # print('fetch', pdb_id)
        file = pdb_id.lower() + '.pdb'
        file_path = path + file
        rcsb = 'https://files.rcsb.org/download/'
        # print(rcsb + file)
        # print(file_path, os.path.exists(file_path))
        if not os.path.exists(file_path):
            try:
                # print(rcsb + file)
                r = requests.get(rcsb + file, stream=True)
                # print('status', r.status_code)
                if r.status_code==200:
                    with open(file_path, 'wb') as f:
                        for chunk in r:
                            f.write(chunk)
            except HTTPError:
                print("PDBNotFoundError:", pdb_id)
            except:
                print('Error:', sys.exc_info()[0])

    with open(config['input_csv'], newline='') as csvfile:
        with ThreadPoolExecutor() as executor:
            executor.map(lambda param: fetch(param, config['pdb']), csv.DictReader(csvfile))

def parse_pdb(path, chain, all_chains=False, first=False):
    '''
    '''
    # Parse residue, atom type and atomic coordinates
    seq_data = []
    helix_data = []
    beta_data = []
    complex_data = {}
    protein_data = []
    res_ = None
    res_i = None
    res_c = None
    sidechain_data = []
    sidechain_flag = False
    sidechain_counter = 0
    with open(path, 'r') as f:
        lines = f.readlines()
        for row in lines:
            if row[:6] == 'SEQRES':
                row_ = row[:-1].split()
                if not all_chains and row_[2] != chain.upper(): continue
                for _ in row_[4:]:
                    try: ress = residues.index(_)
                    except: ress = residues.index('UNK')
                    seq_data.append([row_[2].upper(), ress])

            if row[:5] == 'HELIX':
                if not all_chains and row[19] != chain.upper(): continue
                helix_data.append([row[19], int(row[22:25]), int(row[34:37])])

            if row[:5] == 'SHEET':
                if not all_chains and row[21] != chain.upper(): continue
                beta_data.append([row[21], int(row[23:26]), int(row[34:37])])

            if row[:4] == 'ATOM':

                # Check if for chain
                if not all_chains and row[21] != chain.upper(): continue

                if res_i is None: res_i = row[22:26]

                if row[22:26] == res_i:

                    if row[12:17] in [' CA  ',' CA A']:
                        res_ = row[17:20]
                        res_c = [row[30:38].strip(), row[38:46].strip(), row[47:54].strip()]
                        sidechain_flag = True
                        sidechain_counter += 1
                    else:
                        if sidechain_flag:
                            if sidechain_counter > 2:
                                sidechain_data.append([row[30:38].strip(), row[38:46].strip(), row[47:54].strip()])
                            else:
                                sidechain_counter += 1

                else:
                    try: ress = residues.index(res_)
                    except: ress = residues.index('UNK')
                    if len(sidechain_data)> 0:
                        sidechain_data = np.array(sidechain_data).astype('float')
                        sidechain_c = np.mean(sidechain_data, axis=0).tolist()
                        sidechain_data = []
                    else:
                        sidechain_c = res_c
                    sidechain_flag = False
                    sidechain_counter = 0
                    if res_c is not None:
                        res_data = [res_i, ress] + res_c + sidechain_c
                        protein_data.append(res_data)
                    res_i = row[22:26]

            if row[:3] == 'TER':
                if sidechain_flag == True:
                    try: ress = residues.index(res_)
                    except: ress = residues.index('UNK')
                    if len(sidechain_data)> 0:
                        sidechain_data = np.array(sidechain_data).astype('float')
                        sidechain_c = np.mean(sidechain_data, axis=0).tolist()
                        sidechain_data = []
                    else:
                        sidechain_c = res_c
                    sidechain_flag = False
                    sidechain_counter = 0
                    if res_c is not None:
                        res_data = [res_i, ress] + res_c + sidechain_c
                        protein_data.append(res_data)

                if len(protein_data) > 0:
                    complex_data[row[21].upper()] = protein_data
                    protein_data = []
                    if not all_chains or first: break

    if len(complex_data)==0: return []
    # No Sequence Data
    if len(seq_data) < 1:
        chains_ = []
        ress_ = []
        for _ in complex_data:
            chains = np.array([' ' for i in range(len(_))])
            chains_.append(chains)
            ress_.append(_[:,1])
        chains_ = np.expand_dims(np.concatenate(chains_, axis=0),axis=-1)
        ress_ = np.expand_dims(np.concatenate(ress_, axis=0),axis=-1)
        seq_data = np.concatenate([chains_, ress_], axis=-1)

    # Set Sequence Data
    data = {}
    last_chain = -1
    temp = []
    ii = 1
    for i,_ in enumerate(seq_data):
        t = np.zeros((10))
        t[2] = _[1]
        t[1] = ii
        ii += 1
        if last_chain != _[0] or i+1 == len(seq_data):
            if i+1 == len(seq_data): temp.append(t)
            if len(temp) > 0:
                data[last_chain] = np.array(temp)
                temp = []
                ii = 0
            else: temp.append(t)
            last_chain = _[0]
        else:
            temp.append(t)

    '''
    last_chain = None
    temp_i = -1
    for i,_ in enumerate(helix_data):
        if last_chain != _[0]:
            last_chain = _[0]
            temp_i +=1
        data[temp_i][_[1]-1:_[2]-1,5] = 1
    last_chain = None
    temp_i = -1
    for i,_ in enumerate(beta_data):
        if last_chain != _[0].upper():
            last_chain = _[0].upper()
            temp_i +=1
        data[temp_i][_[1]-1:_[2]-1,6] = 1
    '''
    for i in data.keys():
        data[i] = data[i].astype('int').astype('str')

    for ii in complex_data.keys():
        chain_data = np.array(complex_data[ii])
        chain_c = chain_data[:,2:5].astype('float')
        chain_sc_c = chain_data[:,5:].astype('float')
        chain_centroid = np.mean(chain_c,axis=0)
        residue_depth = np.array([euclidean(chain_centroid, c) for c in chain_c])
        residue_depth_percentile = [1- perc(residue_depth, d)/100.0 for d in residue_depth]
        chain_c = chain_c - chain_centroid
        chain_sc_c = chain_sc_c - chain_centroid
        chain_sc_c = chain_sc_c - chain_c
        chain_c = -(chain_c)
        residue_orientation = [1-cosine(chain_c[i], chain_sc_c[i]) for i in range(len(chain_c))]

        if ii not in data: continue

        # Try First three res align
        offset = -1
        for j in range(len(chain_data)-3):
            for i, _ in enumerate(data[ii][:-3]):
                if data[ii][i:i+3,2].tolist() == chain_data[j:j+3, 1].tolist():
                    offset = int(data[ii][i,1]) - int(chain_data[j,0])
                    break
            if offset != -1: break

        if offset == -1:
            return []

        for i in range(len(chain_data)):
            ir = int(chain_data[i][0]) - 1 + offset
            if ir >= len(data[ii]): break
            if ir < 0: continue
            data[ii][ir,0] = 1
            data[ii][ir,3] = str(residue_depth_percentile[i])[:6]
            data[ii][ir,-3:] = chain_data[i,2:5]
            if np.isnan(residue_orientation[i]): data[ii][ir,4] = '0.0000'
            else: data[ii][ir,4] =  str(residue_orientation[i])[:6]

        tmp = 0
        for i, _ in enumerate(data[ii]):
            if data[ii][i,0] == '1': tmp = i
            else:
                data[ii][i,-3:] = data[ii][tmp,-3:]

    data = np.concatenate([data[ii] for ii in data.keys()], axis=0)
    if len(data) == 0: return []

    return data

def tensorize_pdb(conf):
    print('\n\n### Start tensorize_pdb ###')
    with open(conf['input_csv'], newline='') as csvfile:
        ### Multiprocess
        # with ProcessPoolExecutor() as executor:
        #     executor.map(lambda param: tensorize(param, conf['pdb'], conf['tensors']), csv.DictReader(csvfile))

        ## Single process
        for row in csv.DictReader(csvfile):
            tensorize(row, conf['pdb'], conf['tensors'])

    print('### End tensorize_pdb ###\n\n')

def tensorize(pdb_row, path, tensor):
    pdb_id = pdb_row['PDB_ID'].lower()
    chain_id = pdb_row['CHAIN_ID']
    npy_file = pdb_id.upper() + '_' + chain_id.upper() + '.npy'
    all_chains =  False

    if path[-1] != '/': path += '/'
    if tensor[-1] != '/': tensor += '/'

    if not os.path.exists(path + pdb_id + '.pdb'):
        print("PDB not found: " + pdb_id + '.pdb')

    if not os.path.exists(tensor + npy_file):
        protein_data = parse_pdb(path + pdb_id + '.pdb', chain_id, all_chains, False)
        print(npy_file, len(protein_data))

        np.save(f"{tensor}{npy_file}", protein_data)
    else:
        print(npy_file, 'EXISTS')


def get_subsets(dataset, split=(0.7,0.1,0.2), augment=1):
    classes = [dataset.input_df.index[dataset.input_df['CLASS_ID'] == i].tolist() for i in range(dataset.nb_classes)]
    train_sizes = [0] * dataset.nb_classes
    val_sizes = [0] * dataset.nb_classes
    test_sizes = [0] * dataset.nb_classes
    train_indices = []
    test_indices = []
    val_indices = []

    for i, cls in enumerate(classes):
        train_val_size = int(np.floor((split[0] + split[1]) * len(cls)))
        train_size = int(np.floor(split[0] / (split[0] + split[1]) * train_val_size))
        val_size = train_val_size - train_size
        test_size = len(cls) - train_val_size
        # print(train_size, test_size, val_size)

        train_sizes[i] = train_size
        val_sizes[i] = val_size
        test_sizes[i] = test_size


        train_indices.append(cls[: train_sizes[i]])
        test_indices.append(cls[train_sizes[i] : (train_sizes[i] + test_sizes[i])])
        val_indices.append(cls[(train_sizes[i] + test_sizes[i]) :])

    train_indices = list(itertools.chain.from_iterable(train_indices)) # flatten the lists
    test_indices = list(itertools.chain.from_iterable(test_indices))
    val_indices = list(itertools.chain.from_iterable(val_indices))

    targets = dataset.input_df['CLASS_ID'].values
    for i, t in enumerate(targets):
        if t in [1,2,3] and dataset.nb_classes == 2:
            targets[i] = 1

    weights = [1.0 / len(classes[i]) for i in range(dataset.nb_classes)]
    sample_weights = np.array([weights[t] for t in targets])

    train_weights = sample_weights[train_indices]
    test_weights = sample_weights[test_indices]
    val_weights = sample_weights[val_indices]

    if augment > 1:
        train_indices *= augment
        val_indices *= augment

    train_subset = Subset(dataset, train_indices)
    test_subset = Subset(dataset, test_indices)
    val_subset = Subset(dataset, val_indices)

    return (train_subset, test_subset, val_subset), (train_weights, test_weights, val_weights), (weights)

def accuracy(output, labels):
    pass

def precision(output, labels):
    pass

def recall(output, labels):
    pass
