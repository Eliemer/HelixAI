<template>
  <div class="content">
    <div class="md-layout">
      <div class="md-layout-item md-large-size-50 md-size-50">
        <md-card>
          <md-card-header data-background-color="green">
            <h4 class="title">Trained Models</h4>
          </md-card-header>
          <md-card-content>
            <model-card
              v-bind:models="models"
              table-header-color="green"
            ></model-card>
          </md-card-content>
        </md-card>
      </div>
      <div class="md-layout-item md-large-size-50 md-size-50">
        <interpret-nav-tab></interpret-nav-tab>
      </div>
    </div>
  </div>
</template>
<script>
import ModelCard from "./Interpretability/ModelCard.vue";
import InterpretNavTab from "./Interpretability/InterpretNavTab.vue";
export default {
  components: {
    ModelCard,
    InterpretNavTab
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
