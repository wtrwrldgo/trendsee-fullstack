<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useIntersectionObserver } from '@vueuse/core';
import api from '../api';
import PostCard from '../components/PostCard.vue';
import AnalysisModal from '../components/AnalysisModal.vue';

interface Publication {
  id: number;
  user_id: number;
  title: string;
  text: string;
  created_at: string;
  updated_at: string;
}

const publications = ref<Publication[]>([]);
const loading = ref(false);
const limit = 10;
const offset = ref(0);
const hasMore = ref(true);
const target = ref(null);
const selectedPost = ref<Publication | null>(null);

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
    console.error("Error fetching publications", error);
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
    <div class="max-w-4xl mx-auto">
      <h1 class="text-3xl font-bold mb-8 text-gray-800">My Publications feed</h1>
      
      <div class="flex flex-wrap gap-6">
        <PostCard 
          v-for="post in publications" 
          :key="post.id" 
          :post="post" 
          @analyze="openAnalysis(post)"
        />
      </div>
      
      <!-- Infinite Scroll Trigger -->
      <div ref="target" class="h-20 flex items-center justify-center mt-8">
        <div v-if="loading" class="text-blue-500 font-semibold animate-pulse">
          Loading more posts... (might take 2s for cold ones)
        </div>
        <div v-else-if="!hasMore" class="text-gray-500">
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
