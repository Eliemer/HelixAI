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
export default {
  name: "training-chart",
  components: {
    ChartCard
  },
  data() {
    return {
      latestModelmetrics: {
        data: {
          labels: Array.from(Array(7), (_, i) => i + 1),
          series: [[12, 17, 7, 17, 23, 18, 38]]
        },
        options: {
          lineSmooth: this.$Chartist.Interpolation.cardinal({
            tension: 0
          }),
          height: 300,
          high: 100,
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
  }
};
</script>
