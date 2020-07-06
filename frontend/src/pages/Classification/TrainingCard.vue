<template>
  <div class="md-layout">
    <md-card>
      <md-card-header :data-background-color="dataBackgroundColor">
        <h4 class="title">Training</h4>
        <p class="category">Train from submited Model Configuration Files</p>
      </md-card-header>
      <div class="md-layout-item md-large-50 md-size 100">
        <div class="md-layout-item md-large-50 md-size 50">
          <md-progress-spinner
            :md-diameter="100"
            :md-stroke="10"
            md-mode="determinate"
          ></md-progress-spinner>
          <h6 class="category" style="text-align:center">Training Progress</h6>
        </div>
        <div class="md-layout-item md-large-50 md-size 100">
          <div class="md-layout-item md-large-50 md-size 50">
            <form>
              <md-card-header
                :data-background-color="dataBackgroundColor"
                style="margin-top:10%; margin-bottom: 5%;"
              >
                <h4 class="title">Training</h4>
                <p class="category">
                  Train from submited Model Configuration Files
                </p>
              </md-card-header>

              <md-field>
                <div class="md-layout-item md-size-100">
                  <label for="configfile">Available Configuration Files</label>
                  <md-select v-model="configfile">
                    <md-option
                      value="form"
                      v-for="con in cons"
                      v-bind:key="con"
                    >
                      {{ con.name }}
                    </md-option>
                  </md-select>
                </div>
              </md-field>
              <div class="md-layout-item md-size-100 text-right">
                <md-button class="md-raised md-success">Train</md-button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </md-card>
  </div>
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
