<template>
  <div class="content">
    <div class="md-layout">
      <div class="md-layout-item md-large-size-50 md-size 50">
        <div class="md-layout-item md-large-size-100 md-size-100">
          <md-card>
            <md-card-header data-background-color="blue">
              <h4 class="title">Trained Models</h4>
            </md-card-header>
            <md-card-content>
              <model-card v-bind:models="models" table-header-color="blue"></model-card>
            </md-card-content>
          </md-card>
        </div>
         <div class="md-layout-item md-large-size-100 md-size-100">
          <md-card>
            <md-card-header data-background-color="blue">
              <h4 class="title">Interpreted Models</h4>
            </md-card-header>
            <md-card-content>
              <interpret-model v-bind:models="models" table-header-color="blue"></interpret-model>
            </md-card-content>
          </md-card>
        </div>

      </div>
      <div class="md-layout-item md-large-size-50 md-size 50">
        <div class="md-layout-item md-large-size-100 md-size 100">
          <md-card>
            <md-card-header data-background-color="blue">
              <h4 class="title">Visualization</h4>
            </md-card-header>
            <md-card-content>
            <d-viewer />
            </md-card-content>
          </md-card>
        
        </div>
      </div>
      
    </div>
  </div>
</template>
<script>
import ModelCard from "./Interpretability/ModelCard.vue";
import InterpretModel from "./Interpretability/InterpretModel.vue";
import DViewer from "./Interpretability/DViewer.vue";
export default {
  components: {
    ModelCard,
    InterpretModel,
    DViewer
  },
  data() {
    return {
      models: [
        {
          id: "1",
          name: "config_file1",
          dataset: "Kinase",
          accuracy: 0.99,
          loss: 0.0001
        },
        {
          id: "2",
          name: "config_file2",
          dataset: "Ras",
          accuracy: 0.97,
          loss: 0.0001
        },
        {
          id: "3",
          name: "config_file3",
          dataset: "TSG/OG",
          accuracy: 0.91,
          loss: 0.0001
        }
      ]
    };
  }
};
</script>
