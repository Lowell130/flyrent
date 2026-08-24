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
          <h3 class="text-xs font-bold uppercase tracking-wider text-purple-700 border-b border-slate-200 pb-1 flex items-center gap-1">
            <ImageIcon class="w-4 h-4" /> Foto Immobili (Facebook / Chat / Screenshot)
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
              <label class="block text-xs font-semibold text-slate-700 mb-1">Periodo Disponibilità</label>
              <input
                type="text"
                placeholder="es. 1 Ottobre - 30 Novembre (2 mesi)"
                v-model="formData.availablePeriod"
                class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-sm text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>
          </div>
        </div>

        <!-- Section 3: Smart Working & Servizi (Wi-Fi, Postazione & Parcheggio) -->
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

        <!-- Section 4: Scoreboard Gradimento Zona & Servizi (Voti 1-5 ⭐) -->
        <div class="space-y-4">
          <h3 class="text-xs font-bold uppercase tracking-wider text-amber-700 border-b border-slate-200 pb-1 flex items-center gap-1">
            <Star class="w-4 h-4 text-amber-500" /> 4. Scoreboard Gradimento Zona & Servizi (Voti 1-5 ⭐)
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 bg-amber-50/50 p-3 rounded-2xl border border-amber-200/80">
            <!-- Rating 1: Quartiere -->
            <div>
              <label class="block text-xs font-semibold text-slate-800 mb-1 flex items-center justify-between">
                <span>🏡 Quartiere / Zona</span>
                <span class="font-bold text-amber-600">{{ formData.ratingNeighborhood }} / 5 ⭐</span>
              </label>
              <div class="flex items-center gap-1 bg-white p-1.5 rounded-xl border border-amber-200 justify-between">
                <button
                  type="button"
                  v-for="star in 5"
                  :key="star"
                  @click="formData.ratingNeighborhood = star"
                  :class="['p-1 rounded-lg transition', star <= formData.ratingNeighborhood ? 'text-amber-500' : 'text-slate-300']"
                >
                  <Star class="w-4 h-4 fill-current" />
                </button>
              </div>
            </div>

            <!-- Rating 2: Servizi & Supermercati -->
            <div>
              <label class="block text-xs font-semibold text-slate-800 mb-1 flex items-center justify-between">
                <span>🛒 Servizi & Supermercati</span>
                <span class="font-bold text-amber-600">{{ formData.ratingServices }} / 5 ⭐</span>
              </label>
              <div class="flex items-center gap-1 bg-white p-1.5 rounded-xl border border-amber-200 justify-between">
                <button
                  type="button"
                  v-for="star in 5"
                  :key="star"
                  @click="formData.ratingServices = star"
                  :class="['p-1 rounded-lg transition', star <= formData.ratingServices ? 'text-amber-500' : 'text-slate-300']"
                >
                  <Star class="w-4 h-4 fill-current" />
                </button>
              </div>
            </div>

            <!-- Rating 3: Stazione & Aeroporto -->
            <div>
              <label class="block text-xs font-semibold text-slate-800 mb-1 flex items-center justify-between">
                <span>🚉 Stazione / Aeroporto</span>
                <span class="font-bold text-amber-600">{{ formData.ratingTransport }} / 5 ⭐</span>
              </label>
              <div class="flex items-center gap-1 bg-white p-1.5 rounded-xl border border-amber-200 justify-between">
                <button
                  type="button"
                  v-for="star in 5"
                  :key="star"
                  @click="formData.ratingTransport = star"
                  :class="['p-1 rounded-lg transition', star <= formData.ratingTransport ? 'text-amber-500' : 'text-slate-300']"
                >
                  <Star class="w-4 h-4 fill-current" />
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
            class="px-5 py-2 rounded-xl text-sm font-bold text-white bg-indigo-600 hover:bg-indigo-700 shadow-md shadow-indigo-600/20 transition"
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
import { X, Building, Euro, Wifi, Laptop, User, Link as LinkIcon, Image as ImageIcon, Upload, Plus, Trash2, Star } from 'lucide-vue-next';
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
  availablePeriod: '2 Mesi',
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
      availablePeriod: initialDataVal.availablePeriod || '',
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
      availablePeriod: '2 Mesi',
      contactName: '',
      contactPhone: '',
      notes: '',
      images: []
    });
  }
}, { immediate: true, deep: true });

const handleAddImageUrl = () => {
  if (!imageUrlInput.value.trim()) return;
  if (!formData.images) formData.images = [];
  formData.images.push(imageUrlInput.value.trim());
  imageUrlInput.value = '';
};

const handleFileUpload = (e: Event) => {
  const files = (e.target as HTMLInputElement).files;
  if (!files || files.length === 0) return;

  Array.from(files).forEach((file) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      if (typeof reader.result === 'string') {
        if (!formData.images) formData.images = [];
        formData.images.push(reader.result);
      }
    };
    reader.readAsDataURL(file);
  });
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
