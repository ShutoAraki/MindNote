<template>
  <b-container fluid>
    <div v-if="loading">
      <span>Loading note...</span>
    </div>
    <div v-if="!loading && note_loaded" class="pt-2 text-left">
      <h3>{{title}}</h3>
      <br />
      <span>{{ content }}</span>
    </div>
    <div v-if="!loading && !note_loaded">
      <span>No note loaded!</span>
    </div>
  </b-container>
</template>

<script> 
import axios from 'axios';

export default {
  props: {
    id: String,
  },
  data() {
    return {
      title: '',
      content: '',
      note_loaded: false,
      loading: false,
    }
  },
  methods: {
    async get_note(id) {
      this.note_loaded = false;
      if (id) {
        const path = `http://localhost:5000/api/note/${id}`;
        try {
          this.loading = true;
          let note = (await axios.get(path)).data;
          this.loading = false;
          this.title = note.title;
          this.content = note.content;
          this.note_loaded = true;
        } catch (error) {
          this.loading = false;
        }
      }
    }
  },
  mounted() {
    this.get_note(this.id);
  },
  watch: {
    id: function () {
      this.get_note(this.id);
    }
  }
}
</script>
