<template>
  <nav class="bg-blue-600 text-white px-6 py-4 flex justify-between items-center">
    <NuxtLink to="/" class="font-bold text-xl">DailyNotes</NuxtLink>
    <div class="space-x-4 flex items-center">
      <NuxtLink to="/login">Login</NuxtLink>
      <NuxtLink to="/register">Register</NuxtLink>
      <NuxtLink to="/dashboard">Dashboard</NuxtLink>
      <button @click="logout" class="logout-btn ml-2">Logout</button>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const logout = async () => {
  // 1. ดึง token (ถ้าเก็บใน localStorage)
  const token = localStorage.getItem('access_token')
  try {
    if (token) {
      // 2. เรียก API logout (จะเรียกหรือไม่ก็ได้ ถ้า server เป็น JWT stateless)
      await axios.post('http://localhost:5000/api/logout', {}, {
        headers: { Authorization: `Bearer ${token}` }
      })
    }
  } catch (e) {
    // จะล้มก็ไม่เป็นไร logout ต่อ
  }
  // 3. ลบ token
  localStorage.removeItem('access_token')
  // 4. Redirect ไปหน้า login หรือหน้าแรก
  router.push('/login')
}
</script>

<style scoped>
.logout-btn {
  background: #ff5959;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 7px 20px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}
.logout-btn:hover {
  background: #d94848;
}
</style>
