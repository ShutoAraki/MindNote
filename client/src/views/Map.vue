<template>
  <div id="map">
    <map-renderer id="renderer" />
  </div>
</template>

<script>
import MapRenderer from '@/components/MapRenderer.vue'
export default {
  components: {
    MapRenderer
  }
}
</script>

<style scoped>
#map {
  flex: 1;
  display: flex;
}

#renderer {
  padding: 30px;
  flex: 1;
}
</style>
