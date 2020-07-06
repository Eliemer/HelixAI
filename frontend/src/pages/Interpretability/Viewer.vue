<template>
  <div class="content">
    <div class="md-layout">
      <div class="md-layout-item md-large-size-100 md-size-100">
        <vue-player
          src="http://techslides.com/demos/sample-videos/small.mp4"
          title="this is a title"
          v-model="playing"
        ></vue-player>
      </div>
      <div class="md-layout-item md-large-size-100 md-size 100">
        <pdb-to-view></pdb-to-view>
      </div>
    </div>
  </div>
</template>
<script>
import vuePlayer from "@algoz098/vue-player";
import PdbToView from "./PdbToView.vue";
export default {
  name: "viewer",
  components: {
    vuePlayer,
    PdbToView
  }
};
</script>
