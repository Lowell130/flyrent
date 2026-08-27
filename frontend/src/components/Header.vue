<template>
  <header class="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-sm w-full">
    
    <!-- LEVEL 1: Top Bar (Brand & User Profile) -->
    <div class="border-b border-slate-100 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2.5 flex items-center justify-between">
        
        <!-- Brand Logo & Subtitle -->
        <router-link to="/" class="flex items-center gap-3 group">
          <div class="bg-indigo-600 p-2 rounded-xl shadow-md shadow-indigo-600/20 text-white flex items-center justify-center group-hover:scale-105 transition">
            <Plane class="w-5 h-5 transform -rotate-45" />
          </div>
          <div class="flex items-center gap-2">
            <h1 class="text-lg font-black text-slate-900 tracking-tight">FlyRent</h1>
            <span class="bg-indigo-50 text-indigo-700 text-[11px] px-2.5 py-0.5 rounded-full font-bold border border-indigo-200 flex items-center gap-1">
              <GraduationCap class="w-3.5 h-3.5 text-indigo-600" /> Student & Worker Organizer
            </span>
          </div>
        </router-link>

        <!-- User Info & Account Actions -->
        <div>
          <!-- Logged In User State -->
          <div v-if="user || hasToken" class="flex items-center gap-3">
            <div v-if="user" class="flex items-center gap-2 bg-slate-50 border border-slate-200 px-3 py-1 rounded-xl">
              <div class="w-7 h-7 rounded-lg bg-indigo-100 text-indigo-700 font-bold text-xs flex items-center justify-center border border-indigo-200">
                {{ user.name ? user.name.charAt(0).toUpperCase() : 'U' }}
              </div>
              <div class="text-xs">
                <span class="font-bold text-slate-900 block leading-none">{{ user.name }}</span>
                <span class="text-[10px] text-slate-500 block leading-none mt-0.5 max-w-[130px] truncate">{{ user.email }}</span>
              </div>
            </div>

            <button
              @click="$emit('logout')"
              title="Disconnetti account"
              class="bg-rose-50 hover:bg-rose-100 text-rose-600 font-bold px-3 py-1.5 rounded-xl text-xs border border-rose-200 transition flex items-center gap-1.5"
            >
              <LogOut class="w-3.5 h-3.5" />
              <span>Esci</span>
            </button>
          </div>

          <!-- Guest State -->
          <div v-else>
            <router-link
              to="/login"
              class="bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-bold px-3.5 py-1.5 rounded-xl text-xs border border-indigo-200 transition flex items-center gap-1.5"
            >
              <LogIn class="w-4 h-4" />
              Accedi / Registrati
            </router-link>
          </div>
        </div>

      </div>
    </div>

    <!-- LEVEL 2: Controls Bar (Search, Filters, Views & New Action) -->
    <div class="bg-slate-50/50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2.5">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
          
          <!-- Left: Search Bar & City Selector -->
          <div class="flex flex-wrap items-center gap-2.5 flex-1 max-w-xl">
            <div class="relative flex-1 min-w-[200px]">
              <Search class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
              <input
                type="text"
                placeholder="Cerca per titolo, città, note..."
                :value="searchTerm"
                @input="$emit('update:searchTerm', ($event.target as HTMLInputElement).value)"
                class="w-full bg-white border border-slate-300 rounded-xl pl-9 pr-3 py-1.5 text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm"
              />
            </div>

            <select
              :value="selectedCity"
              @change="$emit('update:selectedCity', ($event.target as HTMLSelectElement).value)"
              class="bg-white border border-slate-300 rounded-xl px-3 py-1.5 text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm font-medium"
            >
              <option value="">Tutte le città</option>
              <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
            </select>
          </div>

          <!-- Right: View Switcher, Data Tools & Primary Add Button -->
          <div class="flex items-center gap-2 flex-wrap justify-end">
            
            <!-- View Switcher -->
            <div class="bg-slate-200/70 p-1 rounded-xl flex items-center gap-1 border border-slate-200">
              <button
                @click="$emit('update:viewMode', 'table')"
                :class="[
                  'flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-bold transition-all',
                  viewMode === 'table' ? 'bg-white text-indigo-700 shadow-sm' : 'text-slate-600 hover:text-slate-900'
                ]"
              >
                <Table class="w-3.5 h-3.5" />
                Tabella
              </button>
              <button
                @click="$emit('update:viewMode', 'kanban')"
                :class="[
                  'flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-bold transition-all',
                  viewMode === 'kanban' ? 'bg-white text-indigo-700 shadow-sm' : 'text-slate-600 hover:text-slate-900'
                ]"
              >
                <LayoutGrid class="w-3.5 h-3.5" />
                Kanban
              </button>
            </div>

            <!-- Export / Backup Button -->
            <button
              @click="$emit('exportData')"
              title="Esporta tutti gli annunci in file JSON"
              class="bg-white hover:bg-slate-100 text-slate-700 px-3 py-1.5 rounded-xl text-xs font-semibold border border-slate-300 transition flex items-center gap-1.5 shadow-sm"
            >
              <Download class="w-3.5 h-3.5 text-emerald-600" />
              <span class="hidden sm:inline">Esporta</span>
            </button>

            <!-- Seed Button -->
            <button
              @click="$emit('seedData')"
              title="Popola con annunci di prova"
              class="bg-white hover:bg-slate-100 text-slate-700 px-3 py-1.5 rounded-xl text-xs font-semibold border border-slate-300 transition flex items-center gap-1.5 shadow-sm"
            >
              <Database class="w-3.5 h-3.5 text-indigo-600" />
              <span>Dati Prova</span>
            </button>

            <!-- Primary Add Button -->
            <button
              @click="$emit('openAddModal')"
              class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-1.5 rounded-xl text-xs font-bold shadow-md shadow-indigo-600/20 flex items-center gap-1.5 transition"
            >
              <Plus class="w-4 h-4" />
              <span>Nuovo Annuncio</span>
            </button>

          </div>

        </div>
      </div>
    </div>

  </header>
</template>

<script setup lang="ts">
import { Plane, GraduationCap, Search, Table, LayoutGrid, Database, Plus, LogOut, LogIn, Download } from 'lucide-vue-next';

defineProps<{
  viewMode: 'kanban' | 'table';
  searchTerm: string;
  selectedCity: string;
  cities: string[];
  user: any;
  hasToken?: boolean;
}>();

defineEmits(['update:viewMode', 'update:searchTerm', 'update:selectedCity', 'openAddModal', 'seedData', 'exportData', 'logout']);
</script>
