<template>
  <div>
    <md-content>
      <md-table v-model="allConfigs" :table-header-color="tableHeaderColor">
        <md-table-row slot="md-table-row" slot-scope="{ item }">
          <md-table-cell md-label="ID">{{ item.config_id }}</md-table-cell>
          <md-table-cell md-label="Name">{{ item.config_path }}</md-table-cell>
        </md-table-row>
      </md-table>
    </md-content>
  </div>
</template>

<script>
import {mapGetters, mapActions} from 'vuex'
export default {
  name: "config-table",
  props: ["tableHeaderColor"],
  methods: {
    ...mapActions(['fetchConfigs']) //all configs will be feteched this will be changed to all usr configs
  },
  computed: mapGetters(['allConfigs']),
  created(){
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
