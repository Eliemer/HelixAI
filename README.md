### What is Helix-AI?
This application is designed to provide insightful observations on protein structures. Our Graphical Convolutional Neural Network can be trained to classify any protein available in the [Protein Data Bank](https://www.rcsb.org/pdb/static.do?p=general_information/about_pdb/index.html) based exclusively on its structural properties, such as:

* type of residue
* coordinates of its C-alpha residues (x,y,z)
* sinusoidal positional encoding of residue index in primary structure
* orientation of sidechain for each C-alpha
* distance of residue to protein's center of mass

Once a model is sufficiently well trained, it can be used to create attribution maps, which are then used as heat-maps that are projected back onto the subject protein, usually the proteins with the lowest loss. These painted proteins can provide incredibly useful insight into what structural features were most important to the classification property. You can read more about model attributions [here](https://ai.googleblog.com/2018/03/the-building-blocks-of-interpretability.html) and this process being applied to proteins [here](https://www.biorxiv.org/content/10.1101/610444v1).
Helix AI is a web application that encapsulates this process and provides the user with a dashboard to manage, configure, and view different models, experiments and hyperparameters. As well as have an embedded PyMol viewer of these painted proteins

### Getting Started
If you're interested in using the model by itself, click [here](https://github.com/Eliemer/GCNN_Lightning). You can also learn more about pytorch and pytorch_lightning [here](https://pytorch.org/) and [here](https://github.com/PytorchLightning/pytorch-lightning), respectively. The python requirements are all included in the `setup.py` script at the root of the project. Simply `cd` into the project root and run `pip install .`. The frontend (Javascript) requirements are included in a `package.json` file. Before installing dependencies, you must install `npm` and `vue-cli` as directed in the Vue.js official webpage [here](https://vuejs.org/). Then simply `cd` into `root/frontend` and run `npm install`.
Once all requirements are met, you must export a few environment variables for flask:
In linux:
```Bash
export FLASK_APP='src'
flask init_db
flask run
```
In Windows powershell:
```
$env:FLASK_APP = \"src\"
flask init_db
flask run
```
This turns the Flask server on to receive requests through the REST endpoints. Important to note that `flask init_db` is only required on the initial setup of the server. Running it a second time will delete all the information previously stored there. Now we turn on the Vue.js frontend:
```Bash
npm run serve
```
### Media
##### Demo
[Demo]()
##### Elevator Pitch
[![](http://img.youtube.com/vi/BE3QCFYqFoo/0.jpg)](http://www.youtube.com/watch?v=BE3QCFYqFoo "Pitch")
