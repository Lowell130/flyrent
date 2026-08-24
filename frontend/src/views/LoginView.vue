<template>
  <div class="min-h-screen bg-slate-50 flex items-center justify-center p-4 font-sans text-slate-800">
    <div class="bg-white border border-slate-200 rounded-3xl shadow-xl w-full max-w-md overflow-hidden p-8">
      
      <!-- Header Logo -->
      <div class="text-center mb-8">
        <router-link to="/" class="inline-block group">
          <div class="bg-indigo-600 w-14 h-14 rounded-2xl shadow-lg shadow-indigo-600/30 text-white flex items-center justify-center mx-auto mb-3 group-hover:scale-105 transition">
            <Plane class="w-8 h-8 transform -rotate-45" />
          </div>
          <h1 class="text-2xl font-black text-slate-900 tracking-tight">FlyRent</h1>
        </router-link>
        <p class="text-xs text-slate-500 mt-1">Smart Working Rental Tracker</p>
      </div>

      <!-- Quick Demo Login Banner -->
      <div class="bg-indigo-50 border border-indigo-200 rounded-2xl p-4 mb-6 text-center">
        <div class="text-xs font-bold text-indigo-900 mb-1">⚡ Accesso Rapido Demo</div>
        <p class="text-[11px] text-indigo-700 mb-3">Accedi subito senza digitare credenziali o crea un tuo account personale.</p>
        <button
          type="button"
          @click="handleDemoLogin"
          :disabled="loading"
          class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 rounded-xl text-xs shadow-md shadow-indigo-600/20 transition flex items-center justify-center gap-1.5"
        >
          <Sparkles class="w-4 h-4 text-amber-300" />
          <span>Accedi come Utente Demo</span>
        </button>
      </div>

      <!-- Mode Switcher Tabs -->
      <div class="flex bg-slate-100 p-1 rounded-xl mb-6">
        <button
          type="button"
          @click="isRegister = false"
          :class="[
            'flex-1 py-2 text-xs font-bold rounded-lg transition-all',
            !isRegister ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-500 hover:text-slate-800'
          ]"
        >
          Accedi
        </button>
        <button
          type="button"
          @click="isRegister = true"
          :class="[
            'flex-1 py-2 text-xs font-bold rounded-lg transition-all',
            isRegister ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-500 hover:text-slate-800'
          ]"
        >
          Registrati
        </button>
      </div>

      <!-- Error Alert -->
      <div v-if="error" class="bg-rose-50 border border-rose-200 text-rose-700 p-3 rounded-xl text-xs mb-4">
        {{ error }}
      </div>

      <!-- Form -->
      <form @submit.prevent="handleSubmit" class="space-y-4">
        
        <div v-if="isRegister">
          <label class="block text-xs font-semibold text-slate-700 mb-1">Nome Completo</label>
          <div class="relative">
            <User class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              required
              v-model="form.name"
              placeholder="es. Mario Rossi"
              class="w-full bg-slate-50 border border-slate-300 rounded-xl pl-9 pr-3 py-2 text-sm text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Email</label>
          <div class="relative">
            <Mail class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="email"
              required
              v-model="form.email"
              placeholder="nome@email.com"
              class="w-full bg-slate-50 border border-slate-300 rounded-xl pl-9 pr-3 py-2 text-sm text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Password</label>
          <div class="relative">
            <Lock class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="password"
              required
              v-model="form.password"
              placeholder="••••••••"
              class="w-full bg-slate-50 border border-slate-300 rounded-xl pl-9 pr-3 py-2 text-sm text-slate-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-slate-900 hover:bg-slate-800 text-white font-bold py-2.5 rounded-xl text-sm shadow-md transition flex items-center justify-center gap-2 mt-6 disabled:opacity-50"
        >
          <span v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
          <span>{{ isRegister ? 'Crea Account' : 'Accedi a FlyRent' }}</span>
        </button>

      </form>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { Plane, Mail, Lock, User, Sparkles } from 'lucide-vue-next';
import { api } from '../services/api';

const router = useRouter();
const route = useRoute();

const isRegister = ref(false);
const loading = ref(false);
const error = ref<string | null>(null);

onMounted(() => {
  if (route.query.mode === 'register') {
    isRegister.value = true;
  }
});

const form = reactive({
  name: '',
  email: '',
  password: ''
});

const handleSubmit = async () => {
  error.value = null;
  loading.value = true;
  try {
    let data;
    if (isRegister.value) {
      data = await api.register({
        name: form.name,
        email: form.email,
        password: form.password
      });
    } else {
      data = await api.login({
        email: form.email,
        password: form.password
      });
    }

    localStorage.setItem('token', data.access_token);
    localStorage.setItem('user', JSON.stringify(data.user));

    router.push('/dashboard');
  } catch (err: any) {
    console.error('Auth error:', err);
    error.value = err.response?.data?.detail || 'Errore durante l\'autenticazione';
  } finally {
    loading.value = false;
  }
};

const handleDemoLogin = async () => {
  error.value = null;
  loading.value = true;
  const demoEmail = 'stefano@example.com';
  const demoPassword = 'flyrent2026';

  try {
    let data;
    try {
      data = await api.login({ email: demoEmail, password: demoPassword });
    } catch (e) {
      data = await api.register({ name: 'Stefano Demo', email: demoEmail, password: demoPassword });
    }

    localStorage.setItem('token', data.access_token);
    localStorage.setItem('user', JSON.stringify(data.user));

    router.push('/dashboard');
  } catch (err: any) {
    console.error('Demo login error:', err);
    error.value = 'Impossibile accedere con l\'account demo.';
  } finally {
    loading.value = false;
  }
};
</script>
