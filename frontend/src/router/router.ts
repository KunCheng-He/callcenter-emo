// 配置路由
export const constantRouterMap = [
  {
    path: "/",
    name: "home",
    component: () => import("../views/HomeView.vue"),
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (About.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import("../views/AboutView.vue"),
  },
  {
    path: "/404",
    name: "404",
    component: () => import("@/views/NoFound.vue"),
  },
  {
    // 任意路由，没有匹配上就跳转 404
    path: "/:pathMatch(.*)*",
    redirect: "/404",
    name: "any",
  },
];
