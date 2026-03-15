<script setup lang="ts">
import { defineProps, defineEmits, onMounted, onUnmounted, computed } from 'vue';

const props = defineProps({
  post: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['close']);

// Lock body scroll when modal is open
onMounted(() => {
  document.body.style.overflow = 'hidden';
});

onUnmounted(() => {
  document.body.style.overflow = '';
});

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
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
  <Transition name="modal">
    <div class="fixed inset-0 z-50 flex items-center justify-center overflow-auto bg-black/40 backdrop-blur-sm p-4 sm:p-6"
         @click.self="emit('close')">
      
      <div class="relative bg-white rounded-3xl w-full max-w-[920px] shadow-2xl overflow-hidden flex flex-col md:flex-row max-h-[90vh]">
        
        <!-- Close Button (Absolute) -->
        <button @click="emit('close')" class="absolute top-4 right-4 z-10 p-2 bg-gray-100 hover:bg-gray-200 rounded-full text-gray-500 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        
        <!-- Left Column: Media & Summary -->
        <div class="bg-slate-50 p-6 md:w-[320px] flex-shrink-0 flex flex-col border-r border-gray-100">
          <div class="w-full aspect-[9/16] bg-slate-900 rounded-2xl mb-6 relative overflow-hidden shadow-inner group">
             <video 
               :src="videoUrl" 
               class="absolute inset-0 w-full h-full object-cover opacity-90 group-hover:opacity-100 transition-opacity"
               autoplay 
               loop 
               muted 
               playsinline
             ></video>
          </div>
          
          <div class="flex items-center gap-3 mb-6">
            <div class="w-10 h-10 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center font-bold border border-blue-200">
              T
            </div>
            <div>
              <div class="font-bold text-gray-900 text-sm">@trendsee</div>
              <div class="text-xs text-gray-500">224K followers</div>
            </div>
          </div>
          
          <!-- Mock stats table -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden divide-y divide-gray-50">
            <div class="grid grid-cols-2 p-3 items-center">
              <span class="text-xs text-gray-500">Просмотры</span>
              <span class="text-sm font-semibold text-right">1.2M</span>
            </div>
            <div class="grid grid-cols-2 p-3 items-center">
              <span class="text-xs text-gray-500">Лайки</span>
              <span class="text-sm font-semibold text-right text-red-500 flex items-center justify-end gap-1">
                 <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
                </svg>
                45.2K
              </span>
            </div>
            <div class="grid grid-cols-2 p-3 items-center">
              <span class="text-xs text-gray-500">Репосты</span>
              <span class="text-sm font-semibold text-right text-gray-800">12.1K</span>
            </div>
          </div>
        </div>
        
        <!-- Right Column: Context & Details -->
        <div class="p-6 md:p-8 flex-grow flex flex-col overflow-y-auto">
          <div class="mb-4 pr-8">
            <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ props.post.title }}</h2>
            <div class="text-sm text-gray-500 flex items-center gap-2">
               User ID: {{ props.post.user_id }} &bull; {{ formatDate(props.post.created_at) }}
            </div>
          </div>
          
          <div class="flex gap-2 flex-wrap mb-6">
            <span class="bg-blue-50 text-blue-600 text-xs font-semibold px-3 py-1 rounded-full">Тренд</span>
            <span class="bg-green-50 text-green-600 text-xs font-semibold px-3 py-1 rounded-full">Юмор</span>
            <span class="bg-amber-50 text-amber-600 text-xs font-semibold px-3 py-1 rounded-full">Высокий охват</span>
          </div>
          
          <div class="space-y-6">
            <!-- Dynamic Post Details -->
            <div>
              <h3 class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Суть видео</h3>
              <p class="text-sm text-gray-700 leading-relaxed bg-gray-50 p-4 rounded-xl">
                {{ props.post.text }}
              </p>
            </div>
            
            <div>
               <h3 class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Структура хуков</h3>
               <ul class="space-y-2">
                 <li class="flex items-start gap-3 bg-white p-3 rounded-lg border border-gray-100">
                    <div class="w-6 h-6 rounded bg-indigo-100 flex items-center justify-center flex-shrink-0 mt-0.5"><span class="text-xs font-bold text-indigo-600">0s</span></div>
                    <p class="text-sm text-gray-600">Визуальный триггер - резкая смена ракурса привлекает внимание.</p>
                 </li>
                 <li class="flex items-start gap-3 bg-white p-3 rounded-lg border border-gray-100">
                    <div class="w-6 h-6 rounded bg-blue-100 flex items-center justify-center flex-shrink-0 mt-0.5"><span class="text-xs font-bold text-blue-600">3s</span></div>
                    <p class="text-sm text-gray-600">Завязка - текстовый вопрос на экране, заставляющий досмотреть до конца.</p>
                 </li>
               </ul>
            </div>
          </div>
          
          <div class="mt-8 pt-6 border-t border-gray-100 flex justify-end">
            <button class="bg-blue-500 hover:bg-blue-600 text-white font-medium py-2.5 px-6 rounded-xl transition-colors text-sm shadow-sm hover:shadow active:scale-95 duration-200">
              Адаптировать сценарий
            </button>
          </div>
        </div>
        
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .bg-white,
.modal-leave-active .bg-white {
  transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.modal-enter-from .bg-white,
.modal-leave-to .bg-white {
  transform: scale(0.95) translateY(10px);
}
</style>
