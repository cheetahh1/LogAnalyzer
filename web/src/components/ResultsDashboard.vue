<template>
    <div class="dashboard-container">
        <div class="stats-row">
            <div class="stat-card">
                <h3>Total IPs Flagged</h3>
                <p class="value">{{ store.analysisResults.length }}</p>
            </div>
            <div class="stat-card danger">
                <h3>Most Suspicious</h3>
                <p class="value">{{ store.analysisResults[0]?.ip || 'None' }}</p>
            </div>
        </div>

        <div class="table-wrapper">
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
                        <td class="ip-text">{{ item.ip }}</td>
                        <td class="count-text">
                            <span :class="['badge', item.count > 10 ? 'high' : 'low']">{{ item.count }}</span>
                        </td>
                        <td>
                            <div class="user-pills">
                                <span v-for="u in item.users" :key="u" class="pill">{{ u }}</span>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useLogStore } from '../stores/logStore';
const store = useLogStore();
</script>

<style scoped>
.dashboard-container {
    width: 100%;
    max-width: 1000px;
}

.stats-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
}

.stat-card {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    flex: 1;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border-top: 4px solid #42b883;
}

.stat-card.danger {
    border-top-color: #e53e3e;
}

.value {
    font-size: 2rem;
    font-weight: bold;
    margin: 0;
}

.table-wrapper {
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.results-table {
    width: 100%;
    border-collapse: collapse;
}

.results-table th {
    background: #f7fafc;
    padding: 1rem;
    text-align: left;
    border-bottom: 1px solid #edf2f7;
}

.results-table td {
    padding: 1rem;
    border-bottom: 1px solid #edf2f7;
}

.results-table tbody tr:hover {
  background-color: #f7fafc;
  transition: background-color 0.2s ease;
}

.badge {
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-weight: bold;
}

.badge.high {
    background: #fed7d7;
    color: #c53030;
}

.badge.low {
    background: #f0fff4;
    color: #2f855a;
}

.user-pills {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.pill {
    background: #edf2f7;
    padding: 2px 8px;
    border-radius: 99px;
    font-size: 0.8rem;
    font-family: monospace;
}
</style>