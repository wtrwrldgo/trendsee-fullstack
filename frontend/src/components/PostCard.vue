<script setup lang="ts">
import { computed } from 'vue';
import { useLike } from '../composables/useLike';

const props = defineProps({
  post: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['analyze']);

const { isLiked, toggleLike } = useLike(props.post.id);

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  });
};

const downloadVideo = async () => {
  try {
    const response = await fetch(videoUrl.value);
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = `trendsee-video-${props.post.id}.mp4`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  } catch (error) {
    console.error('Download failed:', error);
  }
};

const sampleVideos = [
  'https://assets.mixkit.co/videos/preview/mixkit-girl-in-neon-sign-1232-large.mp4',
  'https://assets.mixkit.co/videos/preview/mixkit-winter-fashion-cold-looking-woman-concept-video-39874-large.mp4',
  'https://assets.mixkit.co/videos/preview/mixkit-tree-with-yellow-flowers-1173-large.mp4',
  'https://assets.mixkit.co/videos/preview/mixkit-shoes-of-a-person-doing-a-stretching-exercise-43407-large.mp4',
  'https://assets.mixkit.co/videos/preview/mixkit-waves-in-the-water-1164-large.mp4',
  'https://assets.mixkit.co/videos/preview/mixkit-very-close-shot-of-the-leaves-of-a-tree-wet-18310-large.mp4'
];

const videoUrl = computed(() => {
  const index = (props.post.id || 0) % sampleVideos.length;
  return sampleVideos[index];
});
</script>

<template>
  <div class="w-[262px] flex-shrink-0 bg-white rounded-2xl flex flex-col overflow-hidden shadow-sm hover:shadow-md transition-shadow">
    <!-- Header Image / Video Placeholder -->
    <div class="relative h-[420px] bg-black w-full overflow-hidden">
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
      <!-- Top Left Overlay for Source (e.g. Reels icon) -->
      <div class="absolute top-2 left-2 flex items-center gap-1 bg-black/40 backdrop-blur-sm text-white text-xs px-2 py-1 rounded-full z-10">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        Reels
      </div>

      <!-- Vertical Actions Stack (Like, Link, Download) -->
      <div class="absolute top-2 right-2 flex flex-col gap-2 z-20">
        <!-- Like Button -->
        <button 
          @click.stop="toggleLike"
          class="w-8 h-8 rounded-full bg-black/40 backdrop-blur-sm flex items-center justify-center transition-all duration-300 hover:scale-110 active:scale-95"
        >
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            :class="['h-4 w-4 transition-colors duration-300', isLiked ? 'text-red-500 fill-current' : 'text-white']" 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
          </svg>
        </button>

        <!-- Instagram Link Button -->
        <a 
          href="https://www.instagram.com/trendsee"
          target="_blank"
          @click.stop
          class="w-8 h-8 rounded-full bg-black/40 backdrop-blur-sm flex items-center justify-center transition-all duration-300 hover:scale-110 active:scale-95 text-white"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
             <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
          </svg>
        </a>

        <!-- Download Button -->
        <button 
          @click.stop="downloadVideo"
          class="w-8 h-8 rounded-full bg-black/40 backdrop-blur-sm flex items-center justify-center transition-all duration-300 hover:scale-110 active:scale-95 text-white"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
        </button>
      </div>

      <!-- Bottom Stats Overlay row inside Video -->
      <div class="absolute bottom-2 left-2 right-2 flex items-center justify-between text-white text-[10px] font-medium z-10">
        <div class="flex items-center gap-1">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 opacity-90" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
          105k
        </div>
        <div class="flex items-center gap-1">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 opacity-90" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
          </svg>
          {{ isLiked ? '86k' : '85k' }}
        </div>
        <div class="flex items-center gap-1">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 opacity-90" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          15k
        </div>
        <div class="flex items-center gap-1">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 opacity-90" fill="none" viewBox="0 0 24 24" stroke="currentColor">
             <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
          485
        </div>
      </div>
    </div>
    
    <!-- Content Section -->
    <div class="p-4 flex flex-col flex-grow bg-white">
      
      <!-- User Info Row (Moved from video to content area per Figma) -->
      <div class="flex justify-between items-center mb-3">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 rounded-full overflow-hidden bg-gray-200">
             <img src="https://ui-avatars.com/api/?name=User&background=random" alt="Avatar" class="w-full h-full object-cover">
          </div>
          <div class="flex flex-col">
            <span class="text-sm font-semibold text-blue-600">@blogerich</span>
            <span class="text-[10px] text-gray-500">384.5K</span>
          </div>
        </div>
        <div class="text-blue-500">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
      </div>
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
          class="w-full bg-[#3030BD] hover:bg-blue-800 active:bg-blue-900 text-white font-medium py-2 rounded-xl transition-colors text-sm flex items-center justify-center gap-2">
          Анализ видео
        </button>
      </div>
    </div>
  </div>
</template>
