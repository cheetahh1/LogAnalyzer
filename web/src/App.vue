<script setup lang="ts">
import { useLogStore } from './stores/logStore';
import FileUploader from './components/FileUploader.vue';
import ResultsDashboard from './components/ResultsDashboard.vue';

const store = useLogStore();

const triggerNewScan = () => {
  store.resetState();
};
</script>

<template>
  <div class="wrapper">
    <nav class="main-nav">
      <div class="nav-content">
        <div class="logo">SSH<span>Analyzer</span></div>
        <div class="nav-actions">
          <button 
            v-if="store.status === 'success' || store.status === 'error'" 
            @click="triggerNewScan" 
            class="nav-btn"
          >
            New Scan
          </button>
        </div>
      </div>
    </nav>

    <main class="content-area">
      <FileUploader v-if="store.status !== 'success'" />
      <ResultsDashboard v-else />
    </main>
  </div>

</template>

<style>
body {
  font-family: 'Inter', Roboto, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f8f9fa;
  color: #2d3748;
}

.wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Navbar */
.main-nav {
  background: #1a202c;
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.logo {
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.logo span {
  color: #42b883;
}

.nav-btn {
  background: #42b883;
  border: none;
  padding: 0.6rem 1.2rem;
  color: white;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.nav-btn:hover {
  background: #38a169;
}

/* Content Area */
.content-area {
  flex: 1;
  padding: 40px 20px;
  display: flex;
  justify-content: center;
}

.container {
  width: 100%;
  max-width: 1000px;
  display: flex;
  justify-content: center;
}
</style>