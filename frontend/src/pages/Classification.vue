<template>
  <div class="content">
    <div class="md-layout">
      <div class="md-layout-item md-large-size-50 md-size-50">
        <config-form
          data-background-color="blue"
          v-on:add-config="addConfigForm"
        >
        </config-form>
      </div>
      <div class="md-layout-item md-large-size-50 md-size-50">
        <div class="md-layout-item md-large-size-100 md-size-100">
          <training-chart></training-chart>
        </div>
        <div class="md-layout-item md-large-size-100 md-size-100">
          <training-card
            data-background-color="blue"
            v-bind:item="item"
          ></training-card>
        </div>
      </div>
      <div class="md-layout-item md-large-size-100 md-size-100">
        <md-card>
          <md-card-header data-background-color="teal">
            <h4 class="title">Available Configuration Files</h4>
          </md-card-header>
          <md-card-content>
            <config-table
              v-bind:configs="configs"
              table-header-color="blue"
              v-on:to-train="getSelected"
            ></config-table>
          </md-card-content>
        </md-card>
      </div>
    </div>
  </div>
</template>

<script>
import ConfigForm from "./Classification/ConfigForm.vue";
import TrainingCard from "./Classification/TrainingCard.vue";
import ConfigTable from "./Classification/ConfigTable.vue";
import TrainingChart from "./Classification/TrainingChart.vue";

export default {
  components: {
    ConfigForm,
    TrainingCard,
    ConfigTable,
    TrainingChart
  },
  data(){
    return {
      item: {}
    };
  },
  methods: {
    getSelected(item){
      this.item = item;
    }
  }
};
</script>
