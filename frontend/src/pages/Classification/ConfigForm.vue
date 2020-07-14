<template>
  <form @submit.prevent="addConfigForm">
    <md-card>
      <md-card-header :data-background-color="dataBackgroundColor">
        <h4 class="title">Model Configuration</h4>
        <p class="category">Configure Neural Network Paramenters</p>
      </md-card-header>

      <md-card-content>
        <div class="md-layout">
          <div class="md-layout-item md-large-size-100 md-size-100">
            <md-field>
              <label for="name">File Name</label>
              <md-input v-model="config_name" type="text"> </md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-large-size-50 md-size-50">
            <md-field>
              <label for="dataset">Dataset</label>
              <md-select v-model="dataset">
                <md-option value="HRAS_KRAS">Hras Kras</md-option>
                <md-option value="Kinases">Kinases</md-option>
                <md-option value="TSG_OG">Oncogenes</md-option>
              </md-select>
            </md-field>
          </div>
          <div class="md-layout-item md-large-size-50 md-size-50">
            <md-field>
              <label>Number of Epochs</label>
              <md-input v-model="epoch" type="number"></md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-large-size-33 md-size-33">
            <md-field>
              <label>Learning Rate</label>
              <md-input v-model="learning_rate" type="number" placeholder="0.000001" step="0.00000000001" min="0.000000000001" max="1"></md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-large-size-33 md-size-33">
            <md-field>
              <label>Linear Dropout Rate</label>
              <md-input v-model="lin_dropout" type="number" step="0.01" min="0.00" max="1"></md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-large-size-33 md-size-33">
            <md-field>
              <label>Convolutional Dropout</label>
              <md-input v-model="conv_dropout" type="number" step="0.01" min="0.00" max="1"></md-input>
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
              <label>Linear Dropout Rate</label>
              <md-input v-model="lin_dropout" type="number"></md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-size-100 text-right">
            <md-card-actions>
              <md-button type="submit" class="md-raised md-primary">
                Create Config File</md-button
              >
            </md-card-actions>
          </div>
        </div>
      </md-card-content>
    </md-card>
  </form>
</template>
<script>
import uuid from "uuid";
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
      config_name: null,
      dataset: null,
      epoch: null,
      batch: null,
      workers: null,
      learning_rate: null,
      fuzzy_radius: null,
      augment: null,

      nb_classes: null,
      nb_features: null,
      nb_nodes: null,

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
    addConfigForm(e) {
      e.preventDefault();

      const newConfig = {
        id: uuid.v4(),
        name: this.name,
        dataset: this.dataset,
        epoch: this.epoch,
        batch: this.batch,
        workers: this.workers,
        learning_rate: this.learning_rate,
        shuffle: true,
        split: [0.7, 0.1, 0.2],
        fuzzy_radius: this.fuzzy_radius,
        augment: this.augment,
        is_weighted: true,
        nb_classes: this.nb_classes,
        nb_features: this.nb_features,
        nb_nodes: this.nb_nodes,
        nb_conv_layers: this.nb_conv_layers,
        nb_kernels: this.nb_kernels,
        nb_filters: this.nb_filters,
        conv_dropout: this.conv_dropout,
        pool_size: this.pool_size,
        kernel_limit: this.kernel_limit,
        nb_linear_layers: this.nb_linear_layers,
        lin_size: this.lin_size,
        lin_dropout: this.lin_dropout
      };
      this.$emit("add-config", newConfig);
      console.log(newConfig);
      this.name = null;
      this.dataset = null;
      this.epoch = null;
      this.batch = null;
      this.workers = null;
      this.learning_rate = null;
      this.fuzzy_radius = null;
      this.augment = null;

      this.nb_classes = null;
      this.nb_features = null;
      this.nb_nodes = null;

      this.nb_conv_layers = null;
      this.nb_kernels = null;
      this.nb_filters = null;
      this.conv_dropout = null;
      this.pool_size = null;
      this.kernel_limit = null;

      this.nb_linear_layers = null;
      this.lin_size = null;
      this.lin_dropout = null;
    }
  }
};
</script>
