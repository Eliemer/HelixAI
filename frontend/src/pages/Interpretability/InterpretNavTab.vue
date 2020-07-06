<template>
  <div class="content">
    <md-card class="md-card-nav-tabs">
      <md-card-content>
        <span class="md-nav-tabs-title">Tasks:</span>
        <md-tabs class="md-success" md-alignment="left">
          <md-tab id="tab-home" md-label="PDBS" md-icon="bug_report">
            <structure></structure>
          </md-tab>
          <md-tab id="tab-pages" md-label="3D View" md-icon="code"> 
            <viewer></viewer>
          </md-tab>

          <md-tab
            id="tab-posts"
            md-label="Attributions"
            md-icon="cloud"
          ></md-tab>
        </md-tabs>
      </md-card-content>
    </md-card>
  </div>
</template>

<script>
import Structure from "./Structure.vue";
import Viewer from "./Viewer.vue"
export default {
  name: "interpret-nav-tab",
  components: {
    Structure,
    Viewer
  }
};
</script>
