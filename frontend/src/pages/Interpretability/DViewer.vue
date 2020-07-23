<template>
  <div class="md-layout">
    <div class="md-layout-item md-large-size-100 md-size-100">
      <div class=" md-header">PDB NAME: {{ pdb }}</div>
      <script2
        src="https://cdnjs.cloudflare.com/ajax/libs/3Dmol/1.4.0/3Dmol-min.js"
      ></script2>
      <div
        style="height: 400px; width: 400px; position: relative;"
        class="viewer_3Dmoljs"
        :data-pdb="pdb"
        data-backgroundcolor="0xffffff"
        data-style1="cartoon:color=spectrum"
      ></div>
      <div class=" md-header">Attributions for : {{ pdb }}</div>
      <div class="images" v-viewer="{ movable: false }">
        <img
          src="@/assets/img/4q9z_a.png"
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
import Structure from "./Structure.vue";
Vue.use(Viewer);
export default {
  name: "d-viewer",
  components: {
    Structure
  },
  data() {
    return {
      pdb: "4Q9Z",
      images: ["/assets/img/logo.png", "../assets/img/face.png"]
    };
  }
};
</script>
