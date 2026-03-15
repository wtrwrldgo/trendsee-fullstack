import { defineProps, defineEmits, onMounted, onUnmounted, computed, ref } from 'vue';
import AnimatedNumber from './AnimatedNumber.vue';

const props = defineProps({
  post: {
    type: Object,
    required: true
  }
});

const isAdapting = ref(false);
const isAdapted = ref(false);

const originalHooks = [
  { id: 1, time: '0s', text: 'Визуальный триггер - резкая смена ракурса привлекает внимание.', bgClass: 'bg-indigo-100', textClass: 'text-indigo-600' },
  { id: 2, time: '3s', text: 'Завязка - текстовый вопрос на экране, заставляющий досмотреть до конца.', bgClass: 'bg-blue-100', textClass: 'text-blue-600' }
];

const adaptedHooks = [
  { id: 3, time: '0s', text: 'Появление вашего продукта крупным планом под трендовый бит.', bgClass: 'bg-green-100', textClass: 'text-green-600' },
  { id: 4, time: '2s', text: 'Озвучка популярной проблемы целевой аудитории текстом на экране.', bgClass: 'bg-amber-100', textClass: 'text-amber-600' },
  { id: 5, time: '5s', text: 'Call-to-Action: Решение этой проблемы через ваш продукт! Ссылка в био.', bgClass: 'bg-purple-100', textClass: 'text-purple-600' }
];

const currentHooks = computed(() => isAdapted.value ? adaptedHooks : originalHooks);

// Generate deterministic random stats based on post ID
const postStats = computed(() => {
  const base = (props.post.id || 1) * 12345;
  return {
    views: base % 5000000 + 100000,
    likes: base % 100000 + 5000,
    reposts: base % 20000 + 1000
  };
});

const handleAdapt = () => {
  if (isAdapted.value || isAdapting.value) return;
  
  isAdapting.value = true;
  // Simulate API delay for generating a scenario
  setTimeout(() => {
    isAdapting.value = false;
    isAdapted.value = true;
  }, 1200);
};

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
              <span class="text-sm font-semibold text-right text-gray-900">
                <AnimatedNumber :value="postStats.views" format="compact" :duration="2000" />
              </span>
            </div>
            <div class="grid grid-cols-2 p-3 items-center">
              <span class="text-xs text-gray-500">Лайки</span>
              <span class="text-sm font-semibold text-right text-red-500 flex items-center justify-end gap-1">
                 <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
                </svg>
                <AnimatedNumber :value="postStats.likes" format="compact" :duration="2200" />
              </span>
            </div>
            <div class="grid grid-cols-2 p-3 items-center">
              <span class="text-xs text-gray-500">Репосты</span>
              <span class="text-sm font-semibold text-right text-gray-800">
                <AnimatedNumber :value="postStats.reposts" format="compact" :duration="2500" />
              </span>
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
               <h3 class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">
                 {{ isAdapted ? 'Адаптированный сценарий' : 'Структура хуков' }}
               </h3>
               <TransitionGroup name="list" tag="ul" class="space-y-2 relative">
                 <li v-for="hook in currentHooks" :key="hook.id" class="flex items-start gap-3 bg-white p-3 rounded-lg border border-gray-100 shadow-sm transition-all duration-300">
                    <div :class="['w-6 h-6 rounded flex items-center justify-center flex-shrink-0 mt-0.5', hook.bgClass]">
                      <span :class="['text-xs font-bold', hook.textClass]">{{ hook.time }}</span>
                    </div>
                    <p class="text-sm text-gray-600">{{ hook.text }}</p>
                 </li>
               </TransitionGroup>
            </div>
          </div>
          
          <div class="mt-8 pt-6 border-t border-gray-100 flex justify-end">
             <button 
              @click="handleAdapt"
              :disabled="isAdapted || isAdapting"
              :class="[
                'font-medium py-2.5 px-6 rounded-xl transition-all text-sm shadow-sm duration-300 flex items-center gap-2',
                isAdapted 
                  ? 'bg-green-500 text-white cursor-default' 
                  : isAdapting 
                    ? 'bg-blue-400 text-white cursor-wait'
                    : 'bg-blue-500 hover:bg-blue-600 text-white hover:shadow active:scale-95'
              ]"
            >
              <svg v-if="isAdapting" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <svg v-else-if="isAdapted" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              {{ isAdapted ? 'Сценарий готов!' : isAdapting ? 'Генерация ИИ...' : 'Адаптировать сценарий' }}
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

.list-enter-active,
.list-leave-active {
  transition: all 0.4s ease;
}
.list-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}
.list-leave-to {
  opacity: 0;
  transform: translateX(20px);
  position: absolute;
}
</style>
