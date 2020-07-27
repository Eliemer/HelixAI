<template>
  <div class="content" style="margin-top: 35%;">
    <md-card class="md-card-profile">
      <div class="md-card-avatar">
        <img class="img" :src="EisLogo" />
      </div>
      <md-card-content>
        <h3>Helix AI</h3>
        <div class="md-layout-item md-large-size-100 md-size-100">
          <md-field>
            <label>User Name</label>
            <md-input v-model="username" type="text"></md-input>
          </md-field>
        </div>
        <div class="md-layout-item md-large-size-100 md-size-100">
          <md-field>
            <label>Password</label>
            <md-input v-model="password" type="password"></md-input>
          </md-field>
        </div>
        <md-button class="md-round md-primary" @click.native="onLogin"
          >>Login</md-button
        >
        <md-button class="md-round md-primary">Register</md-button>
      </md-card-content>
    </md-card>
  </div>
</template>
<script>
export default {
  name: "login-card",

  props: {
    EisLogo: {
      type: String,
      default: require("@/assets/img/logo.png")
    }
  },
  data() {
    return {
      username: null,
      password: null
    };
  },
  methods: {
    onLogin(event) {
      this.$router.push("/dashboard");
    }
  }
};
</script>
