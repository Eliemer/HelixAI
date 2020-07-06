<template>
  <div class="content">
    <div class="md-layout">
      <div class="md-layout-item md-large-size-50 md-size-50">
        <config-form
          data-background-color="green"
          v-on:add-config="addConfigForm"
        >
        </config-form>
      </div>
      <div class="md-layout_item md-large-size-50 md-size-50">
        <div class="md-layout-item md-large-size-100 md-size-100">
          <training-card data-background-color="green"></training-card>
        </div>
        <div class="md-layout-item md-large-size-100 md-size-100">
          <md-card>
            <md-card-header data-background-color="orange">
              <h4 class="title">Available Configuration Files</h4>
            </md-card-header>
            <md-card-content>
              <config-table
                v-bind:configs="configs"
                table-header-color="green"
              ></config-table>
            </md-card-content>
          </md-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ConfigForm from "./Classification/ConfigForm.vue";
import TrainingCard from "./Classification/TrainingCard.vue";
import ConfigTable from "./Classification/ConfigTable.vue";

export default {
  components: {
    ConfigForm,
    TrainingCard,
    ConfigTable
  },
  data() {
    return {
      configs: [
        {
          id: 1,
          name: "ras",
          dataset: "Hras KRAS"
        },
        {
          id: 1,
          name: "ras",
          dataset: "Hras KRAS"
        },
        {
          id: 1,
          name: "ras",
          dataset: "Hras KRAS"
        },
        {
          id: 1,
          name: "ras",
          dataset: "Hras KRAS"
        }
      ]
    };
  },
  methods: {
    addConfigForm(newConfig) {
      this.config = [...this.configs, newTodo];
    }
  }
};
</script>
