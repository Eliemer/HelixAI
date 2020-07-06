<template>
  <div class="md-layout">
    <div class="md-layout-item md-large-size-100">
      <md-table v-model="lowest_loss_pdb" @md-selected="onSelect">
        <md-table-row
          slot="md-table-row"
          slot-scope="{ item }"
          md-selectable="single"
          md-auto-select
        >
          <md-table-cell>{{ item.config_file }}</md-table-cell>
          <md-table-cell>{{ item.pdb_name }}</md-table-cell>
          <md-table-cell>
            <md-button class="md-just-icon md-simple md-primary">
              <md-icon>3d_rotation</md-icon>
              <md-tooltip md-direction="top">Develop 3D Structures</md-tooltip>
            </md-button>
          </md-table-cell>
        </md-table-row>
      </md-table>
    </div>
  </div>
</template>

<script>
export default {
  name: "structure",
  data() {
    return {
      selected: [],
      lowest_loss_pdb: [
        {
          config_file: "config_file_1",
          pdb_name: "1atp",
          chain: "A",
          dataset: "Kinase",
          loss: 0.00001,
          pdb_path: "/pdb/Kinases/1atp.pdb"
        },
        {
          config_file: "config_file_2",
          pdb_name: "2ayp",
          chain: "A",
          dataset: "Kinase",
          loss: 0.00001,
          pdb_path: "/pdb/Kinases/1atp.pdb"
        },
        {
          config_file: "config_file_1",
          pdb_name: "4pka",
          chain: "E",
          dataset: "K",
          loss: 0.00001,
          pdb_path: "/pdb/Ras/1atp.pdb"
        },
      ]
    };
  },
  methods: {
    onSelect: function(items) {
      this.selected = items;
    }
  }
};
</script>
