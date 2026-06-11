<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { DataLine, Grid, Tickets } from '@element-plus/icons-vue'

import { navigationItems } from './router'

const route = useRoute()
const isLogin = computed(() => route.path === '/login')
</script>

<template>
  <router-view v-if="isLogin" />
  <el-container v-else class="app-shell">
    <el-aside class="sidebar" width="260px">
      <div class="brand">
        <el-icon><Tickets /></el-icon>
        <span>Order System</span>
      </div>
      <el-scrollbar class="nav-scroll">
        <el-menu :default-active="route.path" router>
          <el-menu-item
            v-for="item in navigationItems"
            :key="item.path"
            :index="item.path"
          >
            <el-icon><Grid /></el-icon>
            <span>{{ item.label }}</span>
          </el-menu-item>
        </el-menu>
      </el-scrollbar>
    </el-aside>

    <el-container>
      <el-header class="topbar">
        <div>
          <div class="eyebrow">Workspace</div>
          <strong>Default workspace</strong>
        </div>
        <el-button :icon="DataLine" type="primary" plain>OpenAPI ready</el-button>
      </el-header>

      <el-main class="main-panel">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>
