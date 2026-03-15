<script setup lang="ts">
import { ref } from 'vue'
import Sidebar from './components/Sidebar.vue'
import FeedView from './views/FeedView.vue'

const currentMenu = ref('feed')
</script>

<template>
  <div class="flex min-h-screen bg-slate-50">
    <Sidebar :active-menu="currentMenu" @change-menu="currentMenu = $event" />
    <main class="flex-1 w-full min-w-0">
      <FeedView v-if="currentMenu === 'feed'" />
      
      <!-- Placeholder for undeveloped sections -->
      <div v-else class="h-full flex flex-col items-center justify-center p-8 text-center bg-white rounded-tl-3xl shadow-sm lg:m-2 lg:ml-0 border border-gray-100 min-h-[calc(100vh-16px)]">
        <div class="w-20 h-20 bg-blue-50 rounded-2xl flex items-center justify-center mb-6 shadow-sm border border-blue-100">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
        </div>
        <h2 class="text-3xl font-bold text-gray-800 mb-2">Раздел в разработке</h2>
        <p class="text-gray-500 max-w-md mx-auto mb-8">
          Вы выбрали раздел "<span class="font-medium text-gray-700">{{ currentMenu === 'analytics' ? 'Статистика' : currentMenu === 'scenarios' ? 'Сценарии' : 'Настройки' }}</span>". 
          <br/><br/>
          В рамках данного тестового задания реализована только основная фича — интерактивная лента публикаций с бесконечным скроллом и UI-модалками.
        </p>
        <button @click="currentMenu = 'feed'" class="bg-blue-500 hover:bg-blue-600 text-white font-medium py-3 px-8 rounded-xl transition-all duration-200 shadow-sm hover:shadow active:scale-95">
          Вернуться в Мою ленту
        </button>
      </div>
    </main>
  </div>
</template>
