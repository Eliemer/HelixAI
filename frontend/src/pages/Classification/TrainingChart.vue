<template>
  <div class="content">
    <div class="md-layout">
      <chart-card
        :chart-data="latestModelmetrics.data"
        :chart-options="latestModelmetrics.options"
        :chart-type="'Line'"
        data-background-color="blue"
      >
        <template slot="content">
          <h4 class="title">Latest Trained Model Metrics</h4>
          <p class="category"></p>
        </template>

        <template slot="footer">
          <div class="stats">
            <md-icon>access_time</md-icon>
          </div>
        </template>
      </chart-card>
    </div>
  </div>
</template>

<script>
import { ChartCard } from "@/components";
import { mapGetters, mapActions } from "vuex";
export default {
  name: "training-chart",
  components: {
    ChartCard
  },
  data() {
    return {
      lable_size: null,
      latestModelmetrics: {
        data: {
          labels: [],
          series: []
        },
        options: {
          lineSmooth: this.$Chartist.Interpolation.cardinal({
            tension: 0
          }),
          height: 300,
          high: 2,
          low: 0,

          chartPadding: {
            top: 0,
            right: 0,
            bottom: 0,
            left: 0
          }
        }
      }
    };
  },
  computed: mapGetters(["allTrainedModels"]),
  created() {
    this.label_size = (this.allTrainedModels[0].metrics.length - 1) / 3;
    this.latestModelmetrics.data.labels.push(
      Array.from(Array(this.lable_size), (_, i) => i + 1)
    );
    let train = [];
    let test = [];
    let val = [];
    let metrics = this.allTrainedModels[0].metrics;
    console.log(metrics.length)
    for (let i = 0; i < metrics.length - 1; i = i + 3) {
      val.push(metrics[i + 1].val_acc_mean);
      train.push(metrics[i].train_acc);
    }
    this.latestModelmetrics.data.series.push(train);
    this.latestModelmetrics.data.series.push(val);

    console.log(this.latestModelmetrics.data.series);
  }
};
</script>
