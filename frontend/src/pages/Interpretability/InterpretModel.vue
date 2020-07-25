<template>
  <div>
    <md-table
      v-model="attributions"
      :table-header-color="tableHeaderColor"
      @md-selected="onSelect"
    >
      <md-table-row
        slot="md-table-row"
        slot-scope="{ item }"
        md-selectable="single"
      >
        <md-table-cell md-label="Attributed Model">{{
          item.attribution_name
        }}</md-table-cell>
        <md-table-cell md-label="Path to Attributions">
          {{ item.attribution_path }}
        </md-table-cell>
        <md-table-cell md-label="PDBS Attributed">
          {{ item.pdbs_attributed.length }}
        </md-table-cell>
        <md-table-cell md-label="Loss">{{ item.loss }}</md-table-cell>
      </md-table-row>
    </md-table>
  </div>
</template>
<script>
export default {
  name: "interpret-model",
  props: ["tableHeaderColor"],
  data() {
    return {
      selected: {},
      attributions: [
        {
          attribution_name: "config_file1",
          attribution_path: "/attributions.npz",
          pdbs_attributed: [
            {
              pdb_name: "4q9z",
              pdb_chain: "A",
              pdb_class: 0
            }
          ]
        }
      ]
    };
  },
  methods: {
    onSelect(item, event) {
      this.selected = item;
      this.$emit("to-interpret", this.selected);
      this.$forceUpdate();
    },
    interpretModel(e) {
      e.preventDefault();
      this.selected = null;
    }
  }
};
</script>
