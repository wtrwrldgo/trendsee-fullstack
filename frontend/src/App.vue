<script setup lang="ts">
import Sidebar from './components/Sidebar.vue'
import FeedView from './views/FeedView.vue'
</script>

<template>
  <div class="flex min-h-screen bg-slate-50">
    <Sidebar />
    <main class="flex-1 w-full min-w-0">
      <FeedView />
    </main>
  </div>
</template>
