<template>
  <div class="bg-white rounded-2xl w-full sm:w-[320px] overflow-hidden shadow-sm border border-gray-100 flex-shrink-0 relative">
    <!-- Header Video Placeholder Skeleton -->
    <div class="relative h-48 bg-slate-200 w-full overflow-hidden animate-pulse">
      <!-- Gradient overlay simulation -->
      <div class="absolute inset-0 bg-gradient-to-t from-slate-300/60 to-transparent pointer-events-none"></div>
      
      <!-- Top Right overlay for views skeleton -->
      <div class="absolute top-2 right-2 bg-slate-300 w-16 h-6 rounded"></div>
    </div>
    
    <div class="p-4">
      <!-- User Info Skeleton -->
      <div class="flex items-center gap-2 text-sm text-gray-500 mb-2">
         <div class="w-6 h-6 rounded-full bg-slate-200 animate-pulse"></div>
         <div class="w-24 h-4 bg-slate-200 rounded animate-pulse"></div>
      </div>
      
      <!-- Title Skeleton -->
      <div class="w-3/4 h-5 bg-slate-200 rounded mb-1 animate-pulse"></div>
      
      <!-- Date Skeleton -->
      <div class="w-1/3 h-3 bg-slate-100 rounded mb-3 animate-pulse"></div>
      
      <!-- Body Text Skeleton -->
      <div class="space-y-2 mb-4">
         <div class="w-full h-3 bg-slate-100 rounded animate-pulse"></div>
         <div class="w-5/6 h-3 bg-slate-100 rounded animate-pulse"></div>
         <div class="w-4/6 h-3 bg-slate-100 rounded animate-pulse"></div>
      </div>
      
      <!-- Button Skeleton -->
      <div class="w-full h-10 bg-slate-200 rounded-xl animate-pulse mt-4"></div>
    </div>
  </div>
</template>
