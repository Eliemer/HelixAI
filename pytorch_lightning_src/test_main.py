from Model.GCNN import GCNN
from Logger.logger import JSONLogger
import pytorch_lightning as pl
import os
import json

def main():
    with open('Configs/base_config.json') as base_config:

        my_config = json.load(base_config)
        my_config['input_csv'] = 'Test/input.csv'
        my_config['error_csv'] = 'Test/error.csv'
        my_config['tensors']   = 'Test/Tensors'
        my_config['pdb']       = 'Test/PDB'
        my_config['output_name'] = 'Test/Output'
        my_config['dataset']   = 'MyTestLogger'

        my_config['epochs'] = 10
        # my_config['nb_nodes'] = 25
        # my_config['nb_kernels'] = 2
        # my_config['nb_filters'] = 2
        # my_config['kernel_limit'] = 50
        # my_config['lin_size'] = 8
        my_config['workers'] = 0

        model   = GCNN(my_config)
        logger  = JSONLogger(
            path="Logs/test_log.json",
            name=my_config['dataset']
            )
        trainer = pl.Trainer(
            logger=logger, 
            max_epochs=my_config['epochs'])


        trainer.fit(model)
        trainer.test(model)


if __name__ == '__main__':
    main()
