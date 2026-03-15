import { useLocalStorage } from '@vueuse/core';
import { computed } from 'vue';

// Maintain a global reactive Set-like array stored in browser LocalStorage
// Using an array of IDs avoids complex serialization
const likedPosts = useLocalStorage<number[]>('trendsee-liked-posts', []);

export function useLike(postId: number) {
  const isLiked = computed(() => likedPosts.value.includes(postId));

  const toggleLike = () => {
    if (isLiked.value) {
      likedPosts.value = likedPosts.value.filter(id => id !== postId);
    } else {
      likedPosts.value.push(postId);
    }
  };

  return {
    isLiked,
    toggleLike
  };
}
