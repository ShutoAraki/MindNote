<template>
    <div class="container">
        <div class="row">
        <div class="col-sm-10">
            <h1 class="">MindNote</h1>
            <hr><br><br>
            <button type="button" class="btn btn-success btn-sm" v-b-modal.note-modal>Create a new note</button>
            <br><br>
            <table>
                <tbody>
                    <td>
                        <table class="table table-hover">
                        <thead>
                            <tr>
                            <th scope="col">Title</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(note, index) in notes" :key="index">
                            <td><button type="button" class="btn btn-sm" @click="getANote(note.id)">{{ note.title }}</button></td>
                            <td>
                                <div class="btn-group" role="group">
                                <button type="button" class="btn btn-warning btn-sm" v-b-modal.note-update-modal>Edit</button>   
                                <button type="button" class="btn btn-danger btn-sm" @click="onDeleteNote(note)">Delete</button>
                                </div>
                            </td>
                            </tr>
                        </tbody>
                        </table>
                    </td>
                    <td>
                        <h2 class="display-2">{{ selected_note }}</h2>
                    </td>
                </tbody>
            </table>
        </div>
        </div>
        <b-modal ref="addNoteModal"
                id="note-modal"
                title="Add a new note"
                hide-footer>
        <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-title-group"
                        label="Title:"
                        label-for="form-title-input">
            <b-form-input id="form-title-input"
                            type="text"
                            v-model="addNoteForm.title"
                            required
                            placeholder="Enter title">
            </b-form-input>
            </b-form-group>
            <b-form-group id="form-content-group"
                        label="Content:"
                        label-for="form-content-input">
                <b-form-input id="form-content-input"
                            type="text"
                            v-model="addNoteForm.content"
                            required
                            placeholder="Write whatever is on your mind!">
                </b-form-input>
            </b-form-group>
            <b-button-group>
            <b-button type="submit" variant="primary">Submit</b-button>
            <b-button type="reset" variant="danger">Reset</b-button>
            </b-button-group>
        </b-form>
        </b-modal>

        <b-modal ref="editNoteModal"
                id="note-update-modal"
                title="Update"
                hide-footer>
        <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-title-edit-group"
                        label="Title:"
                        label-for="form-title-edit-input">
            <b-form-input id="form-title-edit-input"
                            type="text"
                            v-model="editForm.title"
                            required
                            placeholder="Enter title">
            </b-form-input>
            </b-form-group>
            <b-form-group id="form-content-edit-group"
                        label="Content:"
                        label-for="form-content-edit-input">
                <b-form-input id="form-content-edit-input"
                            type="text"
                            v-model="editForm.content"
                            required
                            placeholder="Let your mind wander">
                </b-form-input>
            </b-form-group>
            <b-button-group>
            <b-button type="submit" variant="primary">Update</b-button>
            <b-button type="reset" variant="danger">Cancel</b-button>
            </b-button-group>
        </b-form>
        </b-modal>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            notes: [],
            selected_note: '',
            addNoteForm: {
                title: '',
                content: '',
            },
            editForm: {
                id: '',
                title: '',
                content: '',
            },
        };
    },
    methods: {
        async getNotes() {
            const path = 'http://localhost:5000/api/notes';
            this.notes = (await axios.get(path)).data;
        },
        async getANote(id) {
            const path = `http://localhost:5000/api/note/${id}`;
            this.selected_note = (await axios.get(path)).data.content;
        },
        addNote(payload) {
            const path = 'http://localhost:5000/api/note';
            axios.post(path, payload)
                .then(() => {
                    this.getNotes();
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.log(error);
                    this.getNotes();
            });
        },
        editBook(book) {
            this.editForm = book;
        },
        updateNote(payload, id) {
            const path = `http://localhost:5000/api/note/${id}`;
            axios.post(path, payload)
                .then(() => {
                    this.getNotes();
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.log(error);
                    this.getNotes();
            });
        },
        removeNote(id) {
            const path = `http://localhost:5000/api/note/${id}`;
            axios.delete(path)
            .then(() => {
                this.getNotes();
            })
            .catch((error) => {
                // eslint-disable-next-line
                console.error(error);
                this.getBooks();
            });
        },
        initForm() {
            this.addNoteForm.title = '';
            this.addNoteForm.content = '';
            this.editForm.id = '';
            this.editForm.title = '';
            this.editForm.content = '';
        },
        onSubmit(evt) {
            evt.preventDefault();
            this.$refs.addNoteModal.hide();
            const payload = {
                title: this.addNoteForm.title,
                content: this.addNoteForm.content,
            };
            this.addNote(payload);
            this.initForm();
        },
        onReset(evt) {
            evt.preventDefault();
            this.$refs.addNoteModal.hide();
            this.initForm();
        },
        onSubmitUpdate(evt) {
            evt.preventDefault();
            this.$refs.editNoteModal.hide();
            const payload = {
                title: this.editForm.title,
                content: this.editForm.content,
            };
            this.updateNote(payload, this.editForm.id);
            this.initForm();
        },
        onResetUpdate(evt) {
            evt.preventDefault();
            this.$refs.editBookModal.hide();
            this.initForm();
            this.getBooks();
        },
        onDeleteNote(note) {
            this.removeNote(note.id);
        },
    },
    created() {
        this.getNotes();
    },
};
</script>