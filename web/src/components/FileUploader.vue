<script setup lang="ts">
import { ref, watch } from 'vue';
import { useLogStore } from '../stores/logStore';
import { validateLogFile } from '@/utils/fileValidator';

const store = useLogStore();
const fileInputRef = ref<HTMLInputElement | null>(null);
const isDragging = ref(false);

// --- Event Handlers ---
const onDragOver = () => { isDragging.value = true; };
const onDragLeave = () => { isDragging.value = false; };

const handleFileAction = (file: File) => {
    const validation = validateLogFile(file);

    if (!validation.isValid) {
        store.status = 'error';
        store.errorMessage = validation.error || 'Unknown file validation error.';
        return;
    }

    store.handleFileUpload(file);
};

const onDrop = (e: DragEvent) => {
    isDragging.value = false;
    const file = e.dataTransfer?.files?.[0]; // Get the first file if it exists
    if (file) handleFileAction(file);
};

// Handle manual file selection via the browser dialog
const onFileSelected = (e: Event) => {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (file) handleFileAction(file);
};

// Trigger the hidden standard file input when clicking the box
const triggerManualSelect = () => {
    // Don't trigger if already uploading
    if (store.status === 'idle' || store.status === 'error') {
        fileInputRef.value?.click();
    }
}

watch(() => store.status, (newStatus) => {
  if (newStatus === 'idle' && fileInputRef.value) {
    fileInputRef.value.value = ''; // This allows selecting the same file again
  }
});
</script>

<template>
    <div class="uploader-container">
        <h1 class="title">SSH Security Analyzer</h1>
        <p class="description">
            Analyze your server's authentication logs for brute-force attacks and suspicious activity. Drag and drop
            your `/var/log/auth.log` file below.
        </p>

        <div class="dropzone" :class="{
            'dragging': isDragging,
            'processing': store.status === 'uploading',
            'error-state': store.status === 'error'
        }" @dragover.prevent="onDragOver" @dragleave.prevent="onDragLeave" @drop.prevent="onDrop"
            @click="triggerManualSelect">
            <input type="file" ref="fileInputRef" @change="onFileSelected" hidden accept=".log,.txt" />


            <div v-if="store.status === 'uploading'" class="state-content">
                <div class="spinner"></div>
                <p class="state-text">Analyzing <strong>{{ store.selectedFileName }}</strong>...</p>
            </div>


            <div v-else-if="store.status === 'success'" class="state-content success-view">
                <div class="success-header">
                    <h2 class="results-title">Analysis Results</h2>
                    <p class="results-subtitle">Detected {{ store.analysisResults.length }} unique suspicious IPs</p>
                </div>

                <div class="results-table-container">
                    <table class="results-table">
                        <thead>
                            <tr>
                                <th>IP Address</th>
                                <th>Failed Attempts</th>
                                <th>Targeted Users</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="item in store.analysisResults" :key="item.ip">
                                <td class="ip-cell">{{ item.ip }}</td>
                                <td class="count-cell">{{ item.count }}</td>
                                <td class="users-cell">{{ item.users.join(', ') }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <button class="reset-btn" @click.stop="store.resetState">Analyze another file</button>
            </div>


            <div v-else class="state-content idle">
                <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"
                    class="upload-icon">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                    <polyline points="17 8 12 3 7 8" />
                    <line x1="12" x2="12" y1="3" y2="15" />
                </svg>

                <p class="main-text">Drag and drop your log file here</p>
                <p class="sub-text">or click to browse</p>
                <p class="limit-text">Supports .log and plain .txt files</p>
            </div>
        </div>

        <div v-if="store.status === 'error'" class="error-container">
            <p>{{ store.errorMessage }}</p>
            <button class="retry-btn" @click="store.resetState">Try Again</button>
        </div>
    </div>
</template>

<style scoped>
.uploader-container {
    max-width: 800px;
    width: 100%;
    text-align: center;
    padding: 2rem;
    background: white;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.title {
    font-size: 2rem;
    color: #1a1a1a;
    margin-bottom: 0.5rem;
}

.description {
    font-size: 1.1rem;
    color: #666;
    margin-bottom: 2.5rem;
    line-height: 1.5;
}

.dropzone {
    border: 3px dashed #e0e0e0;
    border-radius: 12px;
    padding: 3rem 2rem;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
    background-color: #fdfdfd;
    min-height: 250px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.dropzone:hover:not(.processing) {
    border-color: #aaa;
    background-color: #f5f5f5;
}

.dropzone.dragging {
    border-color: #42b883;
    background-color: #ecfdf5;
}

.dropzone.error-state {
    border-color: #d32f2f;
    background-color: #fff5f5;
}


.state-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.8rem;
}

.upload-icon {
    color: #999;
    margin-bottom: 1rem;
}

.main-text {
    font-size: 1.4rem;
    font-weight: 600;
    color: #333;
    margin: 0;
}

.sub-text {
    color: #666;
    margin: 0;
    font-size: 1.1rem;
}

.limit-text {
    margin-top: 1.5rem;
    font-size: 0.9rem;
    color: #999;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.state-text {
    font-size: 1.2rem;
    color: #444;
}

.big-icon {
    font-size: 4rem;
}

.reset-btn,
.retry-btn {
    padding: 0.6rem 1.2rem;
    cursor: pointer;
    background-color: #42b883;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 1rem;
    font-weight: 600;
    margin-top: 1rem;
}

.retry-btn {
    background-color: #d32f2f;
}

.error-container {
    margin-top: 1.5rem;
    color: #d32f2f;
    font-weight: bold;
}

.spinner {
    border: 4px solid #f3f3f3;
    border-top: 4px solid #42b883;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}
</style>