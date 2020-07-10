from Model.GCNN import GCNN
import pytorch_lightning as pl

import json

def main():
    with open('Configs/base_config.json') as base_config:

        my_config = json.load(base_config)
        my_config['input_csv'] = 'Test/input.csv'
        my_config['error_csv'] = 'Test/error.csv'
        my_config['tensors']   = 'Test/Tensors'
        my_config['pdb']       = 'Test/PDB'
        my_config['output_name'] = 'Test/Output'


        # my_config['nb_nodes'] = 25
        # my_config['nb_kernels'] = 2
        # my_config['nb_filters'] = 2
        # my_config['kernel_limit'] = 50
        # my_config['lin_size'] = 8
        my_config['workers'] = 0

        model = GCNN(my_config)
        trainer = pl.Trainer()

        trainer.fit(model)


if __name__ == '__main__':
    main()
