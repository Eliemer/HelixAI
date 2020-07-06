<template>
  <md-card>
    <div class="md-layout  md-alignment-center">
      <div class="md-layout-item md-large-size-100 md-size-100">
        <div class="md-card-media">
          <img
            src="@/assets/img/logo_transparent_background.png"
            alt="Logo"
            style="display: block;
                    margin-left:20%;
                    width: 50%;"
          />
        </div>
        <div class="md-content">
          <h2 class="category text-gray" style="text-align:center;">
            Brought to you by The University of Puerto Rico at Mayaguez
          </h2>
          <h3 class="card-title" style="text-align:center;">About Us</h3>
          <h4
            class="card-description"
            style="display: inline-block;
                    text-align:center;
                    margin-left:25%;
                    margin-right:25%;
                    color: black;"
          >
            Our team at the University of Puerto Rico is happy to bring you
            Helix. Our goal with Helix is to facilitate scientific research by
            hiding away all the necessary engineering code required to set up a
            a deep learning application, while also providing quality metrics
            and interpretable results which describe how their experiment
            performed. Clients would be able to select a deep learning
            architecture from a drop-down menu, select the hyperparameters of
            the experiment and provide a dataset. With only this, our
            application will take care of training, testing, logging
            performance, and creating interpretable visualizations for the user.
          </h4>
        </div>
      </div>
      <div class="md-layout-item md-large-size-33 md-size-33">
        <md-card class="md-card-profile" style="padding-top:30%">
          <div class="md-card-avatar">
            <img class="img" src="@/assets/img/faces/marc.jpg" />
          </div>

          <md-card-content>
            <h6 class="category text-gray">CEO / Co-Founder</h6>
            <h4 class="card-title">Alec Thompson</h4>
            <p class="card-description">
              Don't be scared of the truth because we need to restart the human
              foundation in truth And I love you like Kanye loves Kanye I love
              Rick Owens’ bed design but the back is...
            </p>
            <md-button class="md-round md-success">Follow</md-button>
          </md-card-content>
        </md-card>
      </div>
      <div class="md-layout-item md-large-size-33 md-size-33">
        <md-card class="md-card-profile" style="padding-top:30%">
          <div class="md-card-avatar">
            <img class="img" src="@/assets/img/faces/marc.jpg" />
          </div>

          <md-card-content>
            <h6 class="category text-gray">CEO / Co-Founder</h6>
            <h4 class="card-title">Alec Thompson</h4>
            <p class="card-description">
              Don't be scared of the truth because we need to restart the human
              foundation in truth And I love you like Kanye loves Kanye I love
              Rick Owens’ bed design but the back is...
            </p>
            <md-button class="md-round md-success">Follow</md-button>
          </md-card-content>
        </md-card>
      </div>
      <content-footer v-if="!$route.meta.hideFooter"></content-footer>
    </div>
  </md-card>
</template>
<script>
import ContentFooter from "./Layout/ContentFooter.vue";
export default {
  name: "about",
  props: {
    HelixLogo: {
      type: String,
      default: require("@/assets/img/logo_transparent_background.png")
    }
  },
  components: {
    ContentFooter
  }
};
</script>
