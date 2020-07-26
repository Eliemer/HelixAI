import axios from "axios";

const state = {
  trainedModels: [],
  metrics: [],
  attributions: []
};
const getters = {
  allInterpretedModels: state => state.interpreted,
  allTrainedModels: state => state.trainedModels,
  allMetrics: state => state.metrics
};
//need to add delete option
const actions = {
  async fetchTrainedModels({ commit }) {
    const response = await axios.get("htto://127.0.0.1:5000/");
    commit("setTrainedModels", response.data);
  },

  async trainConfig({ commit }, config_path,completed) {
    let path =
      "http://127.0.0.1:5000/deep_learn/train/config/path/" + config_path;
    const response = await axios.post(path);
    console.log(response.data.metrics); //need to understand how the data is created
    completed = "Finished";
    let rte = {
      model_path: response.data.model_path,
      model_details: response.data.model_details,
      completed: completed
    };
    commit("newTrainedModel", response.data);
    commit("newMetrics", rte);
    return rte;
  },
  async interpretModel({ commit }, { config_path, model_path }) {
    const response = await axios.post(
      "http://127.0.0.1:5000/deep_learn/interpret",
      { config_path, model_path }
    );
    commit("newTrainedModel", response.data);
    console.log(response.data.metrics);
    return response.data.metrics;
  }
};
//changes the state
const mutations = {
  setTrainedModels: (state, models) => (state.trainedModels = models),
  newTrainedModel: (state, model) => state.trainedModels.unshift(model),
  setAttributions: (state, attributions) => (state.attributions = attributions),
  newMetrics: (state, metric) => state.metrics.unshift(metric)
};

export default {
  state,
  getters,
  actions,
  mutations
};
