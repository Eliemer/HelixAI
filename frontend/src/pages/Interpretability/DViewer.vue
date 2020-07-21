<template>
  <div class="md-layout">
    <div class="md-layout-item md-large-size-100 md-size-100">
      <div class=" md-header"> PDB NAME </div>


      <div class=" md-header">Attributions for PDB Ne </div>
      <div class="images" v-viewer="{movable: false}">
        <img
          src="@/assets/img/logo.png"
          style="max-width: 100px; max-height: 100px; display: block;
                 margin-left: auto;
                 margin-right: auto;"
        />
      </div>
      <structure />
       
    </div>
  </div>
</template>
<script>
import Vue from "vue";
import "viewerjs/dist/viewer.css";
import Viewer from "v-viewer";
import Structure from './Structure.vue'
Vue.use(Viewer);
export default {
  name: "d-viewer",
  components: {
    Structure
  },
  data() {
    return {
      pdb: "2ayp",
      images: ["/assets/img/logo.png", "../assets/img/face.png"]
    };
  }
};
</script>
