<template>
  <div>
    <md-table
      v-model="models"
      :table-header-color="tableHeaderColor"
      @md-selected="onSelect"
    >
      <md-table-row
        slot="md-table-row"
        slot-scope="{ item }"
        md-selectable="single"
      >
        <md-table-cell md-label="Name">{{ item.name }}</md-table-cell>
        <md-table-cell md-label="Trained Dataset">
          {{ item.dataset }}
        </md-table-cell>
        <md-table-cell md-label="Accuracy">
          {{ item.accuracy }}
        </md-table-cell>
        <md-table-cell md-label="Loss">{{ item.loss }}</md-table-cell>
      </md-table-row>
    </md-table>
  </div>
</template>
<script>
export default {
  name: "interpret-model",
  props: ["models", "tableHeaderColor"],
  data() {
    return {
      selected: {}
    };
  },
  methods: {
    onSelect(item, event) {
      this.selected = item;
      this.$emit("to-interpret", this.selected);
    },
    interpretModel(e) {
      e.preventDefault();
      this.selected = null;
    }
  }
};
</script>
