<template>
  <div class="content">
    <md-content>
      <md-table
        v-model="allConfigs"
        :table-header-color="tableHeaderColor"
        @md-selected="onSelect"
      >
        <md-table-row
          slot="md-table-row"
          slot-scope="{ item }"
          md-selectable="single"
        >
          <md-table-cell md-label="ID">{{ item.config_id }}</md-table-cell>
          <md-table-cell md-label="Name">{{ item.config_path }}</md-table-cell>
        </md-table-row>
      </md-table>
    </md-content>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
  name: "config-table",
  props: ["tableHeaderColor"],
  data() {
    return {
      selected: {}
    };
  },
  methods: {
    ...mapActions(["fetchConfigs"]), //all configs will be feteched this will be changed to all usr configs
    onSelect(item, event) {
      this.selected = item;
      this.$emit("to-train", this.selected);
    }
  },
  computed: mapGetters(["allConfigs"]),
  created() {
    this.fetchConfigs();
  }
};
</script>

<style lang="scss" scoped>
.md-content {
  max-width: 100%;
  max-height: 200px;
  overflow: auto;
}
</style>
