import axios from "axios";
const FileDownload = require("js-file-download");
const state = {
  trainedModels: [],
  metrics: [],
  attributions: [],
  models: []
};
const getters = {
  allTrainedModels: state => state.trainedModels,
  allModels: state => state.models,
  allMetrics: state => state.metrics,
  allAttributions: state => state.attributions
};
//need to add delete option
const actions = {
  async fetchModels({ commit }) {
    const response = await axios.get(
      "http://127.0.0.1:5000/deep_learn/get_models"
    );
    commit("setModels", response.data);
  },

  async trainConfig({ commit }, config_path) {
    let path =
      "http://127.0.0.1:5000/deep_learn/train/config/path/" + config_path;
    const response = await axios.post(path);
    console.log(response.data.metrics); //need to understand how the data is created

    let rte = {
      model_path: response.data.model_path,
      model_details: response.data.model_details,
      completed: "Training Success",
      prog: "determinate"
    };
    let model = {
      config_path: config_path,
      model_accuracy: response.data.model_details.model_accuracy,
      model_id: response.data.model_details.model_id,
      model_loss: response.data.model_details.model_loss,
      model_path: response.data.model_details.model_path,
      model_python_class: response.data.model_details.model_python_class
    };
    console.log(response.data);
    commit("newTrainedModel", response.data);
    commit("newMetrics", rte);
    commit("newModel", model);
    return rte;
  },
  async interpretModel({ commit }, path) {
    let url = `http://127.0.0.1:5000/deep_learn/interpret/config/path/${path.config_path}/model/${path.model_path}`;

    const response = await axios.post(url, path.config_path, path.model_path);
    console.log(response.data);
    let rtr = {
      completed: "Model has been interpreted",
      prog: "determinate"
    };

    commit("newAttributions", response.data);

    return rtr;
  },
  async downloadAttributions({ commit }, form) {
    let url = "http://127.0.0.1:5000/deep_learn/get_pymol_scene";
    const response = await axios({
      method: "post",
      url: url,
      data: form,
      responseType: "blob"
    });
    const ul = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement("a");
    link.href = ul;
    link.setAttribute("download", `${form.get("pdb_id")}.pse`); //or any other extension
    document.body.appendChild(link);
    link.click();
  }
};
//changes the state
const mutations = {
  setTrainedModels: (state, models) => (state.trainedModels = models),
  setModels: (state, models) => (state.models = models),
  setAttributions: (state, attributions) => (state.attributions = attributions),
  newModel: (state, model) => state.models.unshift(model),
  newTrainedModel: (state, model) => state.trainedModels.unshift(model),
  newAttributions:(state,attribution) => state.attributions.unshift(attribution),
  newMetrics: (state, metric) => state.metrics.unshift(metric)
};

export default {
  state,
  getters,
  actions,
  mutations
};
