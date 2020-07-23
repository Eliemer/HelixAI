import axios from 'axios'

const state = {
  trainedModels: [],
  trainedConfigs: [],
  metrics: []
};
const getters = {};
//need to add delete option
const actions = {
  async trainModel({ commit }, config_path) {
    const response = await axios.post(
      "http://127.0.0.1:5000/deep_learn/train/config/path/",
      config_path
    );
    console.log(response);
  }
};
//changes the state
const mutations = {};

export default {
  state,
  getters,
  actions,
  mutations
};
