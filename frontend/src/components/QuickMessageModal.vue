<template>
  <div v-if="rental" class="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-white border border-slate-200 rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden animate-in fade-in zoom-in duration-150">
      
      <!-- Header -->
      <div class="px-6 py-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
        <div class="flex items-center gap-2 text-indigo-600">
          <MessageSquare class="w-5 h-5" />
          <h3 class="font-bold text-slate-900">Generatore Messaggio di Contatto</h3>
        </div>
        <button @click="$emit('close')" class="text-slate-400 hover:text-slate-700 p-1 rounded-lg">
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Content -->
      <div class="p-6 space-y-4">
        <div class="grid grid-cols-2 gap-3 text-xs">
          <div>
            <label class="block text-slate-600 mb-1 font-semibold">Mesi di permanenza:</label>
            <input
              type="number"
              min="1"
              max="12"
              v-model="months"
              @input="updateMessage"
              class="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 text-slate-900 focus:bg-white"
            />
          </div>
          <div>
            <label class="block text-slate-600 mb-1 font-semibold">Mese/Periodo inizio:</label>
            <input
              type="text"
              v-model="startDate"
              @input="updateMessage"
              class="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 text-slate-900 focus:bg-white"
            />
          </div>
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1.5">Messaggio da inviare:</label>
          <textarea
            rows="8"
            v-model="messageText"
            class="w-full bg-slate-50 border border-slate-300 rounded-xl p-3 text-sm text-slate-800 font-mono focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
          ></textarea>
        </div>

        <div v-if="rental.contactPhone" class="text-xs text-slate-600 flex items-center gap-1.5 bg-slate-50 p-2.5 rounded-lg border border-slate-200">
          <Phone class="w-4 h-4 text-emerald-600" />
          Contatto: <span class="font-semibold text-slate-900">{{ rental.contactName || 'Referente' }} ({{ rental.contactPhone }})</span>
        </div>
      </div>

      <!-- Footer -->
      <div class="px-6 py-4 bg-slate-50 border-t border-slate-200 flex items-center justify-between gap-3">
        <button
          @click="handleCopy"
          class="flex-1 bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold py-2 px-4 rounded-xl text-sm transition flex items-center justify-center gap-2 border border-slate-300"
        >
          <Check v-if="copied" class="w-4 h-4 text-emerald-600" />
          <Copy v-else class="w-4 h-4" />
          <span>{{ copied ? 'Copiato negli appunti!' : 'Copia Testo' }}</span>
        </button>

        <a
          v-if="whatsappUrl"
          :href="whatsappUrl"
          target="_blank"
          rel="noopener noreferrer"
          class="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2 px-4 rounded-xl text-sm transition flex items-center justify-center gap-2 shadow-md shadow-emerald-600/20"
        >
          <MessageSquare class="w-4 h-4" />
          Apri WhatsApp
        </a>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { X, Copy, Check, MessageSquare, Phone } from 'lucide-vue-next';
import { Rental } from '../types/rental';

const props = defineProps<{
  rental: Rental | null;
}>();

defineEmits(['close']);

const months = ref(2);
const startDate = ref('Ottobre');
const copied = ref(false);
const messageText = ref('');

const updateMessage = () => {
  if (!props.rental) return;
  const contactName = props.rental.contactName ? props.rental.contactName.split(' ')[0] : 'proprietario/a';
  messageText.value = `Salve ${contactName}, 

ho visto il Suo annuncio per l'appartamento a ${props.rental.city}${props.rental.title ? ` ("${props.rental.title}")` : ''}.

Lavoro da remoto in smart working e sto cercando una soluzione in affitto per un periodo temporaneo di ${months.value} mesi (con inizio indicativo da ${startDate.value}). 

Vorrei gentilmente chiederLe:
1. È disponibile per un affitto di ${months.value} mesi?
2. Che tipo di connessione internet (Wi-Fi/Fibra) è presente nell'appartamento?
3. Le utenze e le spese condominiali sono incluse nel canone o conteggiate a parte?

La ringrazio molto per la disponibilità!
Un cordiale saluto.`;
};

watch(() => props.rental, (newVal) => {
  if (newVal) updateMessage();
}, { immediate: true });

const handleCopy = () => {
  navigator.clipboard.writeText(messageText.value);
  copied.value = true;
  setTimeout(() => (copied.value = false), 2000);
};

const whatsappUrl = computed(() => {
  if (!props.rental?.contactPhone) return null;
  const cleanPhone = props.rental.contactPhone.replace(/[^0-9]/g, '');
  return `https://wa.me/${cleanPhone}?text=${encodeURIComponent(messageText.value)}`;
});
</script>
