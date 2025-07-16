<template>
  <div class="logout-container">
    <h2>Logout</h2>
    <div v-if="loading">Logging out...</div>
    <div v-else>
      <button @click="logout" class="logout-btn">Logout</button>
      <div v-if="error" class="error-msg">{{ error }}</div>
      <div v-if="success" class="success-msg">{{ success }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const loading = ref(false)
const error = ref('')
const success = ref('')
const router = useRouter()

const logout = async () => {
  error.value = ''
  success.value = ''
  loading.value = true

  try {
    // ดึง access_token จาก localStorage (ถ้าเก็บในที่อื่น เปลี่ยนให้ตรง)
    const token = localStorage.getItem('access_token')
    await axios.post('http://localhost:5000/api/logout', {}, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    // ลบ token ออกจาก localStorage
    localStorage.removeItem('access_token')

    success.value = "You have been logged out."
    // redirect ไปหน้าหลักหรือ login (delay เพื่อให้เห็นข้อความ success)
    setTimeout(() => {
      router.push('/login')
    }, 1000)
  } catch (err) {
    if (err.response && err.response.data && err.response.data.msg) {
      error.value = err.response.data.msg
    } else {
      error.value = "Logout failed"
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.logout-container {
  max-width: 400px;
  margin: 60px auto;
  padding: 32px 28px;
  border-radius: 12px;
  background: #1a1d24;
  color: #f8f8ff;
  box-shadow: 0 4px 32px 0 #0003;
  text-align: center;
}
.logout-btn {
  padding: 10px 30px;
  border-radius: 8px;
  border: none;
  background: #ff5959;
  color: #fff;
  font-size: 1.1em;
  cursor: pointer;
  transition: background 0.2s;
}
.logout-btn:active {
  background: #d94848;
}
.error-msg {
  margin-top: 18px;
  color: #ff5959;
}
.success-msg {
  margin-top: 18px;
  color: #21d97d;
}
</style>
