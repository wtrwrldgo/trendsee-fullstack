<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';

const props = defineProps({
  value: {
    type: Number,
    required: true
  },
  duration: {
    type: Number,
    default: 1500
  },
  format: {
    type: String,
    default: 'number', // 'number', 'compact'
  }
});

const displayValue = ref(0);

onMounted(() => {
  const target = props.value;
  const startTime = Date.now();
  
  const updateCounter = () => {
    const now = Date.now();
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / props.duration, 1);
    
    // Ease out expo
    const easeProgress = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
    
    displayValue.value = Math.floor(easeProgress * target);
    
    if (progress < 1) {
      requestAnimationFrame(updateCounter);
    } else {
      displayValue.value = target; // Ensure it ends exactly on the target
    }
  };
  
  // Add a tiny delay so the modal animation finishes first
  setTimeout(() => {
    requestAnimationFrame(updateCounter);
  }, 300);
});

const formattedValue = computed(() => {
  if (props.format === 'compact') {
    return new Intl.NumberFormat('en-US', {
      notation: 'compact',
      maximumFractionDigits: 1
    }).format(displayValue.value);
  }
  return new Intl.NumberFormat('en-US').format(displayValue.value);
});
</script>

<template>
  <span>{{ formattedValue }}</span>
</template>
