import { createRouter, createWebHashHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import RegisterStudent from "../components/RegisterStudent.vue";
import SearchComp from "../components/SearchComponent.vue";
import RegisterStaff from "../components/RegisterStaff.vue";
import TestingAPI from "../components/Test.vue";
import DashBoardView from "../views/DashBoardView.vue";
import SubjectView from "../views/SubjectView.vue";
import TicketView from "../views/TicketView.vue";
import TagView from "../views/TagView.vue";
import RoleView from "../views/RoleView.vue";
import RegisterAdmin from "../components/RegisterAdmin.vue";
const routes = [
  { path: "/", name: "home", component: HomeView },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
  { path: "/register", name: "Register", component: RegisterStudent },
  { path: "/enroll", name: "Enroll", component: RegisterStaff },
  { path: "/test", name: "test", component: TestingAPI },
  { path: "/dash", name: "Student dashboard", component: DashBoardView },
  { path: "/tag", name: "tag Page", component: TagView },
  { path: "/role", name: "role Page", component: RoleView },
  {
    path: "/subject/:subject",
    name: "Subject Dashboard",
    component: SubjectView,
  },
  { path: "/ticket/:id", name: "Ticket Page", component: TicketView },
  { path: "/search/:search", name: "Search Page", component: SearchComp },
  {
    path: "/sc-admin-register",
    name: "Register Admin",
    component: RegisterAdmin,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
