<template>
  <div>
    <md-table v-model="models" :table-header-color="tableHeaderColor" @md-selected="onSelect">
      <md-table-row slot="md-table-row" slot-scope="{ item }" md-selectable="single">
        <md-table-cell md-label="Name">{{ item.name }}</md-table-cell>
        <md-table-cell md-label="Trained Dataset">{{ item.dataset }}</md-table-cell>
        <md-table-cell md-label="Accuracy">{{ item.accuracy }}</md-table-cell>
        <md-table-cell md-label="Loss">{{ item.loss }}</md-table-cell>
      </md-table-row>
    </md-table>
    <div>
      <form @submit="interpretModel">
        <md-field>
          <md-input type="text" v-model="selected.name" />
        </md-field>
        <div class="text-right">
          <md-button type="submit" class="md-raised md-primary">Interpret Model</md-button>
        </div>
      </form>
    </div>
  </div>
</template>
<script>
export default {
  name: "model-card",
  props: ["models", "tableHeaderColor"],
  data() {
    return {
      selected: {}
    };
  },
  methods: {
    onSelect(item) {
      this.selected = item;
    },
    interpretModel(e) {
      e.preventDefault();
      this.selected = null;
    }
  }
};
</script>
