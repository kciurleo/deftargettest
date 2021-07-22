<template>
  <div class="targets container">
    <h2 class="subtitle is-3">
    Photon Ranch Easy Target Search
    </h2>
    <b-form id="targform" @submit.prevent>
      <p>
        <label for="location1">Photon Ranch Location: </label>
        <select id="location1" v-model="dataentry.location1" required>
            <option lat="34" long="-120" value="mrc">Santa Barbara (MRC)</option>
            <option lat="36" long="-106" value="saf">Santa Fe (SAF)</option>
            <option lat="-31" long="149" value="coj">Sliding Spring</option>
            <option lat="-32" long="20" value="cpt">South African Astronomical Observatory</option>
            <option lat="28" long="-16" value="tfn">Teide Observatory</option>
            <option lat="-30" long="-70" value="lsc">Cerro Tololo Interamerican Observatory</option>
            <option lat="30" long="-104" value="elp">McDonald Observatory</option>
            <option lat="20" long="-156" value="ogg">Haleakala Observatory</option>
            <option lat="30" long="34" value="tlv">Wise Observatory</option>
            <option lat="0" long="0" value="0">None</option>
        </select>
      </p>
      <p>
        <label for="lat1">Latitude (optional):</label>
          <input type="text" id="lat1" v-model="dataentry.lat1">
      </p>
      <p>
        <label for="lon1">Longitude (optional):</label>
          <input type="text" id="lon1" v-model="dataentry.lon1">
      </p>
      <p>
        <label for="dateobs">Date: </label>
            <input type="date" id="dateobs" v-model="dataentry.dateobs" required>
      </p>
      <p>
        <label for="timeobs">Time:</label>
            <input type="time" id="timeobs" v-model="dataentry.timeobs" required>
      </p>
      <p>
      <input type="radio" id="tzinfo" value="my" v-model="dataentry.tzinfo">
      <label for="my">My timezone</label>
      <!-- <input type="radio" id="tzinfo" value="local" v-model="dataentry.tzinfo"> -->
      <!-- <label for="local">Local timezone (observatory)</label> -->
      <input type="radio" id="tzinfo" value="utc" v-model="dataentry.tzinfo">
      <label for="utc">UTC</label>
      </p>
      <p>
        <b-button @click="submitForm">Find Targets</b-button>
      </p>
    </b-form>
    <div class="columns">
      <div v-for="target in targlist" :target="target" :key="target.name">
        <TargetCard :target="target" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import TargetCard from '@/components/TargetCard.vue';

export default {
  name: 'DefaultTargets',
  components: {
    TargetCard,
  },
  data() {
    return {
      target: {},
      targlist: '',
      dataentry: {
        location1: '',
        lat1: '',
        lon1: '',
        dateobs: '',
        timeobs: '',
        tzinfo: '',
        offset: '',
      },
    };
  },
  methods: {
    submitForm() {
      this.dataentry.offset = new Date().getTimezoneOffset();
      const path = 'http://localhost:5000/ping';
      axios.post(path, this.dataentry)
        .then((response) => {
          console.log(response.data);
          this.targlist = response.data;
          console.log(this.targlist);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
};
</script>
<style lang="css" scoped>
  .{targlist {
    margin-top: 100px;
  }}
  .columns {
    display: flex;
    flex-wrap: wrap;
  }

</style>
