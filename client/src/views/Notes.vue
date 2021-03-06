<template>
  <b-container fluid>
    <div class="row mx-0" id="row">
      <!--
        <button type="button" class="btn btn-success btn-sm" v-b-modal.note-modal>Create a new note</button>
        <br />
      <br />-->
      <b-col cols="4" class="px-0" id="left-column" v-if="!loading_notes">
        <div class="pl-0 pr-0 border-right overflow-auto" id="notes">
          <note-table-component
            v-for="note in notes"
            :key="note.id"
            :note="note"
            v-on:change_note="change_note"
            v-on:delete_note="delete_note"
            v-on:update_note="update_note"
            v-on:favorite_note="favorite_note"
          ></note-table-component>
        </div>
        <div
          cols="4"
          class="py-3 bg-success"
          style="flex: 0; cursor: pointer;"
          v-b-modal.note-modal
        >
          <span class="text-light">Create a new note</span>
        </div>
      </b-col>
      <b-col
        cols="4"
        class="px-0 d-flex flex-column justify-content-center h-100"
        id="left-column"
        v-if="loading_notes"
      >
        <b-spinner class="mx-auto" label="Loading..."></b-spinner>
      </b-col>
      <b-col cols="8">
        <note-viewer :id="current_id" ref="note_viewer"></note-viewer>
      </b-col>
    </div>
    <b-modal ref="addNoteModal" id="note-modal" title="Add a new note" hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-title-group" label="Title:" label-for="form-title-input">
          <b-form-input
            id="form-title-input"
            type="text"
            v-model="addNoteForm.title"
            required
            placeholder="Enter title"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="form-content-group" label="Content:" label-for="form-content-input">
          <b-form-textarea
            id="form-content-input"
            type="text"
            size="lg"
            v-model="addNoteForm.content"
            required
            placeholder="Write whatever is on your mind!"
          ></b-form-textarea>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>

    <b-modal ref="editNoteModal" id="note-update-modal" title="Update" hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-title-edit-group" label="Title:" label-for="form-title-edit-input">
          <b-form-input
            id="form-title-edit-input"
            type="text"
            v-model="editForm.title"
            required
            placeholder="Enter title"
          ></b-form-input>
        </b-form-group>
        <b-form-group
          id="form-content-edit-group"
          label="Content:"
          label-for="form-content-edit-input"
        >
          <b-form-textarea
            id="form-content-input"
            type="text"
            v-model="editForm.content"
            required
            placeholder="Let your mind wander"
          ></b-form-textarea>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </b-container>
</template>

<script>
import axios from 'axios';

import NoteTableComponent from '@/components/NoteTableComponent.vue';
import NoteViewer from '@/components/NoteViewer.vue';

export default {
  components: {
    NoteTableComponent,
    NoteViewer
  },
  data() {
    return {
      loading_notes: false,
      notes: [],
      current_id: this.$route.params.id ? this.$route.params.id : '',
      addNoteForm: {
        title: '',
        content: ''
      },
      editForm: {
        id: '',
        title: '',
        content: ''
      }
    };
  },
  methods: {
    async get_note(id) {
      this.loading_notes = true;
      const path = process.env.VUE_APP_API_URL + `/api/note/${id}`;
      this.loading_notes = false;
      return (await axios.get(path)).data;
    },
    async get_notes() {
      this.loading_notes = true;
      const path = process.env.VUE_APP_API_URL + '/api/notes';
      this.notes = (await axios.get(path)).data;
      this.loading_notes = false;
    },
    async addNote(payload) {
      const path = process.env.VUE_APP_API_URL + '/api/note';
      let id = (await axios.post(path, payload)).data.id;
      this.get_notes();
      this.change_note(id);
    },
    async change_note(id) {
      this.$router.replace(`/notes/${id}`);
      this.current_id = id;
    },
    async favorite_note(id, favorite) {
      let note = await this.get_note(id);
      note.favorite = favorite;
      delete note.id;
      this.send_update_note(note, id);
    },
    async update_note(id) {
      let note = await this.get_note(id);
      this.editForm.id = note.id;
      this.editForm.title = note.title;
      this.editForm.content = note.content;
      this.editForm.favorite = note.favorite;

      this.$refs.editNoteModal.show();
    },
    async send_update_note(payload, id) {
      const path = process.env.VUE_APP_API_URL + `/api/note/${id}`;
      await axios.post(path, payload);
      this.get_notes();
    },
    async delete_note(id) {
      const path = process.env.VUE_APP_API_URL + `/api/note/${id}`;
      await axios.delete(path);
      this.get_notes();
      this.change_note('');
    },
    initForm() {
      this.addNoteForm.title = '';
      this.addNoteForm.content = '';
      this.editForm.id = '';
      this.editForm.title = '';
      this.editForm.content = '';
      this.editForm.favorite = false;
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addNoteModal.hide();
      const payload = {
        title: this.addNoteForm.title,
        content: this.addNoteForm.content,
        favorite: false,
      };
      this.addNote(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addNoteModal.hide();
      this.initForm();
    },
    async onSubmitUpdate(evt) {
      evt.preventDefault();
      const payload = {
        title: this.editForm.title,
        content: this.editForm.content,
        favorite: this.editForm.favorite
      };
      await this.send_update_note(payload, this.editForm.id);
      this.$refs.note_viewer.get_note(this.editForm.id);
      this.$refs.editNoteModal.hide();
      this.initForm();
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editBookModal.hide();
      this.initForm();
    }
  },
  created() {
    this.get_notes();
  }
};
</script>

<style scoped>
.container-fluid {
  padding-right: 0;
  padding-left: 0;
  flex: 1;
  display: flex;
  max-height: inherit;
  overflow: hidden;
}

#row {
  max-height: inherit;
  flex: 1;
  display: flex;
  flex-direction: row;
}

#left-column {
  height: 100%;
  display: flex;
  flex-direction: column;
}

#notes {
  max-height: inherit;
  height: 100%;
  width: 100%;
  flex: 1;
  display: flex;
  flex-direction: column;
}

#form-content-input {
  height: 400px;
  text-align: start;
}
</style>
