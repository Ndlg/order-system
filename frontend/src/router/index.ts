import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

import DashboardView from '../views/DashboardView.vue'
import GenericResourceView from '../views/GenericResourceView.vue'
import LoginView from '../views/LoginView.vue'

export interface NavigationItem {
  label: string
  path: string
  apiPath?: string
}

export const navigationItems: NavigationItem[] = [
  { label: 'Dashboard', path: '/dashboard' },
  { label: 'Workspaces', path: '/workspaces', apiPath: '/workspaces' },
  { label: 'Users', path: '/users', apiPath: '/users' },
  { label: 'Waybill Modes', path: '/waybill-modes', apiPath: '/waybill-modes' },
  { label: 'Waybill Templates', path: '/waybill-templates', apiPath: '/waybill-templates' },
  { label: 'Standard Details', path: '/standard-details', apiPath: '/standard-details' },
  { label: 'Field Definitions', path: '/field-definitions', apiPath: '/field-definitions' },
  { label: 'Field Roles', path: '/field-role-configs', apiPath: '/field-role-configs' },
  { label: 'Key Field Sets', path: '/key-field-sets', apiPath: '/key-field-sets' },
  { label: 'Match Rules', path: '/match-rules', apiPath: '/match-rules' },
  { label: 'Images', path: '/image-assets', apiPath: '/image-assets' },
  { label: 'Stalls', path: '/stalls', apiPath: '/stalls' },
  { label: 'Report Batches', path: '/report-batches', apiPath: '/report-batches' },
  { label: 'Exceptions', path: '/exceptions', apiPath: '/exceptions' },
  { label: 'Export Records', path: '/export-records', apiPath: '/export-records' },
  { label: 'Collectors', path: '/collectors', apiPath: '/collectors' },
  { label: 'Capture Tasks', path: '/capture-tasks', apiPath: '/capture-tasks' },
  { label: 'Raw Capture Records', path: '/raw-capture-records', apiPath: '/raw-capture-records' },
]

const resourceRoutes: RouteRecordRaw[] = navigationItems
  .filter((item) => item.apiPath)
  .map((item) => ({
    path: item.path,
    component: GenericResourceView,
    meta: { title: item.label, apiPath: item.apiPath },
  }))

const routes: RouteRecordRaw[] = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', component: LoginView, meta: { public: true } },
  { path: '/dashboard', component: DashboardView, meta: { title: 'Dashboard' } },
  ...resourceRoutes,
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
