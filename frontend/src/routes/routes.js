import DashboardLayout from "@/pages/Layout/DashboardLayout.vue";

import Dashboard from "@/pages/Dashboard.vue";
import UserProfile from "@/pages/UserProfile.vue";
import About from "@/pages/About.vue";
import Classification from "@/pages/Classification.vue";
import Interpretability from "@/pages/Interpretability.vue";
import Notifications from "@/pages/Notifications.vue";
import Login from "@/pages/Login.vue";
const routes = [
  {
    path: "/login",
    name: "Login",
    component: Login
  },
  {
    path: "/about",
    name: "About",
    component: About
  },
  {
    path: "/",
    component: DashboardLayout,
    redirect: "/dashboard",
    children: [
      {
        path: "dashboard",
        name: "Dashboard",
        component: Dashboard
      },
      {
        path: "interpretability",
        name: "Interpretability",
        component: Interpretability
      },
      {
        path: "user",
        name: "User Profile",
        component: UserProfile
      },
      {
        path: "classification",
        name: "Classification",
        component: Classification
      },
      {
        path: "notifications",
        name: "Notifications",
        component: Notifications
      }
    ]
  }
];

export default routes;
