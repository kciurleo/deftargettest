<template>
  <div class="targets container">
    <h2 class="subtitle is-3">
    Check out these targets
    </h2>
    <TargetForm />
    <div class="columns is-multiline">
      <div v-for="target in targlist" :target="target" :key="target.name"
      class="column is-one-quarter">
        <TargetCard :target="target" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import TargetForm from '@/components/TargetForm.vue';
import TargetCard from '@/components/TargetCard.vue';

export default {
  name: 'DefaultTargets',
  components: {
    TargetCard, TargetForm,
  },
  data() {
    return {
      target: {},
      targlist: '',
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/ping';
      axios.get(path)
        .then((res) => {
          this.targlist = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  updated() {
    this.getMessage();
  },
};
</script>
