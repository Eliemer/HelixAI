import axios from 'axios'

const state = {
    config_files :[],
    user_configs: []
}
const getters = {
    allConfigs: (state) => state.config_files,
    allUserConfigs: (state) => state.user_configs
};
//need to add delete option
const actions = {
    async fetchConfigs({commit}){
        const response = await axios.get('http://127.0.0.1:5000/configs/all')
        commit('setConfigs',response.data)
        //console.log(response.data)
    },
    //Need to change this later to id of logged user 
    async fetchUserConfigs({commit}){
        const response = await axios.get('http://127.0.0.1:5000/configs/user/1')
        commit('setUserConfigs',response.data)
       // console.log(response.data)
    },
    //need also id of logged user
    async addConfig({commit},config_name,dataset,epoch,batch,workers,learning_rate ,
        fuzzy_radius, augment,nb_classes,nb_features,nb_nodes,nb_conv_layers, nb_kernels,
        nb_filters,conv_dropout,pool_size,kernel_limit,nb_linear_layers,lin_size,lin_dropout){
        const response = await axios.post('https://jsonplaceholder.typicode.com/todos',
            {config_name,dataset,epoch,batch,workers,learning_rate ,
                fuzzy_radius, augment,nb_classes,nb_features,nb_nodes,nb_conv_layers, nb_kernels,
                nb_filters,conv_dropout,pool_size,kernel_limit,nb_linear_layers,lin_size,lin_dropout});  
            commit('newConfig',response.data)
        }

}
//changes the state
const mutations = {
    setConfigs:(state,config_files)=>(state.config_files =config_files),
    setUserConfigs:(state,user_configs)=>(state.user_configs =user_configs),
    newConfig:(state, user_configs) =>(state.user_configs.unshift(user_configs))
}

export default {
    state,
    getters,
    actions,
    mutations
}
  