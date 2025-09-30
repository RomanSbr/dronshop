<template>
  <div class="notifications-container">
    <Notification
      v-for="notification in notifications"
      :key="notification.id"
      :message="notification.message"
      :description="notification.description"
      :type="notification.type"
      :duration="notification.duration"
      :auto-close="notification.autoClose"
      @close="removeNotification(notification.id)"
    />
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useNotificationsStore } from '../stores/notifications'
import Notification from './Notification.vue'

const notificationsStore = useNotificationsStore()
const { notifications } = storeToRefs(notificationsStore)
const { removeNotification } = notificationsStore
</script>

<style scoped>
.notifications-container {
  @apply fixed top-0 right-0 z-50 p-4 space-y-3 pointer-events-none;
}
</style>
