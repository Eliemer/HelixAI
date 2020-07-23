<template>
  <div class="content">
    <md-table v-model="allDatasets" :table-header-color="tableHeaderColor">
      <md-table-row slot="md-table-row" slot-scope="{ item }">
        <md-table-cell md-label="ID">{{ item.dataset_id }}</md-table-cell>
        <md-table-cell md-label="Name">{{ item.dataset_name }}</md-table-cell>
        <md-table-cell md-label="Class 1">{{ item.num_pdbs_class1 }}</md-table-cell>
        <md-table-cell md-label="Class 2">{{ item.num_pdbs_class2 }}</md-table-cell>
        <md-table-cell md-label=" Total ">{{ item.num_pdbs_class1 + item.num_pdbs_class2}}</md-table-cell>
      </md-table-row>
    </md-table>

    <form @submit="upload">
      <div class="md-layout">
        <div class="md-layout-item md-large-size-50 md-size-50">
          <input
            type="file"
            id="file"
            ref="file"
            accept="text/csv"
            v-on:change="onFileChange"
          />
        </div>
        <div
          class="md-layout-item md-large-size-50 md-siz-50 text-right"
          style="padding-top: 10px;"
        >
          <md-button type="submit" class="md-primary">Upload</md-button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import axios from "axios";
export default {
  name: "ordered-table",
  props: {
    tableHeaderColor: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      selected: [],
      file: null
    };
  },
  methods: {
    ...mapActions(["fetchDatasets","addDataset"]),
    onFileChange(e) {
      this.file = this.$refs.file.files[0];
    },
    upload() {
      let data = new FormData();
      console.log(this.file);
      data.append("file", this.file);
      this.addDataset(data);
    }
  },
  computed: mapGetters(["allDatasets"]),
  created() {
    this.fetchDatasets();
  }
};
</script>
<style scoped>
.md-content {
  max-width: 100%;
  max-height: 200px;
  overflow: auto;
}
#file{
  margin-top: 20px;
}
</style>