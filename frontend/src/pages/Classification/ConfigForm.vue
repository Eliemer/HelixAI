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
              <label for="name">Configuration Name</label>
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
              <md-input
                v-model="learning_rate"
                type="number"
                step="0.00000000001"
                min="0.000000000001"
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
import { mapGetters, mapActions } from "axios";
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
    addConfigForm() {}
  }
};
</script>
