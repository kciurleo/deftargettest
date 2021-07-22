<template>
  <div class="target-card">
    <div class="card">
      <img :src="`${target.image}`"/>
      <div class="card-content">
        <h2 class="is-size-4 has-text-weight-bold">{{ target.name }}</h2>
        <h3 class="target-type">{{ target.type }}</h3>
      </div>
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
    height: 400px;
    width: 400px;
  }
  img {
    position: relative;
    width:400px;
  }
  .card-content {
    color: white;
    position: absolute;
    top:20px;
    left:20px;

  }
</style>
