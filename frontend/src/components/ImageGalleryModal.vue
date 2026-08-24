<template>
  <div v-if="isOpen && images && images.length > 0" class="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
    <div class="relative bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-4xl max-h-[90vh] shadow-2xl flex flex-col overflow-hidden">
      
      <!-- Header -->
      <div class="px-6 py-4 bg-slate-900 border-b border-slate-800 flex items-center justify-between">
        <div class="flex items-center gap-2 text-slate-200">
          <ImageIcon class="w-5 h-5 text-indigo-400" />
          <h3 class="font-bold text-white text-base truncate max-w-lg">{{ title }}</h3>
          <span class="text-xs bg-slate-800 text-slate-400 px-2 py-0.5 rounded-full border border-slate-700">
            {{ currentIndex + 1 }} / {{ images.length }}
          </span>
        </div>
        <button @click="$emit('close')" class="text-slate-400 hover:text-white p-1 rounded-lg">
          <X class="w-6 h-6" />
        </button>
      </div>

      <!-- Main Image Display -->
      <div class="relative flex-1 bg-black flex items-center justify-center min-h-[350px] p-4 overflow-hidden">
        <img
          :src="images[currentIndex]"
          :alt="`Foto ${currentIndex + 1}`"
          class="max-h-[65vh] w-auto max-w-full object-contain rounded-lg shadow-lg"
        />

        <template v-if="images.length > 1">
          <button
            @click="handlePrev"
            class="absolute left-4 top-1/2 -translate-y-1/2 bg-black/60 hover:bg-black/90 text-white p-2.5 rounded-full backdrop-blur-sm transition border border-white/10"
          >
            <ChevronLeft class="w-6 h-6" />
          </button>
          <button
            @click="handleNext"
            class="absolute right-4 top-1/2 -translate-y-1/2 bg-black/60 hover:bg-black/90 text-white p-2.5 rounded-full backdrop-blur-sm transition border border-white/10"
          >
            <ChevronRight class="w-6 h-6" />
          </button>
        </template>
      </div>

      <!-- Thumbnails Bar -->
      <div v-if="images.length > 1" class="p-3 bg-slate-900 border-t border-slate-800 flex items-center justify-center gap-2 overflow-x-auto">
        <button
          v-for="(img, idx) in images"
          :key="idx"
          @click="currentIndex = idx"
          :class="[
            'relative w-14 h-14 rounded-lg overflow-hidden border-2 transition',
            idx === currentIndex ? 'border-indigo-500 scale-105 shadow-md' : 'border-transparent opacity-60 hover:opacity-100'
          ]"
        >
          <img :src="img" :alt="`Thumb ${idx}`" class="w-full h-full object-cover" />
        </button>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { X, ChevronLeft, ChevronRight, Image as ImageIcon } from 'lucide-vue-next';

const props = defineProps<{
  images: string[];
  title: string;
  isOpen: boolean;
}>();

defineEmits(['close']);

const currentIndex = ref(0);

watch(() => props.isOpen, (newVal) => {
  if (newVal) currentIndex.value = 0;
});

const handlePrev = () => {
  if (!props.images) return;
  currentIndex.value = currentIndex.value === 0 ? props.images.length - 1 : currentIndex.value - 1;
};

const handleNext = () => {
  if (!props.images) return;
  currentIndex.value = currentIndex.value === props.images.length - 1 ? 0 : currentIndex.value + 1;
};
</script>
