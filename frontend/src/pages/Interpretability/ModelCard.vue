<template>
  <div class="content">
    <md-table
      v-model="allModels"
      :table-header-color="tableHeaderColor"
      @md-selected="onSelect"
    >
      <md-table-row
        slot="md-table-row"
        slot-scope="{ item }"
        md-selectable="single"
      >
        <md-table-cell md-label="Configuration Name">{{
          item.config_path
        }}</md-table-cell>
        <md-table-cell md-label="Model">{{ item.model_path }}</md-table-cell>
        <md-table-cell md-label="Accuracy">{{
          item.model_accuracy
        }}</md-table-cell>
        <md-table-cell md-label="Loss">{{ item.model_loss }}</md-table-cell>
      </md-table-row>
    </md-table>
    <div>
      <form @submit.prevent="onInterpret">
        <md-field>
          <md-input type="text" v-model="selected.model_path" />
        </md-field>
        <div class="text-right">
          <md-button type="submit" class="md-raised md-primary"
            >Interpret Model</md-button
          >
          <md-progress-bar :md-mode="prog"></md-progress-bar>
          <h6 class="category" style="text-align:center">{{ completed }}</h6>
        </div>
      </form>
    </div>
  </div>
</template>
<script>
import { mapGetters, mapActions } from "vuex";
export default {
  name: "model-card",
  props: ["tableHeaderColor"],
  data() {
    return {
      selected: {},
      prog: "determinate",
      completed: ""
    };
  },
  methods: {
    ...mapActions(["fetchModels", "interpretModel"]),
    onSelect(item) {
      this.selected = item;
    },
    onInterpret() {
      this.completed = "Interpreting model...";
      this.prog = "query";
      let path = {
        model_path: this.selected.model_path,
        config_path: this.selected.config_path
      };
      console.log(path);
      let promise = this.interpretModel(path);
      promise.then(value => {
        this.completed = value.completed;
        this.prog = value.prog;
      });
    }
  },
  computed: mapGetters(["allModels"]),
  created() {
    this.fetchModels();
  }
};
</script>
<style scoped>
.md-content {
  max-width: 100%;
  max-height: 200px;
  overflow: auto;
}
</style>