<template>
  <div
    class="border-top pr-2"
    style="padding-top: 15px; padding-bottom: 15px; display: flex"
    v-bind:class="{ active: is_active }"
  >
    <div style="overflow-x: hidden; white-space: nowrap;">
      <button type="button" class="btn btn-sm" @click="change_note">{{ title }}</button>
    </div>
    <div class="spacer"></div>
    <small
      class="text-muted align-middle my-auto"
      id="date"
      v-bind:class="{ active: is_active }"
    >{{ formatted_date }}</small>
    <div class="btn-group" role="group">
      <button type="button" class="btn btn-warning btn-sm" @click="update_note">Edit</button>
      <button type="button" class="btn btn-danger btn-sm" @click="delete_note">Delete</button>
    </div>
  </div>
</template>

<script>
import moment from 'moment';

export default {
  props: {
    id: String,
    title: String,
    date: String,
  },
  computed: {
    is_active() {
      return this.$route.params.id === this.id;
    },
    formatted_date() {
      return moment(this.date).format('M/D/YY HH:mm');
    }
  },
  methods: {
    change_note() {
      this.$emit('change_note', this.id);
    },
    update_note() {
      this.$emit('update_note', this.id);
    },
    delete_note() {
      this.$emit('delete_note', this.id);
    },
  }
}
</script>

<style scoped>
.active {
  background-color: khaki;
}

.spacer {
  flex: 1;
}

#date {
  position: relative;
}

#date::before {
  content: "";
  display: block;
  width: 30px;
  height: 50px;
  position: absolute;
  top: -15px;
  left: -30px;
  background: linear-gradient(to right, transparent, white);
}

.active #date::before {
  background: linear-gradient(to right, transparent, khaki) !important;
}
</style>
