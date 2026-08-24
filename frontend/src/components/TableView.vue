<template>
  <div>
    <div class="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm my-4 w-full">
      <table class="w-full text-left text-sm text-slate-700 table-auto border-collapse">
        <thead class="bg-slate-50/90 text-slate-500 uppercase text-[11px] font-bold tracking-wider border-b border-slate-200">
          <tr>
            <th class="px-3 py-3 w-14">Foto</th>
            <th class="px-3 py-3 cursor-pointer hover:text-slate-900" @click="handleSort('title')">
              <div class="flex items-center gap-1">
                Annuncio & Località <ArrowUpDown class="w-3 h-3" />
              </div>
            </th>
            <th class="px-3 py-3 text-center cursor-pointer hover:text-slate-900" @click="handleSort('monthlyPrice')">
              <div class="flex items-center justify-center gap-1">
                Prezzo & Stima 2M <ArrowUpDown class="w-3 h-3" />
              </div>
            </th>
            <th class="px-3 py-3 text-center">Score Zona</th>
            <th class="px-3 py-3">Internet & Auto</th>
            <th class="px-3 py-3 cursor-pointer hover:text-slate-900" @click="handleSort('status')">
              <div class="flex items-center gap-1">
                Stato Trattativa <ArrowUpDown class="w-3 h-3" />
              </div>
            </th>
            <th class="px-3 py-3">Referente</th>
            <th class="px-3 py-3 text-right">Azioni</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr v-if="sortedRentals.length === 0">
            <td colspan="8" class="px-4 py-8 text-center text-slate-400">
              Nessun annuncio trovato.
            </td>
          </tr>
          <tr v-else v-for="rental in sortedRentals" :key="rental._id" class="hover:bg-slate-50/80 transition">
            
            <!-- Foto Thumbnail -->
            <td class="px-3 py-3 w-14">
              <button
                v-if="rental.images && rental.images.length > 0"
                @click="openGallery(rental.images, rental.title)"
                class="relative group w-11 h-11 rounded-xl overflow-hidden border border-slate-200 shadow-sm block focus:outline-none focus:ring-2 focus:ring-indigo-500 shrink-0"
                title="Visualizza foto"
              >
                <img :src="rental.images[0]" :alt="rental.title" class="w-full h-full object-cover group-hover:scale-110 transition duration-200" />
                <span v-if="rental.images.length > 1" class="absolute bottom-0.5 right-0.5 bg-black/75 text-white text-[9px] font-bold px-1 rounded">
                  +{{ rental.images.length - 1 }}
                </span>
              </button>
              <div v-else class="w-11 h-11 rounded-xl bg-slate-100 border border-slate-200 flex items-center justify-center text-slate-400 shrink-0" title="Nessuna foto">
                <ImageIcon class="w-4 h-4 opacity-40" />
              </div>
            </td>

            <!-- Annuncio & Località -->
            <td class="px-3 py-3 max-w-[220px]">
              <div class="font-bold text-slate-900 text-xs sm:text-sm truncate hover:text-indigo-600">
                {{ rental.title }}
              </div>

              <div class="flex items-center gap-1.5 text-xs text-slate-500 mt-0.5">
                <MapPin class="w-3.5 h-3.5 text-rose-500 shrink-0" />
                <span class="font-semibold text-slate-800 truncate">{{ rental.city }}</span>
                <span v-if="rental.address" class="text-slate-400 truncate text-[11px]">({{ rental.address }})</span>
              </div>

              <div class="flex items-center gap-2 mt-1">
                <span class="text-[10px] font-bold px-2 py-0.5 rounded-md bg-slate-100 border border-slate-200 text-slate-700">
                  {{ rental.platform }}
                </span>
                <a
                  v-if="rental.url"
                  :href="rental.url"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="text-slate-400 hover:text-indigo-600 text-[11px] flex items-center gap-0.5"
                >
                  <ExternalLink class="w-3 h-3" /> Link
                </a>
              </div>
            </td>

            <!-- Prezzo Mensile & Stima 2 Mesi (Combinato) -->
            <td class="px-3 py-3 text-center">
              <div class="font-black text-emerald-600 text-sm">
                {{ rental.monthlyPrice }}€ <span class="text-[10px] text-slate-400 font-medium">/mese</span>
              </div>
              <div class="text-[11px] font-bold text-slate-900 mt-0.5">
                Stima 2M: {{ (rental.monthlyPrice + (rental.utilitiesPriceEstimate || 0) + (rental.condoFeesPriceEstimate || 0)) * 2 }}€
              </div>
              <div class="text-[10px] text-slate-400">
                Ut.: {{ rental.utilities }} • Cond.: {{ rental.condoFees || 'Escluse' }}
              </div>
            </td>

            <!-- Scoreboard Zona Pulito -->
            <td class="px-3 py-3 text-center">
              <div
                :title="`🏡 Quartiere: ${rental.ratingNeighborhood || 3}/5 | 🛒 Servizi: ${rental.ratingServices || 3}/5 | 🚉 Trasporti: ${rental.ratingTransport || 3}/5`"
                class="inline-flex items-center gap-1 px-2.5 py-1 rounded-xl text-white font-black text-xs shadow-sm cursor-help transition hover:scale-105"
                :class="getScoreBadgeBg(Number(calculateAvgRating(rental)))"
              >
                <BarChart2 class="w-3 h-3 shrink-0 opacity-90" />
                <span>{{ calculateAvgRating(rental) }}</span>
                <span class="text-[10px] font-normal opacity-80">/5</span>
              </div>
              <div class="text-[10px] font-semibold text-slate-500 mt-0.5">
                {{ getScoreLabel(Number(calculateAvgRating(rental))) }}
              </div>
            </td>

            <!-- Internet, Work & Auto (Inline Compact) -->
            <td class="px-3 py-3 text-xs">
              <div class="flex items-center gap-1 text-slate-800 font-semibold truncate">
                <Wifi class="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                <span class="truncate">{{ rental.wifiType }}</span>
              </div>
              <div class="flex items-center gap-1 text-slate-500 mt-0.5 truncate">
                <Laptop class="w-3.5 h-3.5 shrink-0 text-cyan-600" />
                <span class="truncate">{{ rental.workspaceType }}</span>
              </div>
              <div class="flex items-center gap-1 text-slate-500 mt-0.5 truncate">
                <Car class="w-3.5 h-3.5 shrink-0 text-amber-600" />
                <span class="truncate text-[11px]">{{ rental.parkingType || 'Parcheggio libero' }}</span>
              </div>
            </td>

            <!-- Stato Trattativa -->
            <td class="px-3 py-3">
              <select
                :value="rental.status"
                @change="$emit('statusChange', rental._id, ($event.target as HTMLSelectElement).value)"
                class="bg-slate-50 border border-slate-300 text-xs font-semibold rounded-lg px-2 py-1 text-slate-800 focus:ring-2 focus:ring-indigo-500 max-w-[130px]"
              >
                <option v-for="s in STATUSES" :key="s" :value="s">{{ s }}</option>
              </select>
            </td>

            <!-- Referente -->
            <td class="px-3 py-3 text-xs max-w-[110px]">
              <div class="font-semibold text-slate-800 truncate">{{ rental.contactName || '-' }}</div>
              <div class="text-slate-400 text-[11px] truncate">{{ rental.contactPhone || '-' }}</div>
            </td>

            <!-- Azioni (Compatte) -->
            <td class="px-3 py-3 text-right">
              <div class="flex items-center justify-end gap-1">
                <button
                  @click="$emit('openMap', rental)"
                  class="p-1.5 hover:bg-emerald-50 text-emerald-600 hover:text-emerald-700 rounded-lg transition"
                  title="Apri Mappa & Servizi Zona"
                >
                  <Compass class="w-4 h-4" />
                </button>
                <button
                  @click="$emit('openQuickMessage', rental)"
                  class="p-1.5 hover:bg-indigo-50 text-indigo-600 rounded-lg transition"
                  title="Genera messaggio WhatsApp"
                >
                  <MessageSquare class="w-4 h-4" />
                </button>
                <button
                  @click="$emit('edit', rental)"
                  class="p-1.5 hover:bg-slate-100 text-slate-500 hover:text-slate-900 rounded-lg transition"
                  title="Modifica"
                >
                  <Edit class="w-4 h-4" />
                </button>
                <button
                  @click="$emit('delete', rental._id)"
                  class="p-1.5 hover:bg-rose-50 text-slate-400 hover:text-rose-600 rounded-lg transition"
                  title="Elimina"
                >
                  <Trash2 class="w-4 h-4" />
                </button>
              </div>
            </td>

          </tr>
        </tbody>
      </table>
    </div>

    <!-- Gallery Modal -->
    <ImageGalleryModal
      :isOpen="isGalleryOpen"
      @close="isGalleryOpen = false"
      :images="galleryImages"
      :title="galleryTitle"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { Rental, StatusType } from '../types/rental';
import ImageGalleryModal from './ImageGalleryModal.vue';
import { ExternalLink, Edit, Trash2, MessageSquare, Wifi, Laptop, MapPin, ArrowUpDown, Image as ImageIcon, Car, BarChart2, Compass } from 'lucide-vue-next';

const props = defineProps<{
  rentals: Rental[];
}>();

defineEmits(['statusChange', 'edit', 'delete', 'openQuickMessage', 'openMap']);

const STATUSES: StatusType[] = ['Bozza', 'Contattato', 'In Attesa', 'Visita/Videochiamata', 'Opzionato', 'Scartato', 'Confermato'];

const sortField = ref<keyof Rental>('updatedAt');
const sortAsc = ref(false);

// Gallery state
const galleryImages = ref<string[]>([]);
const galleryTitle = ref('');
const isGalleryOpen = ref(false);

const calculateAvgRating = (rental: Rental) => {
  const n = rental.ratingNeighborhood ?? 3;
  const s = rental.ratingServices ?? 3;
  const t = rental.ratingTransport ?? 3;
  return ((n + s + t) / 3).toFixed(1);
};

const getScoreBadgeBg = (score: number) => {
  if (score >= 4.5) return 'bg-emerald-600';
  if (score >= 3.8) return 'bg-teal-600';
  if (score >= 3.0) return 'bg-indigo-600';
  if (score >= 2.0) return 'bg-amber-500';
  return 'bg-rose-500';
};

const getScoreLabel = (score: number) => {
  if (score >= 4.5) return 'Eccellente';
  if (score >= 3.8) return 'Ottima Zona';
  if (score >= 3.0) return 'Buona Zona';
  if (score >= 2.0) return 'Discreta';
  return 'Zona Scarsa';
};

const handleSort = (field: keyof Rental) => {
  if (sortField.value === field) {
    sortAsc.value = !sortAsc.value;
  } else {
    sortField.value = field;
    sortAsc.value = true;
  }
};

const openGallery = (images: string[], title: string) => {
  if (!images || images.length === 0) return;
  galleryImages.value = images;
  galleryTitle.value = title;
  isGalleryOpen.value = true;
};

const sortedRentals = computed(() => {
  return [...props.rentals].sort((a, b) => {
    let valA = a[sortField.value] ?? '';
    let valB = b[sortField.value] ?? '';

    if (typeof valA === 'number' && typeof valB === 'number') {
      return sortAsc.value ? valA - valB : valB - valA;
    }

    return sortAsc.value
      ? String(valA).localeCompare(String(valB))
      : String(valB).localeCompare(String(valA));
  });
});
</script>
