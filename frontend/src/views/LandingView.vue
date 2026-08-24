<template>
  <div class="min-h-screen bg-slate-50 text-slate-800 font-sans flex flex-col">
    
    <!-- Top Navigation Bar -->
    <header class="bg-white/80 backdrop-blur-md border-b border-slate-200 sticky top-0 z-30">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex items-center justify-between">
        
        <!-- Brand Logo -->
        <div class="flex items-center gap-3">
          <div class="bg-indigo-600 p-2.5 rounded-xl shadow-md shadow-indigo-600/20 text-white flex items-center justify-center">
            <Plane class="w-6 h-6 transform -rotate-45" />
          </div>
          <span class="text-xl font-black text-slate-900 tracking-tight">FlyRent</span>
        </div>

        <!-- Right Nav Buttons -->
        <div class="flex items-center gap-3">
          <router-link
            to="/login"
            class="text-slate-600 hover:text-slate-900 text-xs font-semibold px-3 py-2 rounded-xl transition"
          >
            Accedi
          </router-link>
          <router-link
            to="/login?mode=register"
            class="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold px-4 py-2 rounded-xl shadow-md shadow-indigo-600/20 transition flex items-center gap-1.5"
          >
            Inizia Gratis <ArrowRight class="w-3.5 h-3.5" />
          </router-link>
        </div>

      </div>
    </header>

    <!-- Hero Section -->
    <section class="relative py-20 lg:py-28 overflow-hidden bg-gradient-to-b from-white to-slate-50">
      <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        
        <!-- Badge -->
        <div class="inline-flex items-center gap-2 bg-indigo-50 border border-indigo-200 text-indigo-700 text-xs font-bold px-3.5 py-1.5 rounded-full mb-6 shadow-sm">
          <Wifi class="w-4 h-4 text-indigo-600" />
          <span>Il Tracciatore N.1 per Smart Worker in Italia</span>
        </div>

        <!-- Main Headline -->
        <h1 class="text-4xl sm:text-5xl lg:text-6xl font-black text-slate-900 tracking-tight leading-tight mb-6">
          Lavora da ovunque.<br class="hidden sm:inline" /> Organizza la tua casa ideale in Italia.
        </h1>

        <!-- Subtitle -->
        <p class="text-lg sm:text-xl text-slate-600 max-w-3xl mx-auto mb-10 leading-relaxed">
          Smetti di perdere il filo tra annunci su Facebook, Subito, Idealista e Immobiliare. 
          Confronta in un unico posto connessione Fibra, postazione di lavoro, prezzi reali per 2 mesi e stato dei contatti.
        </p>

        <!-- CTA Buttons -->
        <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
          <router-link
            to="/login?mode=register"
            class="w-full sm:w-auto bg-indigo-600 hover:bg-indigo-700 text-white font-bold px-8 py-3.5 rounded-2xl text-base shadow-xl shadow-indigo-600/30 transition flex items-center justify-center gap-2"
          >
            <span>Crea il tuo Account Gratis</span>
            <ArrowRight class="w-5 h-5" />
          </router-link>

          <router-link
            to="/login"
            class="w-full sm:w-auto bg-white hover:bg-slate-100 text-slate-700 font-bold px-8 py-3.5 rounded-2xl text-base border border-slate-300 shadow-sm transition flex items-center justify-center gap-2"
          >
            <Sparkles class="w-5 h-5 text-amber-500" />
            <span>Accedi all'App</span>
          </router-link>
        </div>

      </div>
    </section>

    <!-- Features Section Grid -->
    <section class="py-16 bg-slate-50 border-t border-slate-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div class="text-center mb-16">
          <h2 class="text-2xl sm:text-3xl font-black text-slate-900">Tutto ciò che serve ad uno Smart Worker</h2>
          <p class="text-sm text-slate-500 mt-2">Progettato per chi lavora da remoto e cerca affitti a breve/medio termine.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          
          <!-- Feature 1 -->
          <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition">
            <div class="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-xl flex items-center justify-center mb-4 border border-indigo-100">
              <Table class="w-6 h-6" />
            </div>
            <h3 class="font-bold text-lg text-slate-900 mb-2">Vista Tabella & Kanban</h3>
            <p class="text-sm text-slate-600 leading-relaxed">
              Organizza gli annunci in una griglia ordinabile o sposta le schede da "Contattato" a "In Attesa" e "Confermato".
            </p>
          </div>

          <!-- Feature 2 -->
          <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition">
            <div class="w-12 h-12 bg-cyan-50 text-cyan-600 rounded-xl flex items-center justify-center mb-4 border border-cyan-100">
              <Wifi class="w-6 h-6" />
            </div>
            <h3 class="font-bold text-lg text-slate-900 mb-2">Smart Work Check</h3>
            <p class="text-sm text-slate-600 leading-relaxed">
              Traccia se l'appartamento dispone di Fibra FTTH 1Gbps, FTTC o FWA e se è presente una vera scrivania di lavoro.
            </p>
          </div>

          <!-- Feature 3 -->
          <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition">
            <div class="w-12 h-12 bg-emerald-50 text-emerald-600 rounded-xl flex items-center justify-center mb-4 border border-emerald-100">
              <Euro class="w-6 h-6" />
            </div>
            <h3 class="font-bold text-lg text-slate-900 mb-2">Calcolo Costo Reale 2 Mesi</h3>
            <p class="text-sm text-slate-600 leading-relaxed">
              Calcola in automatico il costo effettivo sommando canone mensile, stima delle utenze e caparra richiesta.
            </p>
          </div>

          <!-- Feature 4 -->
          <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition">
            <div class="w-12 h-12 bg-purple-50 text-purple-600 rounded-xl flex items-center justify-center mb-4 border border-purple-100">
              <MessageSquare class="w-6 h-6" />
            </div>
            <h3 class="font-bold text-lg text-slate-900 mb-2">Messaggi WhatsApp Rapidi</h3>
            <p class="text-sm text-slate-600 leading-relaxed">
              Genera con un click un messaggio formale e chiaro da inviare ai proprietari su WhatsApp chiedendo disponibilità e Wi-Fi.
            </p>
          </div>

          <!-- Feature 5 -->
          <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition">
            <div class="w-12 h-12 bg-rose-50 text-rose-600 rounded-xl flex items-center justify-center mb-4 border border-rose-100">
              <ImageIcon class="w-6 h-6" />
            </div>
            <h3 class="font-bold text-lg text-slate-900 mb-2">Galleria Foto & Screenshot</h3>
            <p class="text-sm text-slate-600 leading-relaxed">
              Molti annunci su Facebook non hanno foto. Puoi caricare le immagini inviate in chat o fare uno screenshot.
            </p>
          </div>

          <!-- Feature 6 -->
          <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition">
            <div class="w-12 h-12 bg-amber-50 text-amber-600 rounded-xl flex items-center justify-center mb-4 border border-amber-100">
              <ShieldCheck class="w-6 h-6" />
            </div>
            <h3 class="font-bold text-lg text-slate-900 mb-2">Sincronizzazione Cloud</h3>
            <p class="text-sm text-slate-600 leading-relaxed">
              Tutti i dati sono salvati al sicuro nel database cloud. Accedi da qualsiasi computer o smartphone ed hai tutto sincronizzato.
            </p>
          </div>

        </div>

      </div>
    </section>

    <!-- Footer -->
    <footer class="mt-auto bg-white border-t border-slate-200 py-8 text-center text-xs text-slate-500">
      <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div class="flex items-center gap-2 font-bold text-slate-700">
          <Plane class="w-4 h-4 text-indigo-600 transform -rotate-45" /> FlyRent © 2026
        </div>
        <div>
          Tracciatore per Smart Working in Italia. Sincronizzato con MongoDB Atlas.
        </div>
      </div>
    </footer>

  </div>
</template>

<script setup lang="ts">
import { Plane, Wifi, ArrowRight, Sparkles, Table, Euro, MessageSquare, Image as ImageIcon, ShieldCheck } from 'lucide-vue-next';
</script>
