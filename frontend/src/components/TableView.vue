<template>
  <div>
    <div class="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm my-4 w-full">
      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm text-slate-700">
          <thead class="bg-slate-50 text-slate-500 uppercase text-[11px] font-bold tracking-wider border-b border-slate-200">
            <tr>
              <th class="px-4 py-3.5">Foto</th>
              <th class="px-4 py-3.5 cursor-pointer hover:text-slate-900" @click="handleSort('title')">
                <div class="flex items-center gap-1">
                  Annuncio <ArrowUpDown class="w-3 h-3" />
                </div>
              </th>
              <th class="px-4 py-3.5 cursor-pointer hover:text-slate-900" @click="handleSort('city')">
                <div class="flex items-center gap-1">
                  Città / Zona <ArrowUpDown class="w-3 h-3" />
                </div>
              </th>
              <th class="px-4 py-3.5 cursor-pointer hover:text-slate-900" @click="handleSort('monthlyPrice')">
                <div class="flex items-center gap-1">
                  Canone / Mese <ArrowUpDown class="w-3 h-3" />
                </div>
              </th>
              <th class="px-4 py-3.5">Stima 2 Mesi</th>
              <th class="px-4 py-3.5">Internet, Work & Auto</th>
              <th class="px-4 py-3.5 cursor-pointer hover:text-slate-900" @click="handleSort('status')">
                <div class="flex items-center gap-1">
                  Stato Trattativa <ArrowUpDown class="w-3 h-3" />
                </div>
              </th>
              <th class="px-4 py-3.5">Referente</th>
              <th class="px-4 py-3.5 text-right">Azioni</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-if="sortedRentals.length === 0">
              <td colspan="9" class="px-4 py-8 text-center text-slate-400">
                Nessun annuncio trovato.
              </td>
            </tr>
            <tr v-else v-for="rental in sortedRentals" :key="rental._id" class="hover:bg-slate-50/80 transition">
              
              <!-- Photo Thumbnail -->
              <td class="px-4 py-3.5 w-16">
                <button
                  v-if="rental.images && rental.images.length > 0"
                  @click="openGallery(rental.images, rental.title)"
                  class="relative group w-12 h-12 rounded-xl overflow-hidden border border-slate-200 shadow-sm block focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  title="Visualizza foto"
                >
                  <img :src="rental.images[0]" :alt="rental.title" class="w-full h-full object-cover group-hover:scale-110 transition duration-200" />
                  <span v-if="rental.images.length > 1" class="absolute bottom-0.5 right-0.5 bg-black/75 text-white text-[9px] font-bold px-1 rounded">
                    +{{ rental.images.length - 1 }}
                  </span>
                </button>
                <div v-else class="w-12 h-12 rounded-xl bg-slate-100 border border-slate-200 flex items-center justify-center text-slate-400" title="Nessuna foto">
                  <ImageIcon class="w-5 h-5 opacity-40" />
                </div>
              </td>

              <!-- Annuncio & Platform -->
              <td class="px-4 py-3.5 max-w-xs">
                <div class="font-bold text-slate-900 truncate hover:text-indigo-600">
                  {{ rental.title }}
                </div>
                <div class="flex items-center gap-2 mt-1">
                  <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 border border-slate-200 text-slate-700">
                    {{ rental.platform }}
                  </span>
                  <a
                    v-if="rental.url"
                    :href="rental.url"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="text-slate-400 hover:text-indigo-600 text-xs flex items-center gap-0.5"
                  >
                    <ExternalLink class="w-3 h-3" /> Link
                  </a>
                </div>
              </td>

              <!-- Città -->
              <td class="px-4 py-3.5">
                <div class="flex items-center gap-1 font-semibold text-slate-800">
                  <MapPin class="w-3.5 h-3.5 text-rose-500 shrink-0" />
                  {{ rental.city }}
                </div>
                <div v-if="rental.address" class="text-xs text-slate-400 truncate">{{ rental.address }}</div>
              </td>

              <!-- Canone, Utenze e Condominio -->
              <td class="px-4 py-3.5 font-bold text-emerald-600">
                {{ rental.monthlyPrice }}€
                <div class="text-[11px] font-normal text-slate-400">
                  Ut.: {{ rental.utilities }} {{ rental.utilitiesPriceEstimate > 0 ? `(+${rental.utilitiesPriceEstimate}€)` : '' }}
                </div>
                <div class="text-[11px] font-normal text-slate-400">
                  Cond.: {{ rental.condoFees || 'Escluse' }} {{ rental.condoFeesPriceEstimate > 0 ? `(+${rental.condoFeesPriceEstimate}€)` : '' }}
                </div>
              </td>

              <!-- Stima 2 Mesi -->
              <td class="px-4 py-3.5">
                <div class="font-black text-slate-900">
                  {{ (rental.monthlyPrice + (rental.utilitiesPriceEstimate || 0) + (rental.condoFeesPriceEstimate || 0)) * 2 }}€
                </div>
                <div v-if="rental.deposit > 0" class="text-[11px] text-slate-400">+ Caparra {{ rental.deposit }}€</div>
              </td>

              <!-- Internet, Work & Parking -->
              <td class="px-4 py-3.5">
                <div class="flex items-center gap-1 text-xs text-slate-800 font-semibold">
                  <Wifi class="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                  <span class="truncate">{{ rental.wifiType }}</span>
                </div>
                <div class="flex items-center gap-1 text-xs text-slate-500 mt-0.5">
                  <Laptop class="w-3.5 h-3.5 shrink-0 text-cyan-600" />
                  <span class="truncate">{{ rental.workspaceType }}</span>
                </div>
                <div class="flex items-center gap-1 text-xs text-slate-500 mt-0.5">
                  <Car class="w-3.5 h-3.5 shrink-0 text-amber-600" />
                  <span class="truncate">{{ rental.parkingType || 'Parcheggio libero in strada' }}</span>
                </div>
              </td>

              <!-- Stato Trattativa -->
              <td class="px-4 py-3.5">
                <select
                  :value="rental.status"
                  @change="$emit('statusChange', rental._id, ($event.target as HTMLSelectElement).value)"
                  class="bg-slate-50 border border-slate-300 text-xs font-semibold rounded-lg px-2.5 py-1 text-slate-800 focus:ring-2 focus:ring-indigo-500"
                >
                  <option v-for="s in STATUSES" :key="s" :value="s">{{ s }}</option>
                </select>
              </td>

              <!-- Referente -->
              <td class="px-4 py-3.5 text-xs">
                <div class="font-semibold text-slate-800">{{ rental.contactName || '-' }}</div>
                <div class="text-slate-400">{{ rental.contactPhone || '-' }}</div>
              </td>

              <!-- Azioni -->
              <td class="px-4 py-3.5 text-right">
                <div class="flex items-center justify-end gap-1">
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
import { ExternalLink, Edit, Trash2, MessageSquare, Wifi, Laptop, MapPin, ArrowUpDown, Image as ImageIcon, Car } from 'lucide-vue-next';

const props = defineProps<{
  rentals: Rental[];
}>();

defineEmits(['statusChange', 'edit', 'delete', 'openQuickMessage']);

const STATUSES: StatusType[] = ['Bozza', 'Contattato', 'In Attesa', 'Visita/Videochiamata', 'Opzionato', 'Scartato', 'Confermato'];

const sortField = ref<keyof Rental>('updatedAt');
const sortAsc = ref(false);

// Gallery state
const galleryImages = ref<string[]>([]);
const galleryTitle = ref('');
const isGalleryOpen = ref(false);

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
