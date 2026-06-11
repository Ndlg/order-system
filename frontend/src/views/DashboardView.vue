<script setup lang="ts">
const stats = [
  { label: 'Waybill modes', value: '1' },
  { label: 'Field definitions', value: '0' },
  { label: 'Match rules', value: '0' },
  { label: 'Exports', value: '0' },
]
</script>

<template>
  <section class="page-header">
    <div>
      <h1>Dashboard</h1>
      <p>Platform scaffold for waybill reading, user-defined fields, matching, and exports.</p>
    </div>
  </section>

  <section class="stat-grid">
    <article v-for="stat in stats" :key="stat.label" class="stat-tile">
      <span>{{ stat.label }}</span>
      <strong>{{ stat.value }}</strong>
    </article>
  </section>

  <section class="work-surface">
    <h2>Build order</h2>
    <el-steps :active="1" finish-status="success">
      <el-step title="Scaffold" description="Backend, frontend, scripts" />
      <el-step title="Persistence" description="MySQL models and repositories" />
      <el-step title="Workflow" description="Excel upload, matching, export" />
    </el-steps>
  </section>
</template>
