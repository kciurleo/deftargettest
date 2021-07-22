<template>
  <div class="targets container">
    <h2 class="subtitle is-3">
    Check out these targets
    </h2>
    <form id="targform" @submit.prevent>
      <p>
        <label for="location1">PTR Location (optional): </label>
        <select id="location1" v-model="dataentry.location1">
            <option lat="0" long="0" value="0"> </option>
            <option lat="34" long="-120" value="mrc">Santa Barbara</option>
            <option lat="36" long="-106" value="saf">Santa Fe</option>
            <option lat="-31" long="149" value="coj">Sliding Spring</option>
            <option lat="-32" long="20" value="cpt">South African Astronomical Observatory</option>
            <option lat="28" long="-16" value="tfn">Teide Observatory</option>
            <option lat="-30" long="-70" value="lsc">Cerro Tololo Interamerican Observatory</option>
            <option lat="30" long="-104" value="elp">McDonald Observatory</option>
            <option lat="20" long="-156" value="ogg">Haleakala Observatory</option>
            <option lat="30" long="34" value="tlv">Wise Observatory</option>
        </select>
      </p>
      <p>
        <label for="lat1">Latitude:</label><br>
            <input type="text" id="lat1" v-model="dataentry.lat1"><br>
        <label for="lon1">Longitude:</label><br>
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
        <button @click="submitForm">click me</button>
      </p>
    </form>
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
