<template>
  <div class="p-6 max-w-3xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">My Notes</h1>

    <div class="flex gap-2 mb-4">
  <input v-model="searchKeyword" placeholder="Search notes..." class="border p-2 flex-1" @keyup.enter="searchNotes" />
  <button @click="searchNotes" class="bg-blue-500 text-white p-2">Search</button>
  <button @click="fetchNotes" class="bg-gray-400 text-white p-2">Reset</button>
</div>

    <div class="flex gap-2 mb-4">
      <input v-model="title" placeholder="Title" class="border p-2 w-1/3" />
      <input v-model="content" placeholder="Content" class="border p-2 flex-1" />
      <button @click="createNote" class="bg-green-500 text-white p-2">Add</button>
    </div>

    <NoteCard
      v-for="note in notes"
      :key="note.id"
      :note="note"
      @delete="deleteNote"
    />
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const title = ref('')
const content = ref('')
const notes = ref([])

const fetchNotes = async () => {
  const token = localStorage.getItem('access_token')
  const res = await axios.get('http://localhost:5000/api/notes', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  notes.value = res.data
}

const createNote = async () => {
  const token = localStorage.getItem('access_token')
  try {
    await axios.post('http://localhost:5000/api/notes', {
      title: title.value,
      content: content.value
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    title.value = ''
    content.value = ''
    fetchNotes()
  } catch (e) {
    console.error('Create note failed:', e)
  }
}


const searchKeyword = ref('')

const searchNotes = async () => {
  const token = localStorage.getItem('access_token')
  if (!searchKeyword.value.trim()) {
    fetchNotes()
    return
  }
  try {
    const res = await axios.get(
      `http://localhost:5000/api/notes/search?keyword=${encodeURIComponent(searchKeyword.value)}`,
      { headers: { Authorization: `Bearer ${token}` } }
    )
    notes.value = res.data
  } catch (err) {
    console.error('Search note failed:', err)
  }
}


const deleteNote = async (id) => {
  const token = localStorage.getItem('access_token')
  await axios.delete(`http://localhost:5000/api/notes/${id}`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  fetchNotes()
}

onMounted(fetchNotes)
</script>

