<template>
  <div class="content">
    <div class="md-layout">
      <div class="md-layout-item md-large-size-100 md-size-100">
        <md-field>
          <div class="md-layout-item md-size-100">
            <label for="configfile">Interpreted Configuration Files</label>
            <md-select v-model="configfile">
              <md-option
                v-for="a in availablePDBs"
                v-bind:key="a"
                v-bind:value="a.config_name"
              >
                {{ a.config_name }}
              </md-option>
            </md-select>
          </div>
        </md-field>
        <span>Selected: {{ configfile }}</span>
      </div>
      <div class="md-layout-item md-large-size-100 md-size-100">
        <md-table
          v-for="a in availablePDBs"
          v-bind:key="a.config_name"
          :table-header-color="tableHeaderColor"
        >
          <md-table-row slot="md-table-row" slot-scope="{ item }">
            <md-table-cell md-label="PDB Name">{{
              item.pdb_name
            }}</md-table-cell>
            <md-table-cell md-label="PDB Chain">
              {{ item.pdb_chain }}
            </md-table-cell>
          </md-table-row>
        </md-table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "pdb-to-view",
  props: {
    tableHeaderColor: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      selected: [],
      configfile: "",
      av: [],
      availablePDBs: [
        {
          config_name: "config_1",
          PDBS: [
            { pdb_name: "1atp", pdb_chain: "A", available: true },
            { pdb_name: "2ayp", pdb_chain: "E", available: true },
            { pdb_name: "1pka", pdb_chain: "A", available: true }
          ]
        },
        {
          config_name: "config_2",
          PDBS: [
            { pdb_name: "1atp", pdb_chain: "A", available: true },
            { pdb_name: "2ayp", pdb_chain: "E", available: true },
            { pdb_name: "1pka", pdb_chain: "A", available: true }
          ]
        }
      ]
    };
  },
  methods: {
    getAvailablePDB(e) {
      e.preventDefault();
      for (let data in this.availablePDBs) {
        if (data.config_name == this.configfile) {
          this.av = this.data.PDBS;
        }
      }
      return this.av;
    }
  }
};
</script>
