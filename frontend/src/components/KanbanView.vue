<template>
  <div>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 py-4 w-full">
      <div
        v-for="col in COLUMNS"
        :key="col.id"
        :class="[
          'bg-white border-t-4 border-x border-b border-slate-200 rounded-2xl flex flex-col shadow-sm max-h-[700px]',
          col.borderColor
        ]"
      >
        <!-- Column Header -->
        <div class="p-3.5 border-b border-slate-100 flex items-center justify-between bg-slate-50/80 rounded-t-xl">
          <div class="flex items-center gap-2">
            <h3 class="font-bold text-sm text-slate-800">{{ col.title }}</h3>
            <span :class="['text-xs px-2 py-0.5 rounded-full font-bold border', col.badgeBg, col.badgeText]">
              {{ getColRentals(col.id).length }}
            </span>
          </div>
        </div>

        <!-- Cards Area -->
        <div class="p-3 space-y-3 flex-1 overflow-y-auto min-h-[140px] rounded-b-2xl">
          <div
            v-for="rental in getColRentals(col.id)"
            :key="rental._id"
            class="bg-white border border-slate-200 hover:border-indigo-400 rounded-xl p-3.5 shadow-sm transition-all group overflow-hidden"
          >
            <!-- Cover Photo if available -->
            <div
              v-if="rental.images && rental.images.length > 0"
              @click="openGallery(rental.images, rental.title)"
              class="relative -mx-3.5 -mt-3.5 mb-3 h-32 bg-slate-100 overflow-hidden cursor-pointer group/img"
            >
              <img
                :src="rental.images[0]"
                :alt="rental.title"
                class="w-full h-full object-cover group-hover/img:scale-105 transition duration-300"
              />
              <div class="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent opacity-60"></div>
              <span class="absolute bottom-2 right-2 bg-black/75 backdrop-blur-sm text-white text-[10px] font-bold px-2 py-0.5 rounded-md flex items-center gap-1">
                <ImageIcon class="w-3 h-3" /> {{ rental.images.length }} foto
              </span>
            </div>

            <!-- Top Bar: Platform + Link + Clean Score Badge -->
            <div class="flex items-center justify-between mb-2">
              <span :class="['text-[10px] font-bold px-2.5 py-0.5 rounded-full border', getPlatformBadge(rental.platform)]">
                {{ rental.platform }}
              </span>
              
              <div class="flex items-center gap-1.5">
                <div
                  :title="`🏡 Quartiere: ${rental.ratingNeighborhood || 3}/5 | 🛒 Servizi: ${rental.ratingServices || 3}/5 | 🚉 Trasporti: ${rental.ratingTransport || 3}/5`"
                  :class="['inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-white text-[10px] font-bold shadow-sm cursor-help', getScoreBadgeBg(Number(calculateAvgRating(rental)))]"
                >
                  <BarChart2 class="w-3 h-3" />
                  <span>Zona {{ calculateAvgRating(rental) }}/5</span>
                </div>

                <a
                  v-if="rental.url"
                  :href="rental.url"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="text-slate-400 hover:text-indigo-600 transition p-1"
                  title="Apri link originale"
                >
                  <ExternalLink class="w-3.5 h-3.5" />
                </a>
              </div>
            </div>

            <!-- Title & City -->
            <h4 class="font-bold text-sm text-slate-900 line-clamp-2 mb-1.5 group-hover:text-indigo-600 transition">
              {{ rental.title }}
            </h4>

            <div class="flex items-center justify-between gap-1 text-xs text-slate-500 mb-3">
              <div class="flex items-center gap-1 truncate">
                <MapPin class="w-3.5 h-3.5 text-rose-500 shrink-0" />
                <span class="truncate font-medium text-slate-700">{{ rental.city }}</span>
              </div>
              <button
                @click="$emit('openMap', rental)"
                class="text-[11px] font-bold text-indigo-600 hover:text-indigo-700 hover:bg-indigo-50 px-2 py-0.5 rounded-md transition flex items-center gap-1 shrink-0"
              >
                <Compass class="w-3 h-3" /> Mappa Servizi
              </button>
            </div>

            <!-- Smart Work & Parking Features -->
            <div class="grid grid-cols-2 gap-1.5 text-[11px] mb-2">
              <div :class="['flex items-center gap-1.5 px-2 py-1 rounded-lg border', getWifiBadge(rental.wifiType)]">
                <Wifi class="w-3 h-3 shrink-0" />
                <span class="truncate font-semibold">{{ rental.wifiType }}</span>
              </div>
              <div class="flex items-center gap-1.5 px-2 py-1 rounded-lg border border-slate-200 bg-slate-50 text-slate-700">
                <Laptop class="w-3 h-3 text-cyan-600 shrink-0" />
                <span class="truncate font-medium">{{ rental.workspaceType }}</span>
              </div>
            </div>

            <!-- Parking Badge -->
            <div class="flex items-center gap-1.5 px-2 py-1 rounded-lg border border-amber-200 bg-amber-50/80 text-amber-800 text-[11px] mb-3">
              <Car class="w-3 h-3 text-amber-600 shrink-0" />
              <span class="truncate font-semibold">{{ rental.parkingType || 'Parcheggio libero in strada' }}</span>
            </div>

            <!-- Price Breakdown -->
            <div class="bg-slate-50 rounded-xl p-2.5 border border-slate-200/80 mb-3 text-xs space-y-1">
              <div class="flex justify-between items-center">
                <span class="text-slate-500 font-medium">Canone mensile:</span>
                <span class="font-bold text-emerald-600">{{ rental.monthlyPrice }}€ / mese</span>
              </div>
              <div class="flex justify-between items-center text-[11px]">
                <span class="text-slate-400">Utenze ({{ rental.utilities }}):</span>
                <span class="text-slate-600 font-medium">
                  {{ rental.utilities === 'Incluse' ? '0€' : `+${rental.utilitiesPriceEstimate}€ est.` }}
                </span>
              </div>
              <div class="flex justify-between items-center text-[11px]">
                <span class="text-slate-400">Condominio ({{ rental.condoFees || 'Escluse' }}):</span>
                <span class="text-slate-600 font-medium">
                  {{ rental.condoFees === 'Incluse' ? '0€' : `+${rental.condoFeesPriceEstimate || 0}€ est.` }}
                </span>
              </div>
              <div class="flex justify-between items-center text-[11px] pt-1.5 border-t border-slate-200">
                <span class="text-slate-600 font-semibold">Totale {{ getRentalMonths(rental) }} mesi:</span>
                <span class="font-black text-slate-900">
                  {{ (rental.monthlyPrice + (rental.utilitiesPriceEstimate || 0) + (rental.condoFeesPriceEstimate || 0)) * getRentalMonths(rental) }}€
                </span>
              </div>
            </div>

            <div v-if="rental.availablePeriod" class="flex items-center gap-1.5 text-[11px] text-slate-500 mb-3">
              <Calendar class="w-3.5 h-3.5 text-indigo-500 shrink-0" />
              <span class="truncate font-medium">{{ rental.availablePeriod }}</span>
            </div>

            <!-- Footer Actions -->
            <div class="pt-2 border-t border-slate-100 flex items-center justify-between gap-1 text-slate-500">
              <button
                @click="$emit('openQuickMessage', rental)"
                class="flex items-center gap-1 text-xs text-indigo-600 hover:text-indigo-700 font-semibold hover:bg-indigo-50 px-2 py-1 rounded-lg transition"
                title="Genera messaggio WhatsApp"
              >
                <MessageSquare class="w-3.5 h-3.5" />
                <span>Messaggio</span>
              </button>

              <div class="flex items-center gap-1">
                <button
                  @click="$emit('edit', rental)"
                  class="p-1.5 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition"
                  title="Modifica"
                >
                  <Edit class="w-3.5 h-3.5" />
                </button>
                <button
                  @click="$emit('delete', rental._id)"
                  class="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition"
                  title="Elimina"
                >
                  <Trash2 class="w-3.5 h-3.5" />
                </button>
              </div>
            </div>

          </div>
        </div>

      </div>
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
import { ref } from 'vue';
import { Rental, StatusType } from '../types/rental';
import ImageGalleryModal from './ImageGalleryModal.vue';
import { Wifi, Laptop, MapPin, ExternalLink, MessageSquare, Edit, Trash2, Calendar, Image as ImageIcon, Car, BarChart2, Compass } from 'lucide-vue-next';

const props = withDefaults(
  defineProps<{
    rentals: Rental[];
    stayMonths?: number;
  }>(),
  {
    stayMonths: 6
  }
);

defineEmits(['statusChange', 'edit', 'delete', 'openQuickMessage', 'openMap']);

const COLUMNS: { id: StatusType; title: string; borderColor: string; badgeBg: string; badgeText: string }[] = [
  { id: 'Bozza', title: 'Bozza', borderColor: 'border-slate-300', badgeBg: 'bg-slate-100', badgeText: 'text-slate-700' },
  { id: 'Contattato', title: 'Contattato', borderColor: 'border-blue-400', badgeBg: 'bg-blue-50', badgeText: 'text-blue-700' },
  { id: 'In Attesa', title: 'In Attesa', borderColor: 'border-amber-400', badgeBg: 'bg-amber-50', badgeText: 'text-amber-700' },
  { id: 'Visita/Videochiamata', title: 'Visita / Call', borderColor: 'border-purple-400', badgeBg: 'bg-purple-50', badgeText: 'text-purple-700' },
  { id: 'Opzionato', title: 'Opzionato', borderColor: 'border-cyan-400', badgeBg: 'bg-cyan-50', badgeText: 'text-cyan-700' },
  { id: 'Confermato', title: 'Confermato 🎉', borderColor: 'border-emerald-400', badgeBg: 'bg-emerald-50', badgeText: 'text-emerald-700' },
  { id: 'Scartato', title: 'Scartato', borderColor: 'border-rose-300', badgeBg: 'bg-rose-50', badgeText: 'text-rose-700' },
];

const galleryImages = ref<string[]>([]);
const galleryTitle = ref('');
const isGalleryOpen = ref(false);

const getRentalMonths = (rental: Rental) => {
  if (rental.availablePeriod) {
    const match = rental.availablePeriod.match(/(\d+)/);
    if (match && match[1]) {
      const parsed = parseInt(match[1], 10);
      if (parsed > 0 && parsed <= 36) {
        return parsed;
      }
    }
  }
  return props.stayMonths || 6;
};

const getScoreBadgeBg = (score: number) => {
  if (score >= 4.5) return 'bg-emerald-600';
  if (score >= 3.8) return 'bg-teal-600';
  if (score >= 3.0) return 'bg-indigo-600';
  if (score >= 2.0) return 'bg-amber-500';
  return 'bg-rose-500';
};

const calculateAvgRating = (rental: Rental) => {
  const n = rental.ratingNeighborhood ?? 3;
  const s = rental.ratingServices ?? 3;
  const t = rental.ratingTransport ?? 3;
  return ((n + s + t) / 3).toFixed(1);
};

const getColRentals = (colId: StatusType) => {
  return props.rentals.filter((r) => r.status === colId);
};

const openGallery = (images: string[], title: string) => {
  if (!images || images.length === 0) return;
  galleryImages.value = images;
  galleryTitle.value = title;
  isGalleryOpen.value = true;
};

const getPlatformBadge = (platform: string) => {
  switch (platform) {
    case 'Facebook':
      return 'bg-blue-50 text-blue-700 border-blue-200';
    case 'Subito':
      return 'bg-red-50 text-red-700 border-red-200';
    case 'Idealista':
      return 'bg-lime-50 text-lime-800 border-lime-200';
    case 'Immobiliare':
      return 'bg-cyan-50 text-cyan-800 border-cyan-200';
    default:
      return 'bg-slate-100 text-slate-700 border-slate-200';
  }
};

const getWifiBadge = (wifiType: string) => {
  if (wifiType.includes('Fibra')) return 'bg-emerald-50 text-emerald-800 border-emerald-200';
  if (wifiType.includes('FTTC') || wifiType.includes('FWA')) return 'bg-sky-50 text-sky-800 border-sky-200';
  if (wifiType.includes('verificare')) return 'bg-amber-50 text-amber-800 border-amber-200';
  return 'bg-slate-100 text-slate-600 border-slate-200';
};
</script>
