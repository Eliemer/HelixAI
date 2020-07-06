<template>
  <div>
    <md-content class="md-scrollbar">
      <md-table v-model="configs" :table-header-color="tableHeaderColor">
        <md-table-row slot="md-table-row" slot-scope="{ item }">
          <md-table-cell md-label="Name">{{ item.name }}</md-table-cell>
          <md-table-cell md-label="Dataset">{{ item.dataset }}</md-table-cell>
        </md-table-row>
      </md-table>
    </md-content>
  </div>
</template>

<script>
export default {
  name: "config-table",
  props: ["tableHeaderColor", "configs"]
};
</script>

<style lang="scss" scoped>
.md-content {
  max-width: 400px;
  max-height: 200px;
  overflow: auto;
}
</style>
