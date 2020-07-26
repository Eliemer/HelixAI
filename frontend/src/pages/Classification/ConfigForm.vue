<template>
  <form @submit.prevent="createConfig">
    <md-card>
      <md-card-header :data-background-color="dataBackgroundColor">
        <h4 class="title">Model Configuration</h4>
        <p class="category">Configure Neural Network Paramenters</p>
      </md-card-header>

      <md-card-content>
        <div class="md-layout">
          <div class="md-layout-item md-large-size-100 md-size-100">
            <md-field>
              <label for="name">Configuration Name</label>
              <md-input v-model="name" type="text"></md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-large-size-50 md-size-50">
            <md-field>
              <label>Dataset</label>
              <md-select v-model="dataset">
                <md-option
                  v-for="data in allDatasets"
                  v-bind:key="data.id"
                  :value="data.input_csv"
                  >{{ data.dataset_name }}</md-option
                >
              </md-select>
            </md-field>
          </div>
          <div class="md-layout-item md-large-size-50 md-size-50">
            <md-field>
              <label>Number of Epochs</label>
              <md-input v-model="epochs" type="number"></md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-large-size-33 md-size-33">
            <md-field>
              <label>Learning Rate</label>
              <md-input
                v-model="learning_rate"
                type="number"
                step="0.0000000001"
                min="0.00"
                max="1"
              ></md-input>
              <md-tooltip>values of the form 0.0001</md-tooltip>
            </md-field>
          </div>
          <div class="md-layout-item md-large-size-33 md-size-33">
            <md-field>
              <label>Linear Dropout Rate</label>
              <md-input
                v-model="lin_dropout"
                type="number"
                step="0.01"
                min="0.00"
                max="1"
              ></md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-large-size-33 md-size-33">
            <md-field>
              <label>Convolutional Dropout</label>
              <md-input
                v-model="conv_dropout"
                type="number"
                step="0.01"
                min="0.00"
                max="1"
              ></md-input>
              <md-tooltip>Convolutional Dropout rate</md-tooltip>
            </md-field>
          </div>
          <div class="md-layout-item md-large-size-33 md-size-33">
            <md-field>
              <label>Fuzzy Radius</label>
              <md-input
                v-model="fuzzy_radius"
                type="number"
                step="0.01"
                min="0.00"
                max="1"
              ></md-input>
              <md-tooltip>Convolutional Dropout rate</md-tooltip>
            </md-field>
          </div>
          <div class="md-layout-item md-small-size-100 md-size-50">
            <md-field>
              <label>Batch Size</label>
              <md-input v-model="batch" type="number"></md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-small-size-100 md-size-50">
            <md-field>
              <label>Data Augmentation</label>
              <md-input v-model="augment" type="number"></md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-small-size-100 md-size-50">
            <md-field>
              <label>Number of Workers</label>
              <md-input v-model="workers" type="number"></md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-large-size-50 md-size-50">
            <md-field>
              <label>Number of Linear Layers</label>
              <md-input v-model="nb_linear_layers" type="number"></md-input>
            </md-field>
          </div>
        </div>

        <div class="md-layout">
          <div class="md-layout-item md-small-size-100 md-size-33">
            <md-field>
              <label>Features</label>
              <md-input v-model="nb_features" type="number"></md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-small-size-100 md-size-33">
            <md-field>
              <label>Classes</label>
              <md-input v-model="nb_classes" type="number"></md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-small-size-100 md-size-33">
            <md-field>
              <label>Number of Nodes</label>
              <md-input v-model="nb_nodes" type="number"></md-input>
            </md-field>
          </div>

          <div class="md-layout-item md-small-size-100 md-size-33">
            <md-field>
              <label>Number of Kernels</label>
              <md-input v-model="nb_kernels" type="number"></md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-small-size-100 md-size-33">
            <md-field>
              <label>Number of Filters</label>
              <md-input v-model="nb_filters" type="float"></md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-large-size-33 md-size-33">
            <md-field>
              <label>Convolutional Layers</label>
              <md-input v-model="nb_conv_layers" type="number"></md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-small-size-100 md-size-33">
            <md-field>
              <label>Size of Pooling Layers</label>
              <md-input v-model="pool_size" type="number"></md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-small-size-100 md-size-33">
            <md-field>
              <label>Size of Linear Layer</label>
              <md-input v-model="lin_size" type="number"></md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-small-size-100 md-size-33">
            <md-field>
              <label>Kernel Limit</label>
              <md-input v-model="kernel_limit" type="number"></md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-size-100 text-right">
            <md-card-actions>
              <md-button type="submit" class="md-raised md-primary">Create Config File</md-button>
            </md-card-actions>
          </div>
        </div>
      </md-card-content>
    </md-card>
  </form>
</template>
<script>
import { mapGetters, mapActions } from "vuex";
export default {
  name: "config-form",
  props: {
    dataBackgroundColor: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
    name: null,
      dataset: null,
      epochs: null,
      batch: null,
      workers: null,
      learning_rate: null,
      fuzzy_radius: null,
      augment: null,

      nb_classes: null,
      nb_features: null,
      nb_nodes: null,
      input_csv: null,
      nb_conv_layers: null,
      nb_kernels: null,
      nb_filters: null,
      conv_dropout: null,
      pool_size: null,
      kernel_limit: null,

      nb_linear_layers: null,
      lin_size: null,
      lin_dropout: null
    };
  },
  methods: {
    ...mapActions(["addConfig", "fetchConfigs"]),
    createConfig() {
      this.input_csv = this.dataset;
      let config = {
        name: this.name,
        dataset: this.dataset,
        epochs: parseInt(this.epochs),
        batch: parseInt(this.batch),
        workers: parseInt(this.workers),
        learning_rate: parseFloat(this.learning_rate),
        fuzzy_radius: parseFloat(this.learning_rate),
        augment: parseInt(this.augment),

        nb_classes: parseInt(this.nb_classes),
        nb_features: parseInt(this.nb_features),
        nb_nodes: parseInt(this.nb_nodes),
        input_csv: this.input_csv,
        nb_conv_layers: parseInt(this.nb_conv_layers),
        nb_kernels: parseInt(this.nb_kernels),
        nb_filters: parseInt(this.nb_filters),
        conv_dropout: parseFloat(this.conv_dropout),
        pool_size: parseInt(this.pool_size),
        kernel_limit: parseInt(this.kernel_limit),

        nb_linear_layers: parseInt(this.nb_linear_layers),
        lin_size: parseInt(this.lin_size),
        lin_dropout: parseFloat(this.lin_dropout),
        shuffle: true,
        is_weighted: true,
        split: [0.7, 0.1, 0.2],
        error_csv: "dummy_error.csv",
        tensors: "",
        pdb: "",
        output_name: ""
      };
      console.log(config);
      this.addConfig(config);

      this.name = null;
      this.dataset = null;
      this.epochs = null;
      this.batch = null;
      this.workers = null;
      this.learning_rate = null;
      this.augment = null;
      this.input_csv = null;
      this.nb_classes = null;
      this.nb_features = null;
      this.nb_nodes = null;
      this.nb_conv_layers = null;
      this.nb_kernels = null;
      this.nb_filters = null;
      this.conv_dropout = null;
      this.pool_size = null;
      this.kernel_limit = null;
      this.fuzzy_radius = null;
      this.nb_linear_layers = null;
      this.lin_size = null;
      this.lin_dropouy = null;

      this.$forceUpdate();
    }
  },
  computed: mapGetters(["allDatasets", "allConfigs"]),
  mounted(){
    this.fetchConfigs();
  }
};
</script>
