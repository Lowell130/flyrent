<template>
  <div class="min-h-screen bg-slate-50 text-slate-800 flex flex-col font-sans w-full">
    
    <!-- Header -->
    <Header
      v-model:viewMode="viewMode"
      v-model:searchTerm="searchTerm"
      v-model:selectedCity="selectedCity"
      :cities="cities"
      :user="user"
      :hasToken="hasToken"
      @openAddModal="openAddModal"
      @seedData="handleSeedData"
      @exportData="handleExportData"
      @logout="handleLogout"
    />

    <!-- Main Content -->
    <main class="flex-1 w-full px-4 sm:px-6 lg:px-8 py-6">
      
      <!-- KPI Stats Banner -->
      <div v-if="!loading && rentals.length > 0" class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        
        <!-- KPI 1: Totale Annunci -->
        <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm flex items-center gap-3">
          <div class="w-10 h-10 bg-indigo-50 text-indigo-600 rounded-xl flex items-center justify-center border border-indigo-100 shrink-0">
            <Building class="w-5 h-5" />
          </div>
          <div>
            <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400 block">Totale Annunci</span>
            <span class="text-lg font-black text-slate-900">{{ kpiStats.totalCount }}</span>
          </div>
        </div>

        <!-- KPI 2: Canone Medio -->
        <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm flex items-center gap-3">
          <div class="w-10 h-10 bg-emerald-50 text-emerald-600 rounded-xl flex items-center justify-center border border-emerald-100 shrink-0">
            <Euro class="w-5 h-5" />
          </div>
          <div>
            <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400 block">Canone Medio</span>
            <span class="text-lg font-black text-slate-900">{{ kpiStats.avgPrice }}€ <span class="text-xs font-semibold text-slate-400">/mese</span></span>
          </div>
        </div>

        <!-- KPI 3: Fibra FTTH -->
        <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm flex items-center gap-3">
          <div class="w-10 h-10 bg-cyan-50 text-cyan-600 rounded-xl flex items-center justify-center border border-cyan-100 shrink-0">
            <Wifi class="w-5 h-5" />
          </div>
          <div>
            <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400 block">Copertura Fibra</span>
            <span class="text-lg font-black text-slate-900">{{ kpiStats.fibraCount }} <span class="text-xs font-semibold text-slate-400">/ {{ kpiStats.totalCount }}</span></span>
          </div>
        </div>

        <!-- KPI 4: Trattative In Corso -->
        <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm flex items-center gap-3">
          <div class="w-10 h-10 bg-amber-50 text-amber-600 rounded-xl flex items-center justify-center border border-amber-100 shrink-0">
            <Sparkles class="w-5 h-5" />
          </div>
          <div>
            <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400 block">Trattative Attive</span>
            <span class="text-lg font-black text-slate-900">{{ kpiStats.activeDeals }}</span>
          </div>
        </div>

      </div>

      <!-- Quick Toggles Filter Bar -->
      <div v-if="!loading && rentals.length > 0" class="bg-white border border-slate-200 rounded-2xl p-3 mb-4 shadow-sm flex flex-wrap items-center justify-between gap-3 text-xs">
        
        <div class="flex items-center gap-2 flex-wrap">
          <span class="font-bold text-slate-500 flex items-center gap-1">
            <Filter class="w-3.5 h-3.5 text-indigo-600" /> Filtri Rapidi:
          </span>

          <button
            @click="onlyFibra = !onlyFibra"
            :class="[
              'px-3 py-1.5 rounded-xl font-bold border transition flex items-center gap-1.5',
              onlyFibra ? 'bg-cyan-600 text-white border-cyan-600 shadow-sm' : 'bg-slate-50 hover:bg-slate-100 text-slate-700 border-slate-200'
            ]"
          >
            <Wifi class="w-3.5 h-3.5" />
            Solo Fibra FTTH
          </button>

          <button
            @click="onlyWorkspace = !onlyWorkspace"
            :class="[
              'px-3 py-1.5 rounded-xl font-bold border transition flex items-center gap-1.5',
              onlyWorkspace ? 'bg-indigo-600 text-white border-indigo-600 shadow-sm' : 'bg-slate-50 hover:bg-slate-100 text-slate-700 border-slate-200'
            ]"
          >
            <Laptop class="w-3.5 h-3.5" />
            Solo con Scrivania
          </button>

          <button
            @click="onlyParking = !onlyParking"
            :class="[
              'px-3 py-1.5 rounded-xl font-bold border transition flex items-center gap-1.5',
              onlyParking ? 'bg-amber-600 text-white border-amber-600 shadow-sm' : 'bg-slate-50 hover:bg-slate-100 text-slate-700 border-slate-200'
            ]"
          >
            <Car class="w-3.5 h-3.5" />
            Solo Posto Auto / Box
          </button>
        </div>

        <div class="flex items-center gap-2">
          <span class="text-slate-500 font-semibold">Budget max:</span>
          <select
            v-model.number="maxPriceFilter"
            class="bg-slate-50 border border-slate-300 rounded-xl px-2.5 py-1 font-bold text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option :value="0">Tutti i prezzi</option>
            <option :value="500">Fino a 500€</option>
            <option :value="600">Fino a 600€</option>
            <option :value="750">Fino a 750€</option>
            <option :value="1000">Fino a 1000€</option>
          </select>
        </div>

      </div>

      <!-- Loading Spinner -->
      <div v-if="loading" class="flex items-center justify-center py-20 text-slate-500 gap-2">
        <div class="w-5 h-5 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
        <span>Caricamento annunci in corso...</span>
      </div>

      <!-- Error Alert -->
      <div v-if="error" class="bg-rose-50 border border-rose-200 text-rose-700 p-4 rounded-xl text-sm mb-6">
        {{ error }}
      </div>

      <!-- Empty State -->
      <div v-if="!loading && !error && filteredRentals.length === 0" class="text-center py-20 bg-white border border-slate-200 rounded-2xl p-8 max-w-md mx-auto my-10 shadow-sm">
        <div class="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-4 border border-indigo-100">
          <Building class="w-6 h-6" />
        </div>
        <h3 class="text-lg font-bold text-slate-900 mb-2">Nessun annuncio trovato</h3>
        <p class="text-sm text-slate-500 mb-6">
          Prova a disattivare i filtri o inserisci nuovi annunci di affitto per la tua ricerca!
        </p>
        <div class="flex justify-center gap-3">
          <button
            @click="handleSeedData"
            class="bg-slate-100 hover:bg-slate-200 text-slate-700 px-4 py-2 rounded-xl text-xs font-semibold border border-slate-300 transition flex items-center gap-1.5"
          >
            <Sparkles class="w-4 h-4 text-amber-500" /> Popola con Dati Prova
          </button>
          <button
            @click="openAddModal"
            class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-xl text-xs font-bold shadow-md shadow-indigo-600/20 transition"
          >
            Aggiungi Annuncio
          </button>
        </div>
      </div>

      <!-- Views -->
      <template v-if="!loading && !error && filteredRentals.length > 0">
        <TableView
          v-if="viewMode === 'table'"
          :rentals="filteredRentals"
          @statusChange="handleStatusChange"
          @edit="openEditModal"
          @delete="handleDelete"
          @openQuickMessage="openQuickMessage"
        />
        <KanbanView
          v-else
          :rentals="filteredRentals"
          @statusChange="handleStatusChange"
          @edit="openEditModal"
          @delete="handleDelete"
          @openQuickMessage="openQuickMessage"
        />
      </template>

    </main>

    <!-- Modals -->
    <RentalModal
      :isOpen="isRentalModalOpen"
      :initialData="editingRental"
      @close="isRentalModalOpen = false"
      @submit="handleCreateOrUpdate"
    />

    <QuickMessageModal
      :rental="quickMessageRental"
      @close="quickMessageRental = null"
    />

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import Header from '../components/Header.vue';
import TableView from '../components/TableView.vue';
import KanbanView from '../components/KanbanView.vue';
import RentalModal from '../components/RentalModal.vue';
import QuickMessageModal from '../components/QuickMessageModal.vue';
import { Rental, StatusType } from '../types/rental';
import { api } from '../services/api';
import { Building, Sparkles, Euro, Wifi, Laptop, Filter, Car } from 'lucide-vue-next';

const router = useRouter();

const rentals = ref<Rental[]>([]);
const viewMode = ref<'kanban' | 'table'>('table');
const searchTerm = ref('');
const selectedCity = ref('');
const loading = ref(true);
const error = ref<string | null>(null);
const user = ref<any>(null);

// Quick Filter states
const onlyFibra = ref(false);
const onlyWorkspace = ref(false);
const onlyParking = ref(false);
const maxPriceFilter = ref(0);

const hasToken = computed(() => !!localStorage.getItem('token'));

// Modals state
const isRentalModalOpen = ref(false);
const editingRental = ref<Rental | null>(null);
const quickMessageRental = ref<Rental | null>(null);

const fetchUser = async () => {
  const storedUser = localStorage.getItem('user');
  if (storedUser) {
    try {
      user.value = JSON.parse(storedUser);
    } catch (e) {}
  }
  const token = localStorage.getItem('token');
  if (token) {
    try {
      const me = await api.getMe();
      user.value = me;
      localStorage.setItem('user', JSON.stringify(me));
    } catch (err) {
      console.error('Failed to get me profile:', err);
    }
  }
};

const fetchRentals = async () => {
  try {
    loading.value = true;
    error.value = null;
    rentals.value = await api.getRentals({
      search: searchTerm.value,
      city: selectedCity.value
    });
  } catch (err: any) {
    console.error('Error fetching rentals:', err);
    error.value = 'Impossibile caricare gli annunci dal backend.';
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await fetchUser();
  await fetchRentals();
});

watch([searchTerm, selectedCity], () => {
  fetchRentals();
});

const cities = computed(() => {
  return Array.from(new Set(rentals.value.map((r) => r.city))).filter(Boolean);
});

// KPI Calculations
const kpiStats = computed(() => {
  const totalCount = rentals.value.length;
  if (totalCount === 0) return { totalCount: 0, avgPrice: 0, fibraCount: 0, activeDeals: 0 };

  const totalPrice = rentals.value.reduce((acc, r) => acc + (r.monthlyPrice || 0), 0);
  const avgPrice = Math.round(totalPrice / totalCount);

  const fibraCount = rentals.value.filter((r) => r.wifiType?.includes('Fibra')).length;
  const activeDeals = rentals.value.filter((r) => ['Contattato', 'In Attesa', 'Visita/Videochiamata', 'Opzionato'].includes(r.status)).length;

  return { totalCount, avgPrice, fibraCount, activeDeals };
});

// Client-side quick filtering
const filteredRentals = computed(() => {
  return rentals.value.filter((r) => {
    if (onlyFibra.value && !r.wifiType?.includes('Fibra')) return false;
    if (onlyWorkspace.value && (!r.workspaceType || r.workspaceType.includes('Nessuna'))) return false;
    if (onlyParking.value && (!r.parkingType || r.parkingType.includes('Nessun') || r.parkingType.includes('pagamento'))) return false;
    if (maxPriceFilter.value > 0 && r.monthlyPrice > maxPriceFilter.value) return false;
    return true;
  });
});

const handleStatusChange = async (id: string, newStatus: StatusType) => {
  const item = rentals.value.find((r) => r._id === id);
  if (item) item.status = newStatus;

  try {
    await api.updateRental(id, { status: newStatus });
  } catch (err) {
    console.error('Failed to update status:', err);
    fetchRentals();
  }
};

const openAddModal = () => {
  editingRental.value = null;
  isRentalModalOpen.value = true;
};

const openEditModal = (rental: Rental) => {
  editingRental.value = rental;
  isRentalModalOpen.value = true;
};

const openQuickMessage = (rental: Rental) => {
  quickMessageRental.value = rental;
};

const handleCreateOrUpdate = async (formData: any) => {
  try {
    if (editingRental.value) {
      await api.updateRental(editingRental.value._id, formData);
    } else {
      await api.createRental(formData);
    }
    isRentalModalOpen.value = false;
    editingRental.value = null;
    fetchRentals();
  } catch (err) {
    console.error('Failed to save rental:', err);
    alert('Errore nel salvataggio dell\'annuncio.');
  }
};

const handleDelete = async (id: string) => {
  if (!window.confirm('Sei sicuro di voler eliminare questo annuncio?')) return;
  try {
    await api.deleteRental(id);
    fetchRentals();
  } catch (err) {
    console.error('Failed to delete rental:', err);
    alert('Errore nell\'eliminazione.');
  }
};

const handleSeedData = async () => {
  try {
    await api.seedData();
    fetchRentals();
  } catch (err) {
    console.error('Failed to seed data:', err);
    alert('Errore nel caricamento dei dati di prova.');
  }
};

const handleExportData = () => {
  const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(rentals.value, null, 2));
  const downloadAnchor = document.createElement('a');
  downloadAnchor.setAttribute('href', dataStr);
  downloadAnchor.setAttribute('download', `flyrent_annunci_backup_${new Date().toISOString().slice(0, 10)}.json`);
  document.body.appendChild(downloadAnchor);
  downloadAnchor.click();
  downloadAnchor.remove();
};

const handleLogout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  user.value = null;
  router.push('/login?force=true');
};
</script>
