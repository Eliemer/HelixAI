<template>
  <div class="content">
    <div class="md-layout md-gutter md-alignment-center">
      <div class="md-layout-item md-large-size-33  md-size-33">
        <login-card> </login-card>
      </div>
    </div>
  </div>
</template>
<script>
import LoginCard from "./UserProfile/LoginCard.vue";
export default {
  name: "Login",
  components: {
    LoginCard
  }
};
</script>
