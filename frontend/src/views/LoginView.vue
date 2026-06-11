<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Lock, User } from '@element-plus/icons-vue'

import { login } from '../services/api'

const router = useRouter()
const username = ref('admin')
const password = ref('admin123')
const loading = ref(false)
const error = ref('')

async function submit() {
  loading.value = true
  error.value = ''
  try {
    const response = await login(username.value, password.value)
    localStorage.setItem('order-system-token', response.access_token)
    await router.push('/dashboard')
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="login-screen">
    <section class="login-panel">
      <h1>Order System</h1>
      <p>Field-driven waybill reporting platform</p>
      <el-form label-position="top" @submit.prevent="submit">
        <el-form-item label="Username">
          <el-input v-model="username" :prefix-icon="User" />
        </el-form-item>
        <el-form-item label="Password">
          <el-input v-model="password" :prefix-icon="Lock" show-password type="password" />
        </el-form-item>
        <el-alert v-if="error" :closable="false" :title="error" type="error" />
        <el-button class="login-button" :loading="loading" type="primary" @click="submit">
          Sign in
        </el-button>
      </el-form>
    </section>
  </main>
</template>
