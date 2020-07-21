import axios from 'axios'
const state = {
    datasets: [

    ]
}
const getters = {
    allDatasets: (state) => state.datasets
};
const actions = {
    async fetchDatasets({ commit }) {
        const response = await axios.get('http://127.0.0.1:5000/dashboard/datasets')
        commit('setDatasets', response.data)
        console.log(response.data)
    },
    async addDataset({ commit }, formData, dataset_name) {

        const response = await axios.post('http://127.0.0.1:5000/dashboard/', formData, dataset_name,
            {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }).then(function () { console.log("Succes") }
            ).catch(error => {
                console.log((error.response || {}).data);
                return false;
            })
        console.log(response.data)


    }

}
//changes the state
const mutations = {
    setDatasets: (state, datasets) => (state.datasets = datasets),
    newDataset: (state, datasets) => (state.datasets.unshift(datasets))
}

export default {
    state,
    getters,
    actions,
    mutations
}
