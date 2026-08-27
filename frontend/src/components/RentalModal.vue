<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
    <div class="bg-white border border-slate-200 rounded-2xl w-full max-w-2xl shadow-2xl overflow-hidden my-8">
      
      <!-- Header -->
      <div class="px-6 py-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
        <h2 class="text-lg font-bold text-slate-900 flex items-center gap-2">
          <Building class="w-5 h-5 text-indigo-600" />
          {{ initialData ? 'Modifica Annuncio' : 'Nuovo Annuncio Affitto' }}
        </h2>
        <button @click="$emit('close')" class="text-slate-400 hover:text-slate-700 p-1 rounded-lg">
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleSubmit" class="p-6 space-y-6 max-h-[80vh] overflow-y-auto">
        
        <!-- Section 1: Informazioni Generali -->
        <div class="space-y-4">
          <h3 class="text-xs font-bold uppercase tracking-wider text-indigo-700 border-b border-slate-200 pb-1">
            1. Info Annuncio & Piattaforma
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="md:col-span-2">
              <label class="block text-xs font-semibold text-slate-700 mb-1">Titolo Annuncio *</label>
              <input
                type="text"
                required
                placeholder="es. Bilocale ristrutturato vista mare"
                v-model="formData.title"
                class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-sm text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Piattaforma</label>
              <select
                v-model="formData.platform"
                class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-sm text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option v-for="p in PLATFORMS" :key="p" :value="p">{{ p }}</option>
              </select>
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Link Annuncio (URL)</label>
              <div class="relative">
                <LinkIcon class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="url"
                  placeholder="https://..."
                  v-model="formData.url"
                  class="w-full bg-slate-50 border border-slate-300 rounded-xl pl-9 pr-3 py-2 text-sm text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Città / Località *</label>
              <input
                type="text"
                required
                placeholder="es. Termoli, Pescara, Vasto"
                v-model="formData.city"
                class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-sm text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Indirizzo / Zona</label>
              <input
                type="text"
                placeholder="es. Zona Stazione, Lungomare"
                v-model="formData.address"
                class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-sm text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </div>
        </div>

        <!-- Section: Gestione Foto -->
        <div class="space-y-4">
          <h3 class="text-xs font-bold uppercase tracking-wider text-purple-700 border-b border-slate-200 pb-1 flex items-center justify-between">
            <span class="flex items-center gap-1">
              <ImageIcon class="w-4 h-4" /> Foto Immobili (Facebook / Chat / Screenshot)
            </span>
            <span v-if="isCompressing" class="text-[11px] font-bold text-purple-600 flex items-center gap-1">
              <span class="w-3 h-3 border-2 border-purple-600 border-t-transparent rounded-full animate-spin"></span>
              Ottimizzazione foto in corso...
            </span>
          </h3>

          <div class="space-y-3">
            <div class="flex flex-col sm:flex-row gap-2">
              <div class="flex-1 flex gap-2">
                <input
                  type="url"
                  placeholder="Incolla URL Immagine (https://...)"
                  v-model="imageUrlInput"
                  class="flex-1 bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-sm text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
                <button
                  type="button"
                  @click="handleAddImageUrl"
                  class="bg-purple-50 hover:bg-purple-100 text-purple-700 font-semibold px-3 py-2 rounded-xl text-xs border border-purple-200 transition flex items-center gap-1"
                >
                  <Plus class="w-4 h-4" /> Aggiungi Link
                </button>
              </div>

              <label class="cursor-pointer bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold px-3 py-2 rounded-xl text-xs border border-slate-300 transition flex items-center justify-center gap-1.5 shrink-0">
                <Upload class="w-4 h-4 text-purple-600" />
                Carica File / Foto
                <input
                  type="file"
                  accept="image/*"
                  multiple
                  @change="handleFileUpload"
                  class="hidden"
                />
              </label>
            </div>

            <!-- Photos Preview Gallery -->
            <div v-if="formData.images && formData.images.length > 0" class="grid grid-cols-4 sm:grid-cols-6 gap-2 pt-2">
              <div v-for="(img, idx) in formData.images" :key="idx" class="relative group aspect-square rounded-xl overflow-hidden border border-slate-200 bg-slate-100">
                <img :src="img" :alt="`Preview ${idx}`" class="w-full h-full object-cover" />
                <button
                  type="button"
                  @click="handleRemoveImage(idx)"
                  class="absolute top-1 right-1 bg-rose-600 hover:bg-rose-700 text-white p-1 rounded-full shadow-md transition"
                  title="Rimuovi foto"
                >
                  <Trash2 class="w-3 h-3" />
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Section 2: Condizioni Economiche -->
        <div class="space-y-4">
          <h3 class="text-xs font-bold uppercase tracking-wider text-emerald-700 border-b border-slate-200 pb-1 flex items-center gap-1">
            <Euro class="w-4 h-4" /> 2. Economia, Utenze e Condominio
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Prezzo Mensile (€) *</label>
              <input
                type="number"
                required
                min="0"
                v-model.number="formData.monthlyPrice"
                class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-sm text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Utenze</label>
              <select
                v-model="formData.utilities"
                class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-sm text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
              >
                <option v-for="u in UTILITIES_TYPES" :key="u" :value="u">{{ u }}</option>
              </select>
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Stima Utenze (€/mese)</label>
              <input
                type="number"
                min="0"
                :disabled="formData.utilities === 'Incluse'"
                v-model.number="formData.utilitiesPriceEstimate"
                class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-sm text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500 disabled:opacity-40"
              />
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Spese Condominio</label>
              <select
                v-model="formData.condoFees"
                class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-sm text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
              >
                <option v-for="c in CONDO_TYPES" :key="c" :value="c">{{ c }}</option>
              </select>
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Costo Condominio (€/mese)</label>
              <input
                type="number"
                min="0"
                :disabled="formData.condoFees === 'Incluse'"
                v-model.number="formData.condoFeesPriceEstimate"
                class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-sm text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500 disabled:opacity-40"
              />
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Caparra / Cauzione (€)</label>
              <input
                type="number"
                min="0"
                v-model.number="formData.deposit"
                class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-sm text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            <div class="md:col-span-3">
              <label class="block text-xs font-semibold text-slate-700 mb-1">Periodo Disponibilità / Durata Contratto</label>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                <select
                  v-model="selectedPeriodPreset"
                  @change="handlePeriodPresetChange"
                  class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-sm text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500 font-medium"
                >
                  <option value="">-- Seleziona Mesi / Durata --</option>
                  <option v-for="m in 36" :key="m" :value="getPresetLabel(m)">
                    {{ m }} {{ m === 1 ? 'Mese' : 'Mesi' }}
                    <template v-if="m === 3"> (Trimestre)</template>
                    <template v-else-if="m === 6"> (Semestre)</template>
                    <template v-else-if="m === 10"> (Anno Accademico)</template>
                    <template v-else-if="m === 12"> (1 Anno)</template>
                    <template v-else-if="m === 24"> (2 Anni)</template>
                    <template v-else-if="m === 36"> (3 Anni)</template>
                  </option>
                  <option value="Flessibile / Personalizzato">Flessibile / Personalizzato</option>
                </select>

                <input
                  type="text"
                  placeholder="es. 6 Mesi (Ottobre - Marzo) o specificare date"
                  v-model="formData.availablePeriod"
                  class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-sm text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Section 3: Smart Working & Servizi -->
        <div class="space-y-4">
          <h3 class="text-xs font-bold uppercase tracking-wider text-cyan-700 border-b border-slate-200 pb-1 flex items-center gap-1">
            <Wifi class="w-4 h-4" /> 3. Smart Working & Parcheggio / Auto
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Connessione Internet</label>
              <select
                v-model="formData.wifiType"
                class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-sm text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
              >
                <option v-for="w in WIFI_TYPES" :key="w" :value="w">{{ w }}</option>
              </select>
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Postazione Lavoro</label>
              <select
                v-model="formData.workspaceType"
                class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-sm text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
              >
                <option v-for="ws in WORKSPACE_TYPES" :key="ws" :value="ws">{{ ws }}</option>
              </select>
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Posto Auto / Garage *</label>
              <select
                v-model="formData.parkingType"
                class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-sm text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
              >
                <option v-for="pk in PARKING_TYPES" :key="pk" :value="pk">{{ pk }}</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Section 4: Scoreboard Gradimento Zona con Barre Colorate -->
        <div class="space-y-4">
          <h3 class="text-xs font-bold uppercase tracking-wider text-indigo-700 border-b border-slate-200 pb-1 flex items-center gap-1">
            <BarChart2 class="w-4 h-4 text-indigo-600" /> 4. Gradimento Zona (Barre Colorate 1-5)
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 bg-slate-50 p-4 rounded-2xl border border-slate-200">
            
            <!-- Rating 1: Quartiere -->
            <div class="space-y-1.5">
              <div class="flex justify-between items-center text-xs font-semibold text-slate-800">
                <span>🏡 Quartiere / Zona</span>
                <span :class="['px-2 py-0.5 rounded-full font-bold text-[11px] text-white', getBarColor(formData.ratingNeighborhood)]">
                  {{ formData.ratingNeighborhood }}/5
                </span>
              </div>
              <div class="grid grid-cols-5 gap-1 bg-white p-1 rounded-xl border border-slate-200">
                <button
                  type="button"
                  v-for="step in 5"
                  :key="step"
                  @click="formData.ratingNeighborhood = step"
                  :class="[
                    'h-6 rounded-lg transition-all font-bold text-[10px] flex items-center justify-center',
                    step <= formData.ratingNeighborhood ? `${getBarColor(formData.ratingNeighborhood)} text-white` : 'bg-slate-100 text-slate-400 hover:bg-slate-200'
                  ]"
                >
                  {{ step }}
                </button>
              </div>
            </div>

            <!-- Rating 2: Servizi & Supermercati -->
            <div class="space-y-1.5">
              <div class="flex justify-between items-center text-xs font-semibold text-slate-800">
                <span>🛒 Servizi & Supermercati</span>
                <span :class="['px-2 py-0.5 rounded-full font-bold text-[11px] text-white', getBarColor(formData.ratingServices)]">
                  {{ formData.ratingServices }}/5
                </span>
              </div>
              <div class="grid grid-cols-5 gap-1 bg-white p-1 rounded-xl border border-slate-200">
                <button
                  type="button"
                  v-for="step in 5"
                  :key="step"
                  @click="formData.ratingServices = step"
                  :class="[
                    'h-6 rounded-lg transition-all font-bold text-[10px] flex items-center justify-center',
                    step <= formData.ratingServices ? `${getBarColor(formData.ratingServices)} text-white` : 'bg-slate-100 text-slate-400 hover:bg-slate-200'
                  ]"
                >
                  {{ step }}
                </button>
              </div>
            </div>

            <!-- Rating 3: Stazione & Aeroporto -->
            <div class="space-y-1.5">
              <div class="flex justify-between items-center text-xs font-semibold text-slate-800">
                <span>🚉 Stazione / Trasporti</span>
                <span :class="['px-2 py-0.5 rounded-full font-bold text-[11px] text-white', getBarColor(formData.ratingTransport)]">
                  {{ formData.ratingTransport }}/5
                </span>
              </div>
              <div class="grid grid-cols-5 gap-1 bg-white p-1 rounded-xl border border-slate-200">
                <button
                  type="button"
                  v-for="step in 5"
                  :key="step"
                  @click="formData.ratingTransport = step"
                  :class="[
                    'h-6 rounded-lg transition-all font-bold text-[10px] flex items-center justify-center',
                    step <= formData.ratingTransport ? `${getBarColor(formData.ratingTransport)} text-white` : 'bg-slate-100 text-slate-400 hover:bg-slate-200'
                  ]"
                >
                  {{ step }}
                </button>
              </div>
            </div>

          </div>
        </div>

        <!-- Section 5: Stato Trattativa & Contatto -->
        <div class="space-y-4">
          <h3 class="text-xs font-bold uppercase tracking-wider text-rose-700 border-b border-slate-200 pb-1 flex items-center gap-1">
            <User class="w-4 h-4" /> 5. Trattativa & Contatto
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Stato Trattativa</label>
              <select
                v-model="formData.status"
                class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-sm text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-rose-500"
              >
                <option v-for="s in STATUSES" :key="s" :value="s">{{ s }}</option>
              </select>
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Nome Referente</label>
              <input
                type="text"
                placeholder="es. Mario (Proprietario)"
                v-model="formData.contactName"
                class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-sm text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-rose-500"
              />
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Telefono / WhatsApp</label>
              <input
                type="text"
                placeholder="+39 333 1234567"
                v-model="formData.contactPhone"
                class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-sm text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-rose-500"
              />
            </div>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Note Libere</label>
            <textarea
              rows="3"
              placeholder="es. Inviato messaggio WhatsApp. Proprietario disponibile a trattare il prezzo..."
              v-model="formData.notes"
              class="w-full bg-slate-50 border border-slate-300 rounded-xl p-3 text-sm text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-rose-500"
            ></textarea>
          </div>
        </div>

        <!-- Footer buttons -->
        <div class="pt-4 border-t border-slate-200 flex items-center justify-end gap-3">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2 rounded-xl text-sm font-semibold text-slate-600 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 transition"
          >
            Annulla
          </button>
          <button
            type="submit"
            :disabled="isCompressing"
            class="px-5 py-2 rounded-xl text-sm font-bold text-white bg-indigo-600 hover:bg-indigo-700 shadow-md shadow-indigo-600/20 transition disabled:opacity-50"
          >
            {{ initialData ? 'Salva Modifiche' : 'Crea Annuncio' }}
          </button>
        </div>

      </form>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue';
import { X, Building, Euro, Wifi, Laptop, User, Link as LinkIcon, Image as ImageIcon, Upload, Plus, Trash2, BarChart2 } from 'lucide-vue-next';
import { Rental, Platform, UtilitiesType, CondoFeesType, StatusType, WifiType, WorkspaceType, ParkingType } from '../types/rental';

const props = defineProps<{
  isOpen: boolean;
  initialData?: Rental | null;
}>();

const emit = defineEmits(['close', 'submit']);

const PLATFORMS: Platform[] = ['Facebook', 'Subito', 'Idealista', 'Immobiliare', 'Privato', 'Altro'];
const UTILITIES_TYPES: UtilitiesType[] = ['Incluse', 'Forfait', 'A consumo'];
const CONDO_TYPES: CondoFeesType[] = ['Incluse', 'Escluse', 'Forfait'];
const STATUSES: StatusType[] = ['Bozza', 'Contattato', 'In Attesa', 'Visita/Videochiamata', 'Opzionato', 'Scartato', 'Confermato'];
const WIFI_TYPES: WifiType[] = ['Fibra FTTH', 'FTTC', 'FWA', 'Wi-Fi da verificare', 'Assente'];
const WORKSPACE_TYPES: WorkspaceType[] = ['Scrivania dedicata', 'Tavolo grande', 'Nessuna'];
const PARKING_TYPES: ParkingType[] = ['Posto auto riservato', 'Box / Garage privato', 'Parcheggio libero in strada', 'Parcheggio a pagamento', 'Nessun parcheggio'];

const imageUrlInput = ref('');
const isCompressing = ref(false);
const selectedPeriodPreset = ref('');

const getPresetLabel = (m: number) => {
  let label = `${m} ${m === 1 ? 'Mese' : 'Mesi'}`;
  if (m === 3) label += ' (Trimestre)';
  else if (m === 6) label += ' (Semestre)';
  else if (m === 10) label += ' (Anno Accademico)';
  else if (m === 12) label += ' (1 Anno)';
  else if (m === 24) label += ' (2 Anni)';
  else if (m === 36) label += ' (3 Anni)';
  return label;
};

const handlePeriodPresetChange = () => {
  if (selectedPeriodPreset.value && selectedPeriodPreset.value !== 'Flessibile / Personalizzato') {
    formData.availablePeriod = selectedPeriodPreset.value;
  }
};

const getBarColor = (score: number) => {
  if (score <= 2) return 'bg-rose-500';
  if (score === 3) return 'bg-amber-500';
  if (score === 4) return 'bg-emerald-500';
  return 'bg-indigo-600';
};

const formData = reactive<any>({
  title: '',
  url: '',
  platform: 'Facebook',
  city: 'Termoli',
  address: '',
  monthlyPrice: 500,
  utilities: 'A consumo',
  utilitiesPriceEstimate: 50,
  condoFees: 'Escluse',
  condoFeesPriceEstimate: 0,
  deposit: 500,
  status: 'Bozza',
  wifiType: 'Wi-Fi da verificare',
  workspaceType: 'Tavolo grande',
  parkingType: 'Parcheggio libero in strada',
  ratingNeighborhood: 3,
  ratingServices: 3,
  ratingTransport: 3,
  availablePeriod: '6 Mesi (Semestre)',
  contactName: '',
  contactPhone: '',
  notes: '',
  images: []
});

watch([() => props.isOpen, () => props.initialData], ([isOpenVal, initialDataVal]) => {
  if (!isOpenVal) return;
  imageUrlInput.value = '';

  if (initialDataVal) {
    Object.assign(formData, {
      title: initialDataVal.title || '',
      url: initialDataVal.url || '',
      platform: initialDataVal.platform || 'Facebook',
      city: initialDataVal.city || '',
      address: initialDataVal.address || '',
      monthlyPrice: initialDataVal.monthlyPrice || 0,
      utilities: initialDataVal.utilities || 'A consumo',
      utilitiesPriceEstimate: initialDataVal.utilitiesPriceEstimate || 0,
      condoFees: initialDataVal.condoFees || 'Escluse',
      condoFeesPriceEstimate: initialDataVal.condoFeesPriceEstimate || 0,
      deposit: initialDataVal.deposit || 0,
      status: initialDataVal.status || 'Bozza',
      wifiType: initialDataVal.wifiType || 'Wi-Fi da verificare',
      workspaceType: initialDataVal.workspaceType || 'Tavolo grande',
      parkingType: initialDataVal.parkingType || 'Parcheggio libero in strada',
      ratingNeighborhood: initialDataVal.ratingNeighborhood ?? 3,
      ratingServices: initialDataVal.ratingServices ?? 3,
      ratingTransport: initialDataVal.ratingTransport ?? 3,
      availablePeriod: initialDataVal.availablePeriod || '6 Mesi (Semestre)',
      contactName: initialDataVal.contactName || '',
      contactPhone: initialDataVal.contactPhone || '',
      notes: initialDataVal.notes || '',
      images: initialDataVal.images ? [...initialDataVal.images] : []
    });
  } else {
    Object.assign(formData, {
      title: '',
      url: '',
      platform: 'Facebook',
      city: 'Termoli',
      address: '',
      monthlyPrice: 500,
      utilities: 'A consumo',
      utilitiesPriceEstimate: 50,
      condoFees: 'Escluse',
      condoFeesPriceEstimate: 0,
      deposit: 500,
      status: 'Bozza',
      wifiType: 'Wi-Fi da verificare',
      workspaceType: 'Tavolo grande',
      parkingType: 'Parcheggio libero in strada',
      ratingNeighborhood: 3,
      ratingServices: 3,
      ratingTransport: 3,
      availablePeriod: '6 Mesi (Semestre)',
      contactName: '',
      contactPhone: '',
      notes: '',
      images: []
    });
  }
  selectedPeriodPreset.value = formData.availablePeriod || '';
}, { immediate: true, deep: true });

const handleAddImageUrl = () => {
  if (!imageUrlInput.value.trim()) return;
  if (!formData.images) formData.images = [];
  formData.images.push(imageUrlInput.value.trim());
  imageUrlInput.value = '';
};

// Client-side Canvas Image Compression (~90% size reduction per photo)
const compressImage = (file: File, maxWidth = 1200, maxHeight = 1200, quality = 0.8): Promise<string> => {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const img = new Image();
      img.onload = () => {
        const canvas = document.createElement('canvas');
        let width = img.width;
        let height = img.height;

        if (width > height) {
          if (width > maxWidth) {
            height = Math.round((height * maxWidth) / width);
            width = maxWidth;
          }
        } else {
          if (height > maxHeight) {
            width = Math.round((width * maxHeight) / height);
            height = maxHeight;
          }
        }

        canvas.width = width;
        canvas.height = height;

        const ctx = canvas.getContext('2d');
        if (ctx) {
          ctx.drawImage(img, 0, 0, width, height);
          resolve(canvas.toDataURL('image/jpeg', quality));
        } else {
          resolve(e.target?.result as string);
        }
      };
      img.src = e.target?.result as string;
    };
    reader.readAsDataURL(file);
  });
};

const handleFileUpload = async (e: Event) => {
  const files = (e.target as HTMLInputElement).files;
  if (!files || files.length === 0) return;

  isCompressing.value = true;
  try {
    for (const file of Array.from(files)) {
      const compressed = await compressImage(file);
      if (!formData.images) formData.images = [];
      formData.images.push(compressed);
    }
  } catch (err) {
    console.error('Image compression error:', err);
  } finally {
    isCompressing.value = false;
  }
};

const handleRemoveImage = (index: number) => {
  if (formData.images) {
    formData.images.splice(index, 1);
  }
};

const handleSubmit = () => {
  emit('submit', { ...formData });
};
</script>
