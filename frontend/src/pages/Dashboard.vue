<template>
  <div class="content">
    <div class="md-layout">
      <div class="md-layout-item md-large-size-50 md-size-50">
        <md-tooltip md-direction="top">Epochs vs Accuracy</md-tooltip>
        <chart-card
          :chart-data="dailySalesChart.data"
          :chart-options="dailySalesChart.options"
          :chart-type="'Line'"
          data-background-color="blue"
        >
          <template slot="content">
            <h4 class="title">Accuracy of Best Performing Models</h4>
            <p class="category">
              Accuracy per epoch of top models for each dataset
            </p>
          </template>

          <template slot="footer">
            <div class="stats"></div>
          </template>
        </chart-card>
      </div>
      <div class="md-layout-item md-large-size-50 md-size-50">
        <md-tooltip md-direction="top">Epochs vs Loss</md-tooltip>
        <chart-card
          :chart-data="dataCompletedTasksChart.data"
          :chart-options="dataCompletedTasksChart.options"
          :chart-type="'Line'"
          data-background-color="teal"
        >
          <md-tooltip>X-axis: Epochs Y-axis: Loss</md-tooltip>
          <template slot="content">
            <h4 class="title">Loss of Best Performing Models</h4>
            <p class="category">
              Loss per epoch of top models for each dataset
            </p>
          </template>

          <template slot="footer">
            <div class="stats"></div>
          </template>
        </chart-card>
      </div>
      <div class="md-layout-item md-large-size-50 md-size-50">
        <div class="md-layout-item md-large-size-100  md-size-100">
          <stats-card data-background-color="red">
            <template slot="header">
              <md-icon>info_outline</md-icon>
            </template>

            <template slot="content">
              <p class="category">Fixed Issues</p>
              <h3 class="title">75</h3>
            </template>

            <template slot="footer">
              <div class="stats">
                <md-icon>local_offer</md-icon>Tracked from Github
              </div>
            </template>
          </stats-card>
        </div>
        <div class="md-layout-item md-large-size-100 md-size-100">
          <stats-card data-background-color="blue">
            <template slot="header">
              <img
                src="@/assets/img/white_logo.png"
                style="max-width: 70px; max-height: 70px; margin-right: -5px;"
              />
            </template>

            <template slot="content">
              <p class="category">Helix Users</p>
              <h3 class="title">+245</h3>
            </template>

            <template slot="footer">
              <div class="stats"><md-icon>update</md-icon>Just Updated</div>
            </template>
          </stats-card>
        </div>
      </div>
      <div class="md-layout-item md-large-size-50  md-size-50">
        <nav-tabs-card>
          <template slot="content">
            <span class="md-nav-tabs-title">Tasks:</span>
            <md-tabs class="md-accent" md-alignment="left">
              <md-tab id="tab-home" md-label="Todos" md-icon="bug_report">
                <nav-tabs-table></nav-tabs-table>
              </md-tab>

              <md-tab id="tab-pages" md-label="Bugs" md-icon="code"> </md-tab>
            </md-tabs>
          </template>
        </nav-tabs-card>
      </div>
      <div class="md-layout-item md-large-size-100md-size-100">
        <md-card>
          <md-card-header data-background-color="blue">
            <h4 class="title">Available Datasets</h4>
            <p class="category">Datasets available for training</p>
          </md-card-header>
          <md-card-content>
            <ordered-table table-header-color="blue"></ordered-table>
          </md-card-content>
        </md-card>
      </div>
    </div>
  </div>
</template>

<script>
import {
  StatsCard,
  ChartCard,
  NavTabsCard,
  NavTabsTable,
  OrderedTable
} from "@/components";

export default {
  components: {
    StatsCard,
    ChartCard,
    NavTabsCard,
    NavTabsTable,
    OrderedTable
  },
  data() {
    return {
      dailySalesChart: {
        data: {
          labels: Array.from(Array(7), (_, i) => i + 1),
          series: [
            [12, 17, 7, 17, 23, 18, 38],
            [25, 20, 10, 21, 30, 22, 41],
            [9, 10, 22, 16, 23, 34, 55]
          ]
        },
        options: {
          lineSmooth: this.$Chartist.Interpolation.cardinal({
            tension: 0
          }),
          low: 0,
          high: 50, // creative tim: we recommend you to set the high sa the biggest value + something for a better look
          chartPadding: {
            top: 0,
            right: 0,
            bottom: 0,
            left: 0
          }
        }
      },
      dataCompletedTasksChart: {
        data: {
          labels: Array.from(Array(7), (_, i) => i + 1),
          series: [[1.1, 1.6, 1.0, 0.9, 0.73, 0.01, 0.009, 0.001]]
        },

        options: {
          lineSmooth: this.$Chartist.Interpolation.cardinal({
            tension: 0
          }),
          low: 0,
          high: 1.9, // creative tim: we recommend you to set the high sa the biggest value + something for a better look
          fullWidth: true,

          chartPadding: {
            top: 0,
            right: 0,
            bottom: 0,
            left: 0
          }
        }
      },
      emailsSubscriptionChart: {
        data: {
          labels: [
            "Ja",
            "Fe",
            "Ma",
            "Ap",
            "Mai",
            "Ju",
            "Jul",
            "Au",
            "Se",
            "Oc",
            "No",
            "De"
          ],
          series: [[542, 443, 320, 780, 553, 453, 326, 434, 568, 610, 756, 895]]
        },
        options: {
          axisX: {
            showGrid: false
          },
          low: 0,
          high: 1000,
          chartPadding: {
            top: 0,
            right: 5,
            bottom: 0,
            left: 0
          }
        },
        responsiveOptions: [
          [
            "screen and (max-width: 640px)",
            {
              seriesBarDistance: 5,
              axisX: {
                labelInterpolationFnc: function(value) {
                  return value[0];
                }
              }
            }
          ]
        ]
      }
    };
  }
};
</script>
