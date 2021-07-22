<template>
  <div class="target-card">
    <div class="card">
      <div class="card-content">
        <h2 class="is-size-4 has-text-weight-bold">{{ target.name }}</h2>
        <h3 class="target-type">{{ target.type }}</h3>
        <img src="@/assets/DefaultTargetImages/SextansC_1_E_GLC_SDSS9.jpg"/>
        <h4>{{ target.image }}</h4>
      </div>
    </div>
  </div>
</template>
<script>

export default {
  props: [
    'target',
  ],
};
</script>
