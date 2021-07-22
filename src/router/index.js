import Vue from 'vue';
import Router from 'vue-router';
import TestPage from '../components/TestPage.vue';
import DefaultTargets from '../components/DefaultTargets.vue';
import TargetCard from '../components/TargetCard.vue';
import FormTest from '../components/TargetForm.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'TestPage',
      component: TestPage,
    },
    {
      path: '/ping',
      name: 'DefaultTargets',
      component: DefaultTargets,
    },
    {
      path: '/formtest',
      name: 'FormTest',
      component: FormTest,
    },
    {
      path: '/target/:id',
      name: 'targetCard',
      component: TargetCard,
    },
  ],
});
