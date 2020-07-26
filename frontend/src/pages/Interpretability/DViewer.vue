<template>
  <div class="content">
    <div class="md-layout">
      <div class="md-layout-item md-large-size-100 md-size-100">
        <md-card>
          <md-card-content>
            <script2 src="https://3Dmol.csb.pitt.edu/build/3Dmol.js"></script2>
            <div
              style="height: 400px; max-width: 400px; position: relative; display: block; margin-left: auto;
  margin-right: auto;"
              class="viewer_3Dmoljs"
              :data-pdb="pdb"
              data-backgroundcolor="0xffffff"
              data-style1="cartoon:color=spectrum"
            ></div>
            <script2>
              setInterval(function() { if ($3Dmol.viewers) if
              ($3Dmol.viewers[0]) { var view = $3Dmol.viewers[0];
              view.rotate(1); } }, 50);
            </script2>
          </md-card-content>
        </md-card>
      </div>
      <div class="md-layout-item md-large-size-100 md-size-100">
        <div>
          <md-table
            v-model="item.pdbs_attributed"
            table-header-color="tableHeaderColor"
            @md-selected="onSelect"
          >
            <md-table-row
              slot="md-table-row"
              slot-scope="{ item }"
              md-selectable="single"
            >
              <md-table-cell md-label="PDB Name">{{
                item.pdb_name
              }}</md-table-cell>
              <md-table-cell md-label="PDB Chain">{{
                item.pdb_chain
              }}</md-table-cell>
              <md-table-cell md-label="PDB Class">{{
                item.pdb_class
              }}</md-table-cell>
              <md-table-cell md-label="Download Structure">
                <md-button class="md-just-icon md-simple md-primary">
                  <md-icon>3d_rotation</md-icon>
                  <md-tooltip md-direction="top"
                    >Download Attributed Structure</md-tooltip
                  >
                </md-button>
              </md-table-cell>
            </md-table-row>
          </md-table>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import Vue from "vue";

export default {
  name: "d-viewer",
  props: ["item"],

  data() {
    return {
      pdb: "2ayp",
      selected: {}
    };
  },
  methods: {
    onSelect(item, event) {
      this.selected = item;
    }
  }
};
</script>
