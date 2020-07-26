import Vuex from "vuex";
import Vue from "vue";
import Datasets from "./modules/Datasets";
import Configs from "./modules/Configs";
import DeepLearning from "./modules/DeepLearning";
Vue.use(Vuex);

//
export default new Vuex.Store({
  modules: {
    Datasets,
    Configs,
    DeepLearning
  }
});
