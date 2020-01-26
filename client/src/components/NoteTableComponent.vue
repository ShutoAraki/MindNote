<template>
  <div
    class="border-top pr-2"
    style="padding-top: 15px; padding-left: 15px; padding-bottom: 15px; display: flex"
    v-bind:class="{ active: is_active }"
  >
    <div style="overflow-x: hidden; white-space: nowrap;">
      <button
        type="button"
        style="font-size: 20px"
        class="btn btn-sm"
        @click="change_note"
      >{{ note.title }}</button>
    </div>
    <div class="spacer"></div>
    <small
      class="text-muted align-middle my-auto"
      id="date"
      v-bind:class="{ active: is_active }"
    >{{ formatted_date }}</small>
    <div class="btn-group" role="group">
      <button type="button" class="btn btn-secondary btn-sm" @click="favorite_note">
        <b-icon icon="star-fill" v-if="note.favorite"></b-icon>
        <b-icon icon="star" v-if="!note.favorite"></b-icon>
      </button>
      <button type="button" class="btn btn-warning btn-sm" @click="update_note">Edit</button>
      <button type="button" class="btn btn-danger btn-sm" @click="delete_note">Delete</button>
    </div>
  </div>
</template>

<script>
import moment from 'moment';

export default {
  props: {
    note: Object
  },
  computed: {
    is_active() {
      return this.$route.params.id === this.id;
    },
    formatted_date() {
      return moment(this.note.date).format('M/D/YY HH:mm');
    }
  },
  methods: {
    favorite_note() {
      this.$emit('favorite_note', this.note.id, !this.note.favorite);
    },
    change_note() {
      this.$emit('change_note', this.note.id);
    },
    update_note() {
      this.$emit('update_note', this.note.id);
    },
    delete_note() {
      this.$emit('delete_note', this.note.id);
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
  padding-right: 20px;
}

#date::before {
  content: "";
  display: block;
  width: 30px;
  height: 50px;
  position: absolute;
  top: -15px;
  left: -30px;
  background: linear-gradient(to right, transparent, rgb(243, 241, 196));
}

.active #date::before {
  background: linear-gradient(to right, transparent, khaki) !important;
}
</style>
