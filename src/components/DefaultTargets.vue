<template>
  <div class="targets container">
    <h2 class="subtitle is-3">
    Photon Ranch Easy Target Search
    </h2>
    <b-form id="targform" @submit.prevent>
      <p>
        <label for="location1">Photon Ranch Location: </label>
        <select id="location1" v-model="dataentry.location1" required @change="setLatLong">
            <option lat="34" lon="-120" value="mrc">Mountain Ranch Camp Observatory</option>
            <option lat="36" lon="-106" value="saf">Apache Ridge Observatory</option>
            <option lat="-31" lon="149" value="coj">Sliding Spring Observatory</option>
            <option lat="-32" lon="20" value="cpt">South African Astronomical Observatory</option>
            <option lat="28" lon="-16" value="tfn">Teide Observatory</option>
            <option lat="-30" lon="-70" value="lsc">Cerro Tololo Interamerican Observatory</option>
            <option lat="30" lon="-104" value="elp">McDonald Observatory</option>
            <option lat="20" lon="-156" value="ogg">Haleakala Observatory</option>
            <option lat="30" lon="34" value="tlv">Wise Observatory</option>
            <option lat="" lon="" value="0">None</option>
        </select>
      </p>
      <p>
        <label for="lat1">Latitude:</label>
          <input type="text" id="lat1" v-model="dataentry.lat1">
        <label for="lon1">Longitude:</label>
          <input type="text" id="lon1" v-model="dataentry.lon1">
      </p>
      <p>
        <label for="dateobs">Date: </label>
            <input type="date" id="dateobs" v-model="dataentry.dateobs" required>
        <label for="timeobs">Time:</label>
            <input type="time" id="timeobs" v-model="dataentry.timeobs" required>
      </p>
      <input name="tzinfo" type="radio" id="tzinfo" value="utc" v-model="dataentry.tzinfo" required>
      <label for="utc">UTC</label>
      <br>
      <input name="tzinfo" type="radio" id="tzinfo" value="my" v-model="dataentry.tzinfo" required>
      <label for="my">My timezone</label>
      <div v-if="dataentry.location1 !== '0'">
        <input name="tzinfo" type="radio" id="tzinfo" value="lcl" v-model="dataentry.tzinfo">
        <label for="local">Local timezone</label>
      </div>
      <p>
        <b-button @click="submitForm" type="submit">Find Easy Targets</b-button>
        <b-button @click="submitFormM" type="submit">Find Messier Objects</b-button>
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
        location1: '0',
        lat1: '',
        lon1: '',
        dateobs: '',
        timeobs: '',
        tzinfo: 'my',
        offset: '',
        messier: '',
      },
    };
  },
  methods: {
    setLatLong() {
      const ddl = document.getElementById('location1');
      const selectedOption = ddl.options[ddl.selectedIndex];
      this.dataentry.lat1 = selectedOption.getAttribute('lat');
      this.dataentry.lon1 = selectedOption.getAttribute('lon');
    },
    submitForm() {
      this.dataentry.offset = new Date().getTimezoneOffset();
      this.dataentry.messier = 'no';
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
    submitFormM() {
      this.dataentry.offset = new Date().getTimezoneOffset();
      this.dataentry.messier = 'yes';
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
