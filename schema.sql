/*
The following is a Database Schema for Helix
Helix is a Protein Structure Classifier that uses a Graph Convolutional Neural
Network to train modelthat are able to classify proteins.
*/

/* Entities */
CREATE TABLE login( login_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT NOT NULL UNIQUE,
                     password TEXT NOT NULL );

CREATE TABLE User( user_id  INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT NOT NULL, last_name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE, address TEXT NOT NULL, city TEXT NOT NULL, country TEXT NOT NULL );

CREATE TABLE ConfigFile(config_id INTEGER PRIMARY KEY AUTOINCREMENT, config_name TEXT UNIQUE, 
                       dataset_name TEXT, epoch INTEGER, batch INTEGER, workers INTEGER,learning_Rate REAL,
                       shuffle TEXT, fuzzy_radius REAL, augment INTEGER, is_weighted TEXT, nb_classes INTEGER,
                       nb_features INTEGER, nb_nodes INTEGER,  nb_conv_layers INTEGER,  nb_kernels INTEGER,  nb_filters INTEGER
                       conv_dropout REAL, pool_size INTEGER, kernel_limit INTEGER, nb_linear_layers INTEGER,
                       lin_size INTEGER, lin_dropout REAL ,output_path TEXT, FOREIGN KEY(dataset_name) REFERENCES dataset(dataset_name));
                        
CREATE TABLE dataset (dataset_name TEXT PRIMARY KEY, numb_pdbs INTEGER,input_csv TEXT, error_csv TEXT,tensors TEXT ,pdb_location TEXT,);

CREATE TABLE  model( model_id INTEGER PRIMARY KEY, model_path TEXT NOT NULL, model_accuracy REAL, model_loss REAL);

CREATE TABLE  Pdbs(pdb_id INTEGER PRIMARY KEY,pdb_name TEXT, pdb_chain TEXT, pdb_loss_value REAL);

CREATE TABLE attributions( attr_id INTEGER PRIMARY KEY, attribution_path TEXT,)

/* RELATIONS */

CREATE TABLE trains (user_id INTEGER, config_id INTEGER, PRIMARY KEY( user_id, config_id), FOREIGN KEY (user_id) 
      REFERENCES User user_id),  FOREIGN KEY (config_id) 
      REFERENCES ConfigFile(config_id),primary key(user_id, config_id));

CREATE TABLE interpret(user_id INTEGER, model_id INTEGER, PRIMARY KEY( user_id, model_id), FOREIGN KEY (user_id) 
      REFERENCES User user_id),  FOREIGN KEY (model_id) 
      REFERENCES model(model_id),primary key(user_id, model_id)););

CREATE TABLE is_trained(model_id INTEGER,config_file INTEGER,
            FOREIGN KEY (config_id) REFERENCES ConfigFile(config_id),
            FOREIGN KEY (model_id) REFERENCES model(model_id),primary key(model_id, config_id) );

CREATE TABLE is_interpreted(model_id INTEGER,attr_id INTEGER,
            FOREIGN KEY (attr_id) REFERENCES attributions(attr_id),
            FOREIGN KEY (model_id) REFERENCES model(model_id),primary key(model_id, attr_id) );
