<template>
  <md-toolbar md-elevation="0" class="md-transparent">
    <div class="md-toolbar-row">
      <div class="md-toolbar-section-start">
        <h3 class="md-title">{{ $route.name }}</h3>
      </div>
      <div class="md-toolbar-section-end">
        <md-button
          class="md-just-icon md-simple md-toolbar-toggle"
          :class="{ toggled: $sidebar.showSidebar }"
          @click="toggleSidebar"
        >
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
        </md-button>

        <div class="md-collapse">
          <md-list>
            <md-list-item href="#/">
              <i class="material-icons">dashboard</i>
              <p class="hidden-lg hidden-md">Dashboard</p>
            </md-list-item>

            <li class="md-list-item">
              <a
                class="md-list-item-router md-list-item-container md-button-clean dropdown"
              >
                <div class="md-list-item-content">
                  <drop-down>
                    <md-button
                      slot="title"
                      class="md-button md-just-icon md-simple"
                      data-toggle="dropdown"
                    >
                      <md-icon>notifications</md-icon>
                      <p class="hidden-lg hidden-md">Notifications</p>
                    </md-button>
                    <ul class="dropdown-menu dropdown-menu-right"></ul>
                  </drop-down>
                </div>
              </a>
            </li>

            <md-list-item href="#/user">
              <i class="material-icons">person</i>
              <p class="hidden-lg hidden-md">Profile</p>
            </md-list-item>
          </md-list>
        </div>
      </div>
    </div>
  </md-toolbar>
</template>

<script>
export default {
  data() {
    return {
      selectedEmployee: null,
      employees: [
        "Jim Halpert",
        "Dwight Schrute",
        "Michael Scott",
        "Pam Beesly",
        "Angela Martin",
        "Kelly Kapoor",
        "Ryan Howard",
        "Kevin Malone"
      ]
    };
  },
  methods: {
    toggleSidebar() {
      this.$sidebar.displaySidebar(!this.$sidebar.showSidebar);
    }
  }
};
</script>

<style lang="css"></style>
