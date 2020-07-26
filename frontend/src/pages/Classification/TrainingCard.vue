<template>
  <md-card>
    <md-card-header :data-background-color="dataBackgroundColor">
      <h4 class="title">Training</h4>
      <p class="category">Train from submited Model Configuration Files</p>
    </md-card-header>
    <md-card-content>
      <div class="md-layout">
        <div class="md-layout-item md-large-size-100 md-size-100">
          <md-progress-bar md-mode="determinate"></md-progress-bar>
          <h6 class="category" style="text-align:center">Training Progress</h6>
        </div>
      </div>
      <form @submit.prevent="onTrain">
        <md-field>
          <div class="md-layout-item md-large-size-100 md-size-100">
            <label for="configfile">Selected Configuration File</label>
            <md-input v-model="item.config_path"></md-input>
          </div>
        </md-field>
        <div class="md-layout-item md-large-size-100 md-size-100 text-right">
          <md-button type="submit" class="md-raised md-primary"
            >Train</md-button
          >
        </div>
      </form>
    </md-card-content>
  </md-card>
</template>
<script>
import { mapGetters, mapActions } from "vuex";
export default {
  name: "training-card",
  props: ["item", "dataBackgroundColor"],
  data() {
    return {
      progress: null
    };
  },
  methods:{
    ...mapActions(["trainConfig"]),
    start() {
      this.$Progress.start()
    },
    set (num) {
      this.$Progress.set(num)
    },
    increase (num) {
      this.$Progress.increase(num)
    },
    decrease (num) {
      this.$Progress.decrease(num)
    },
    finish () {
      this.$Progress.finish()
    },
    onTrain(event){
      console.log(this.item.config_path);

      this.trainConfig(this.item.config_path);
    }
  }
};
</script>
<style scoped>
.md-progress-spinner {
  margin-top: 5%;
  margin-left: 42%;
  margin-right: 50%;
}
.md-progress-bar {
  display: block;
  margin-top: 5%;
}
</style>
