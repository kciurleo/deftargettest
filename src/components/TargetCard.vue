<template>
  <div class="target-card">
    <div class="card">
      <img :src="`${target.image}`"/>
      <div class="target-name">
        <h2>{{ target.name }}</h2>
      </div>
        <h3 class="target-type">{{ target.type }}</h3>
    </div>
  </div>
</template>
<script>

export default {
  props: [
    'target',
  ],
  computed: {
    targetImage() {
      return {
        '--target-image': this.target.image,
      };
    },
  },
};
</script>
<style lang="css">
  .card {
    position: relative;
    height: 300px;
    width: 300px;
  }
  img {
    position: relative;
    width:100%;
    height:100%;
  }
  .target-name {
    color: white;
    position: absolute;
    top:5%;
    left:5%;

  }
  .target-type {
    color: white;
    position: absolute;
    top:80%;
    left:5%;

  }
</style>
