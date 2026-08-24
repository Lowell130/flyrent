<template>
  <div v-if="isOpen && rental" class="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-white border border-slate-200 rounded-2xl w-full max-w-4xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
      
      <!-- Header -->
      <div class="px-6 py-3.5 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 bg-indigo-50 text-indigo-600 rounded-xl flex items-center justify-center border border-indigo-100">
            <MapPin class="w-4 h-4" />
          </div>
          <div>
            <h3 class="font-bold text-sm text-slate-900 line-clamp-1">
              Mappa Mappa & Servizi Zona: {{ rental.title }}
            </h3>
            <span class="text-xs text-slate-500 font-medium">
              {{ rental.city }} {{ rental.address ? `• ${rental.address}` : '' }}
            </span>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <a
            :href="googleMapsUrl"
            target="_blank"
            rel="noopener noreferrer"
            class="hidden sm:flex items-center gap-1.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-semibold px-3 py-1.5 rounded-xl text-xs border border-indigo-200 transition"
          >
            <ExternalLink class="w-3.5 h-3.5" />
            Apri su Google Maps
          </a>
          <button @click="$emit('close')" class="text-slate-400 hover:text-slate-700 p-1.5 rounded-xl hover:bg-slate-100 transition">
            <X class="w-5 h-5" />
          </button>
        </div>
      </div>

      <!-- POI Category Filter Bar -->
      <div class="bg-slate-50 border-b border-slate-200 px-6 py-2.5 flex items-center gap-2 overflow-x-auto text-xs font-semibold">
        <span class="text-slate-400 text-[11px] uppercase tracking-wider font-bold shrink-0">Esplora Vicinanza:</span>

        <button
          v-for="cat in POI_CATEGORIES"
          :key="cat.id"
          @click="toggleCategory(cat.id)"
          :class="[
            'px-3 py-1.5 rounded-xl font-bold border transition flex items-center gap-1.5 shrink-0',
            activeCategory === cat.id ? 'bg-indigo-600 text-white border-indigo-600 shadow-sm' : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-100'
          ]"
        >
          <span>{{ cat.icon }}</span>
          <span>{{ cat.label }}</span>
        </button>
      </div>

      <!-- Map & Sidebar Area -->
      <div class="flex-1 grid grid-cols-1 md:grid-cols-4 min-h-[420px] relative">
        
        <!-- Interactive Leaflet Map Container -->
        <div class="md:col-span-3 h-full min-h-[380px] w-full relative bg-slate-100">
          <div ref="mapContainer" class="w-full h-full min-h-[380px] z-10"></div>

          <!-- Map Loading overlay -->
          <div v-if="loadingGeocode" class="absolute inset-0 bg-white/80 backdrop-blur-sm z-20 flex items-center justify-center gap-2 text-xs font-bold text-slate-600">
            <div class="w-4 h-4 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
            <span>Localizzazione indirizzo in corso...</span>
          </div>
        </div>

        <!-- Sidebar: POI Results List -->
        <div class="md:col-span-1 bg-white border-l border-slate-200 p-4 overflow-y-auto space-y-3 max-h-[420px]">
          <div class="flex items-center justify-between">
            <h4 class="font-bold text-xs text-slate-800 uppercase tracking-wider">
              Punti d'Interesse
            </h4>
            <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">
              {{ pois.length }} trovati
            </span>
          </div>

          <div v-if="loadingPois" class="py-8 text-center text-xs text-slate-400 space-y-2">
            <div class="w-4 h-4 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
            <p>Ricerca {{ getCategoryLabel(activeCategory) }} nelle vicinanze...</p>
          </div>

          <div v-else-if="pois.length === 0" class="py-8 text-center text-xs text-slate-400">
            Nessun punto trovato in questa categoria. Seleziona una categoria in alto!
          </div>

          <div v-else class="space-y-2">
            <div
              v-for="(poi, idx) in pois"
              :key="idx"
              @click="focusPoi(poi)"
              class="p-2.5 rounded-xl border border-slate-200 hover:border-indigo-400 bg-slate-50/50 hover:bg-indigo-50/40 cursor-pointer transition text-xs space-y-1"
            >
              <div class="font-bold text-slate-900 truncate">
                {{ poi.name }}
              </div>
              <div class="text-[11px] text-slate-500 flex items-center justify-between">
                <span>{{ poi.type }}</span>
                <span v-if="poi.distance" class="font-semibold text-indigo-600">{{ poi.distance }} km</span>
              </div>
            </div>
          </div>

        </div>

      </div>

      <!-- Footer Info -->
      <div class="px-6 py-3 bg-slate-50 border-t border-slate-200 flex items-center justify-between text-xs text-slate-500">
        <div class="flex items-center gap-4">
          <span>🏡 Canone: <strong class="text-emerald-600">{{ rental.monthlyPrice }}€/mese</strong></span>
          <span>🚗 Parcheggio: <strong class="text-slate-700">{{ rental.parkingType }}</strong></span>
        </div>
        <span>Mappa interattiva OpenStreetMap / Nominatim</span>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onUnmounted, computed } from 'vue';
import { X, MapPin, ExternalLink } from 'lucide-vue-next';
import { Rental } from '../types/rental';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const props = defineProps<{
  isOpen: boolean;
  rental: Rental | null;
}>();

defineEmits(['close']);

const mapContainer = ref<HTMLElement | null>(null);
let map: L.Map | null = null;
let mainMarker: L.Marker | null = null;
let poiMarkers: L.Marker[] = [];

const loadingGeocode = ref(false);
const loadingPois = ref(false);
const currentLat = ref<number>(42.0008);
const currentLng = ref<number>(14.9961);
const activeCategory = ref<string>('supermarket');
const pois = ref<{ name: string; type: string; lat: number; lon: number; distance?: string }[]>([]);

const POI_CATEGORIES = [
  { id: 'supermarket', label: 'Supermercati', icon: '🛒' },
  { id: 'gym', label: 'Palestre & Sport', icon: '🏋️' },
  { id: 'station', label: 'Stazione & Mezzi', icon: '🚉' },
  { id: 'airport', label: 'Aeroporti', icon: '✈️' },
  { id: 'cafe', label: 'Bar & Co-working', icon: '☕' },
  { id: 'beach', label: 'Spiaggia & Parchi', icon: '🏖️' },
];

const googleMapsUrl = computed(() => {
  if (!props.rental) return '#';
  const query = encodeURIComponent(`${props.rental.address || ''} ${props.rental.city}`);
  return `https://www.google.com/maps/search/?api=1&query=${query}`;
});

const getCategoryLabel = (catId: string) => {
  const cat = POI_CATEGORIES.find((c) => c.id === catId);
  return cat ? cat.label : 'Servizi';
};

const calculateDistance = (lat1: number, lon1: number, lat2: number, lon2: number) => {
  const R = 6371; // km
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLon = ((lon2 - lon1) * Math.PI) / 180;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos((lat1 * Math.PI) / 180) * Math.cos((lat2 * Math.PI) / 180) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return (R * c).toFixed(1);
};

// Geocode rental property using Nominatim OpenStreetMap API
const geocodeRental = async () => {
  if (!props.rental) return;
  loadingGeocode.value = true;
  const query = `${props.rental.address || ''} ${props.rental.city} Italy`.trim();

  try {
    const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`);
    const data = await res.json();

    if (data && data.length > 0) {
      currentLat.value = parseFloat(data[0].lat);
      currentLng.value = parseFloat(data[0].lon);
    } else {
      // Fallback geocode city only
      const cityRes = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(props.rental.city + ' Italy')}`);
      const cityData = await cityRes.json();
      if (cityData && cityData.length > 0) {
        currentLat.value = parseFloat(cityData[0].lat);
        currentLng.value = parseFloat(cityData[0].lon);
      }
    }
  } catch (err) {
    console.error('Geocoding error:', err);
  } finally {
    loadingGeocode.value = false;
  }
};

// Search real POIs around the location using Nominatim search
const fetchPois = async (category: string) => {
  loadingPois.value = true;
  pois.value = [];
  clearPoiMarkers();

  let searchQuery = '';
  switch (category) {
    case 'supermarket':
      searchQuery = `supermercato ${props.rental?.city}`;
      break;
    case 'gym':
      searchQuery = `palestra ${props.rental?.city}`;
      break;
    case 'station':
      searchQuery = `stazione ${props.rental?.city}`;
      break;
    case 'airport':
      searchQuery = `aeroporto ${props.rental?.city}`;
      break;
    case 'cafe':
      searchQuery = `bar ${props.rental?.city}`;
      break;
    case 'beach':
      searchQuery = `spiaggia ${props.rental?.city}`;
      break;
    default:
      searchQuery = `supermercato ${props.rental?.city}`;
  }

  try {
    const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchQuery)}&limit=10`);
    const data = await res.json();

    if (data && data.length > 0) {
      const results = data.map((item: any) => {
        const lat = parseFloat(item.lat);
        const lon = parseFloat(item.lon);
        const dist = calculateDistance(currentLat.value, currentLng.value, lat, lon);
        return {
          name: item.display_name.split(',')[0],
          type: item.type || getCategoryLabel(category),
          lat,
          lon,
          distance: dist
        };
      });

      pois.value = results.sort((a: any, b: any) => parseFloat(a.distance) - parseFloat(b.distance));
      renderPoiMarkers();
    }
  } catch (err) {
    console.error('POI fetch error:', err);
  } finally {
    loadingPois.value = false;
  }
};

const toggleCategory = (catId: string) => {
  activeCategory.value = catId;
  fetchPois(catId);
};

const clearPoiMarkers = () => {
  if (map) {
    poiMarkers.forEach((m) => m.remove());
    poiMarkers = [];
  }
};

const renderPoiMarkers = () => {
  if (!map) return;
  const iconEmoji = POI_CATEGORIES.find((c) => c.id === activeCategory.value)?.icon || '📍';

  pois.value.forEach((poi) => {
    const customHtmlIcon = L.divIcon({
      html: `<div class="bg-white border-2 border-indigo-600 rounded-full w-8 h-8 flex items-center justify-center text-sm shadow-md">${iconEmoji}</div>`,
      className: 'custom-poi-marker',
      iconSize: [32, 32],
      iconAnchor: [16, 16]
    });

    const marker = L.marker([poi.lat, poi.lon], { icon: customHtmlIcon }).addTo(map!);
    marker.bindPopup(`
      <div class="p-1 text-xs">
        <strong class="block font-bold text-slate-900">${poi.name}</strong>
        <span class="text-slate-500">${poi.type} • ${poi.distance} km</span>
      </div>
    `);
    poiMarkers.push(marker);
  });
};

const focusPoi = (poi: any) => {
  if (!map) return;
  map.setView([poi.lat, poi.lon], 15);
};

const initMap = async () => {
  if (!mapContainer.value) return;

  if (map) {
    map.remove();
    map = null;
  }

  await geocodeRental();

  map = L.map(mapContainer.value).setView([currentLat.value, currentLng.value], 14);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map);

  // Custom icon for rental house
  const houseIcon = L.divIcon({
    html: `<div class="bg-rose-600 text-white rounded-full p-2 shadow-lg border-2 border-white flex items-center justify-center font-bold text-xs">🏠</div>`,
    className: 'custom-house-marker',
    iconSize: [36, 36],
    iconAnchor: [18, 18]
  });

  mainMarker = L.marker([currentLat.value, currentLng.value], { icon: houseIcon }).addTo(map);
  mainMarker.bindPopup(`
    <div class="p-1.5 text-xs space-y-1">
      <strong class="font-bold text-indigo-700 block">${props.rental?.title}</strong>
      <span class="text-slate-700 font-semibold block">${props.rental?.monthlyPrice}€ / mese</span>
      <span class="text-slate-500 block">${props.rental?.city}</span>
    </div>
  `).openPopup();

  // Fetch initial POIs
  await fetchPois(activeCategory.value);
};

watch([() => props.isOpen, () => props.rental], async ([isOpenVal, rentalVal]) => {
  if (isOpenVal && rentalVal) {
    setTimeout(() => {
      initMap();
    }, 150);
  }
}, { immediate: true });

onUnmounted(() => {
  if (map) {
    map.remove();
    map = null;
  }
});
</script>

<style>
.custom-poi-marker, .custom-house-marker {
  background: transparent;
  border: none;
}
</style>
