<template>
  <div
    class="border-top pr-2"
    style="padding-top: 15px; padding-bottom: 15px; display: flex"
    v-bind:class="{ active: is_active }"
  >
    <button type="button" class="btn btn-sm" @click="change_note">{{ title }}</button>
    <div class="spacer"></div>
    <div class="btn-group" role="group">
      <button type="button" class="btn btn-warning btn-sm" @click="update_note">Edit</button>
      <button type="button" class="btn btn-danger btn-sm" @click="delete_note">Delete</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    id: String,
    title: String,
  },
  computed: {
    is_active() {
      return this.$route.params.id === this.id;
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
</style>
