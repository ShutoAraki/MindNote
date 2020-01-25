<template>
  <div id="map">
    <div id="chart" v-if="!loading">
      <map-renderer id="renderer" :note_data="note_data" />
      <div id="legend" class="d-flex flex-column border border-dark">
        <div id="colorbar" class="m-2"></div>
        <div id="text" class="d-flex flex-row px-2 pb-2">
          <small>More negative</small>
          <div class="flex-grow-1"></div>
          <small>More positive</small>
        </div>
      </div>
    </div>
    <div
      class="px-0 d-flex flex-column justify-content-center h-100 w-100 flex-grow-1"
      v-if="loading"
    >
      <b-spinner class="mx-auto" label="Loading..."></b-spinner>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

import MapRenderer from '@/components/MapRenderer.vue'
export default {
  components: {
    MapRenderer
  },
  data() {
    return {
      loading: false,
      note_data: [],
    }
  },
  async created() {
    this.loading = true;
    this.note_data = (await axios.get(process.env.VUE_APP_API_URL + '/api/map')).data;
    this.loading = false;
  },
}
</script>

<style scoped>
#map,
#chart {
  flex: 1;
  display: flex;
  position: relative;
}

#renderer {
  padding: 30px;
  flex: 1;
}

#legend {
  position: absolute;
  top: 10px;
  left: 10px;
}

#colorbar {
  height: 20px;
  width: 250px;
  background: linear-gradient(
    to right,
    hsl(240, 100%, 50%),
    hsl(120, 100%, 50%),
    hsl(0, 100%, 50%)
  );
}
</style>
