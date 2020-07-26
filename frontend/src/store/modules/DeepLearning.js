import axios from "axios";

const state = {
  trainModels: [],
  metrics: [],
  attributions: []
};
const getters = {
  allInterpretedModels: state => state.interpreted,
  allTrainedModels: state => state.trainedModels
};
//need to add delete option
const actions = {
  async fetchTrainedModels({ commit }) {
    const response = await axios.get("htto://127.0.0.1:5000/");
    commit("setTrainedModels", response.data);
  },
  async trainConfig({ commit }, config_path) {
    const response = await axios.post(
      "http://127.0.0.1:5000/deep_learn/train/config/path/",
      config_path
    );
    console.log(response.data); //need to understand how the data is created
  },
  async interpretModel({ commit }, { config_path, model_path }) {
    const response = await axios.post(
      "http://127.0.0.1:5000/deep_learn/interpret",
      { config_path, model_path }
    );
    console.log(response.data);
  }
};
//changes the state
const mutations = {
  setTrainedModels: (state, models) => (state.trainedModels = models),
  newTrainedModel: (state, model) => state.trainedModels.unshift(model),
  setAttributions: (state, attributions) => (state.attributions = attributions)
};

export default {
  state,
  getters,
  actions,
  mutations
};
