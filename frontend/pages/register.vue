<template>
  <div class="register-container">
    <h2>Register</h2>
    <form @submit.prevent="register">
      <div class="form-group">
        <label>Username</label>
        <input v-model="username" required autocomplete="username" />
      </div>
      <div class="form-group">
        <label>Password</label>
        <input v-model="password" type="password" required autocomplete="new-password" />
      </div>
      <button type="submit" :disabled="loading">
        {{ loading ? "Registering..." : "Register" }}
      </button>
    </form>
    <div v-if="error" class="error-msg">{{ error }}</div>
    <div v-if="success" class="success-msg">{{ success }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

// <--- เปลี่ยน url ตรงนี้หากใช้ proxy ใน nuxt.config.ts --->
const API_URL = 'http://localhost:5000/api/register'

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')

const register = async () => {
  error.value = ''
  success.value = ''
  loading.value = true
  try {
    const res = await axios.post(API_URL, {
      username: username.value,
      password: password.value,
    })
    success.value = res.data.msg
    username.value = ''
    password.value = ''
  } catch (err) {
    if (err.response && err.response.data && err.response.data.msg) {
      error.value = err.response.data.msg
    } else {
      error.value = 'Something went wrong!'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 60px auto;
  padding: 32px 28px;
  border-radius: 12px;
  background: #1a1d24;
  color: #f8f8ff;
  box-shadow: 0 4px 32px 0 #0003;
}
.form-group {
  margin-bottom: 18px;
}
input {
  width: 100%;
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #444;
  margin-top: 4px;
  background: #272b33;
  color: #f8f8ff;
}
button {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 8px;
  background: #409eff;
  color: #fff;
  font-size: 1.1em;
  cursor: pointer;
  transition: background 0.2s;
}
button:disabled {
  background: #b6b9c9;
  cursor: not-allowed;
}
.error-msg {
  margin-top: 14px;
  color: #ff5959;
}
.success-msg {
  margin-top: 14px;
  color: #21d97d;
}
</style>
