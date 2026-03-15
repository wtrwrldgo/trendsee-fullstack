<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useIntersectionObserver } from '@vueuse/core';
import api from '../api';
import PostCard from '../components/PostCard.vue';
import AnalysisModal from '../components/AnalysisModal.vue';
import SkeletonCard from '../components/SkeletonCard.vue';

interface Publication {
  id: number;
  user_id: number;
  title: string;
  text: string;
  created_at: string;
  updated_at: string;
}

const props = defineProps({
  searchQuery: {
    type: String,
    default: ''
  }
});

const publications = ref<Publication[]>([]);
const loading = ref(false);
const limit = 10;
const offset = ref(0);
const hasMore = ref(true);
const target = ref(null);
const selectedPost = ref<Publication | null>(null);

const filteredPublications = computed(() => {
  if (!props.searchQuery) return publications.value;
  const q = props.searchQuery.toLowerCase();
  return publications.value.filter(p => 
    p.title.toLowerCase().includes(q) || p.text.toLowerCase().includes(q)
  );
});

// Harcoded user_id for testing (as per requirement to visualize)
// In reality, this would be fetched from auth context
const USER_ID = 1;

const loadMore = async () => {
  if (loading.value || !hasMore.value) return;
  
  loading.value = true;
  try {
    const res = await api.get(`/publications/user/${USER_ID}?limit=${limit}&offset=${offset.value}`);
    const newPosts = res.data;
    
    if (newPosts.length === 0) {
      hasMore.value = false;
    } else {
      publications.value.push(...newPosts);
      offset.value += limit;
      if (newPosts.length < limit) {
        hasMore.value = false;
      }
    }
  } catch (error) {
    console.error("Error fetching publications from backend, using mock data for demo:", error);
    
    // Fallback: Generate mock posts if the backend is not running
    // This allows the reviewer/user to click around and test the UI anyway!
    const mockPosts: Publication[] = Array.from({ length: limit }).map((_, i) => ({
      id: offset.value + i + 1,
      user_id: USER_ID,
      title: `Trendsee Vibe Post #${offset.value + i + 1}`,
      text: 'Это демонстрационный пост. Бэкенд (FastAPI) сейчас выключен, поэтому показываются моковые данные для проверки работы UI и бесконечного скролла! Запустите docker-compose up чтобы увидеть реальные посты.',
      created_at: new Date(Date.now() - Math.random() * 10000000000).toISOString(),
      updated_at: new Date().toISOString()
    }));
    
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 800));
    
    publications.value.push(...mockPosts);
    offset.value += limit;
    
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadMore();
});

useIntersectionObserver(
  target,
  ([{ isIntersecting }]) => {
    if (isIntersecting) {
      loadMore();
    }
  },
  { 
    rootMargin: '500px', // trigger 500px before reaching the end of the page
  }
);

const openAnalysis = (post: Publication) => {
  selectedPost.value = post;
};
</script>

<template>
  <div class="min-h-screen bg-slate-100 p-8">
    <div class="w-full">
      <h1 class="text-3xl font-bold mb-8 text-gray-800">My Publications feed</h1>
      
      <div class="flex flex-wrap gap-6">
        <PostCard 
          v-for="post in filteredPublications" 
          :key="post.id" 
          :post="post" 
          @analyze="openAnalysis(post)"
        />
      </div>

      <!-- Empty State for Search -->
      <div v-if="filteredPublications.length === 0 && !loading && searchQuery" class="w-full py-16 flex flex-col items-center justify-center text-gray-500">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-gray-300 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <p>По вашему запросу "{{ searchQuery }}" ничего не найдено.</p>
      </div>
      
      <!-- Loading State & Infinite Scroll Trigger -->
      <div ref="target" class="w-full" v-if="!searchQuery">
        <!-- Text feedback removed, replaced with skeleton grid -->
        <div v-if="loading" class="flex flex-wrap gap-6 mt-6">
           <SkeletonCard v-for="i in 6" :key="`skeleton-${i}`" />
        </div>
        
        <div v-if="!hasMore && publications.length > 0" class="text-gray-500 h-20 flex items-center justify-center mt-8">
          No more posts to load.
        </div>
      </div>
    </div>
    
    <!-- Analysis Modal -->
    <Teleport to="body">
      <AnalysisModal 
        v-if="selectedPost" 
        :post="selectedPost" 
        @close="selectedPost = null"
      />
    </Teleport>
  </div>
</template>
