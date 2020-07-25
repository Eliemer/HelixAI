<template>
  <md-card class="md-card-profile">
    <div class="md-card-avatar">
      <img class="img" :src="cardUserImage" />
    </div>

    <md-card-content>
      <h6 class="category text-gray">Work Position</h6>
      <h4 class="card-title">User</h4>
      <p class="card-description">
        This is Where you would put yout information or a deep insightfull quote
      </p>
      <md-button class="md-round md-primary">Github</md-button>
    </md-card-content>
  </md-card>
</template>
<script>
export default {
  name: "user-card",
  props: {
    cardUserImage: {
      type: String,
      default: require("@/assets/img/faces/user.png")
    }
  },
  data() {
    return {};
  }
};
</script>
<style></style>
