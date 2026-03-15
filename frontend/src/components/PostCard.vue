<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
  post: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['analyze']);

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  });
};

const sampleVideos = [
  'https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4',
  'https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4',
  'https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4',
  'https://storage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4',
  'https://storage.googleapis.com/gtv-videos-bucket/sample/SubaruOutbackOnStreetAndDirt.mp4',
  'https://storage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4'
];

const videoUrl = computed(() => {
  const index = (props.post.id || 0) % sampleVideos.length;
  return sampleVideos[index];
});
</script>

<template>
  <div class="w-[262px] bg-white rounded-2xl flex flex-col overflow-hidden shadow-sm hover:shadow-md transition-shadow">
    <!-- Header Image / Video Placeholder -->
    <div class="relative h-48 bg-slate-200 w-full overflow-hidden">
      <!-- Background Video -->
      <video 
        :src="videoUrl" 
        class="absolute inset-0 w-full h-full object-cover"
        autoplay 
        loop 
        muted 
        playsinline
      ></video>
      <!-- Decorative Gradient overlay for text readability -->
      <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-black/30 pointer-events-none"></div>
      
      <!-- Top Right overlay for views -->
      <div class="absolute top-2 right-2 bg-black/40 backdrop-blur-sm text-white text-xs font-semibold px-2 py-1 rounded flex items-center gap-1">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
        </svg>
        1.2M
      </div>
      
      <!-- Bottom Left Overlay for User -->
      <div class="absolute bottom-2 left-2 flex items-center gap-2">
        <div class="w-8 h-8 rounded-full bg-white flex items-center justify-center text-xs font-bold text-blue-600 shadow-sm border border-gray-100">
          T
        </div>
        <span class="text-white text-xs font-medium drop-shadow-md">@trendsee</span>
      </div>
    </div>
    
    <!-- Content Section -->
    <div class="p-4 flex flex-col flex-grow">
      <!-- Vibe Score -->
      <div class="flex items-center justify-between mb-2">
        <div class="flex items-center gap-1">
          <span class="text-sm font-bold text-gray-800">{{ props.post.title }}</span>
        </div>
        <div class="text-xs text-gray-400">{{ formatDate(props.post.created_at) }}</div>
      </div>
      
      <p class="text-xs text-gray-500 line-clamp-2 mb-4">
        {{ props.post.text }}
      </p>
      
      <div class="mt-auto">
        <button 
          @click="emit('analyze')"
          class="w-full bg-blue-500 hover:bg-blue-600 active:bg-blue-700 text-white font-medium py-2 rounded-xl transition-colors text-sm flex items-center justify-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          Анализ
        </button>
      </div>
    </div>
  </div>
</template>
