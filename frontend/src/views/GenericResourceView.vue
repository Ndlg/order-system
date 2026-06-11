<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { Plus, Refresh } from '@element-plus/icons-vue'

import { createRecord, getRecords, type ApiRecord } from '../services/api'

const route = useRoute()
const title = computed(() => String(route.meta.title ?? 'Resource'))
const apiPath = computed(() => String(route.meta.apiPath ?? ''))
const rows = ref<ApiRecord[]>([])
const loading = ref(false)
const error = ref('')
const payload = ref('{\n  "name": "New record"\n}')

const columns = computed(() => {
  const keys = new Set<string>()
  rows.value.forEach((row) => Object.keys(row).forEach((key) => keys.add(key)))
  return Array.from(keys).slice(0, 8)
})

async function load() {
  if (!apiPath.value) return
  loading.value = true
  error.value = ''
  try {
    rows.value = await getRecords(apiPath.value)
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Unable to load records'
  } finally {
    loading.value = false
  }
}

async function create() {
  try {
    const parsed = JSON.parse(payload.value) as ApiRecord
    await createRecord(apiPath.value, parsed)
    await load()
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Unable to create record'
  }
}

watch(apiPath, load, { immediate: true })
</script>

<template>
  <section class="page-header">
    <div>
      <h1>{{ title }}</h1>
      <p>Workspace-scoped platform records.</p>
    </div>
    <el-button :icon="Refresh" :loading="loading" @click="load">Refresh</el-button>
  </section>

  <el-alert v-if="error" :closable="false" :title="error" type="error" />

  <section class="resource-layout">
    <div class="work-surface">
      <el-table :data="rows" height="520" stripe>
        <el-table-column v-for="column in columns" :key="column" :label="column" :prop="column" />
      </el-table>
    </div>

    <aside class="editor-panel">
      <h2>Create record</h2>
      <el-input v-model="payload" :rows="12" type="textarea" />
      <el-button :icon="Plus" type="primary" @click="create">Create</el-button>
    </aside>
  </section>
</template>
