import Vue from 'vue';
import Router from 'vue-router';
import DefaultTargets from '../components/DefaultTargets.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/ping',
      name: 'DefaultTargets',
      component: DefaultTargets,
    },
  ],
});
