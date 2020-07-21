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

    <form>
      <div class="md-layout">
        <div class="md-layout-item md-large-size-50 md-size-50">
          <md-field>
            <label>Upload CSV</label>
            <md-file
              type="file"
              class="form-control"
              id="file"
              name="file"
              accept="text/csv"
              v-on:change="onFileChange"
            />
          </md-field>
        </div>
        <div class="md-layout-item md-large-size-50 md-siz-50 text-right" style="padding-top: 10px;">
          <md-button class="md-primary" @click="upload">Upload</md-button>
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
    ...mapActions(["fetchDatasets"]),
    onFileChange(e) {
      let files = e.target.files || e.dataTransfer.files;
      if (!files.length) return;
      this.createFile(files[0]);
    },
    createFile(file) {
      let reader = new FileReader();
      let vm = this;
      reader.onload = e => {
        vm.file = e.target.result;
      };
      reader.readAsDataURL(file);
    },
    upload() {
      let data = new FormData();
      console.log(document.getElementById("file").files[0]);
      data.append("file", document.getElementById("file").files[0]);
      axios
        .post("http://127.0.0.1:5000/dashboard/", data, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        })
        .then(function() {
          console.log("SUCCESS!!");
        })
        .catch(function() {
          console.log("FAILURE!!");
        });
      this.file = null;
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
</style>