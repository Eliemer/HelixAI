<template>
  <md-card>
    <md-card-header :data-background-color="dataBackgroundColor">
      <h4 class="title">Training</h4>
      <p class="category">Train from submited Model Configuration Files</p>
    </md-card-header>
    <md-card-content>
      <div class="md-layout">
        <div class="md-layout-item md-large-size-100 md-size-100">
          <md-progress-bar md-mode="indeterminate"></md-progress-bar>
          <h6 class="category" style="text-align:center">Training Progress</h6>
        </div>
      </div>
      <form>
        <md-field>
          <div class="md-layout-item md-large-size-100 md-size-100">
            <label for="configfile">Available Configuration Files</label>
            <md-select v-model="configfile">
              <md-option value="form" v-for="con in cons" v-bind:key="con">
                {{ con.name }}
              </md-option>
            </md-select>
          </div>
        </md-field>
        <div class="md-layout-item md-large-size-100 md-size-100 text-right">
          <md-button class="md-raised md-primary">Train</md-button>
        </div>
      </form>
    </md-card-content>
  </md-card>
</template>
<script>
export default {
  name: "training-card",
  props: {
    dataBackgroundColor: {
      type: String,
      default: ""
    }
  },

  data() {
    return {
      progress: null,
      cons: [
        { name: "Ras", value: 1 },
        { name: "Kinase", value: 2 }
      ]
    };
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
