import axios from "axios";
const state = {
  datasets: []
}
const getters = {
  allDatasets: state => state.datasets
};
const actions = {
  async fetchDatasets({ commit }) {
    const response = await axios.get('http://127.0.0.1:5000/dashboard/datasets')
    commit("setDatasets", response.data);
  },
  async addDataset({ commit }, formData) {
    const response = await axios.post(
      "http://127.0.0.1:5000/dashboard/",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      }
    );
    commit("newDataset", response.data);
  }
};
//changes the state
const mutations = {
  setDatasets: (state, datasets) => (state.datasets = datasets),
  newDataset: (state, dataset) => state.datasets.unshift(dataset)
};

export default {
  state,
  getters,
  actions,
  mutations
}
