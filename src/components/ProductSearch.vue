<template>
  <div class="search-container">
    <form @submit.prevent="onSearch" class="search-form">
      <div class="search-input-container">
        <input
          v-model="query"
          type="text"
          placeholder="Enter product name (e.g., iPhone 15, Nike shoes)"
          class="search-input"
          :disabled="loading"
        />
        <button 
          type="submit" 
          class="search-button"
          :disabled="loading || !query.trim()"
        >
          <span v-if="loading">Searching...</span>
          <span v-else>Search</span>
        </button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'ProductSearch',
  props: {
    loading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      query: ''
    }
  },
  methods: {
    onSearch() {
      if (this.query.trim()) {
        this.$emit('search', this.query.trim())
      }
    }
  }
}
</script>

<style scoped>
.search-container {
  padding: 30px;
  background: linear-gradient(135deg, #0071ce 0%, #004c87 100%);
}

.search-form {
  max-width: 600px;
  margin: 0 auto;
}

.search-input-container {
  display: flex;
  gap: 12px;
  align-items: center;
}

.search-input {
  flex: 1;
  padding: 16px 20px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.search-input:focus {
  outline: none;
  box-shadow: 0 4px 12px rgba(0, 113, 206, 0.3);
}

.search-input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.search-button {
  padding: 16px 24px;
  background-color: #ffc220;
  color: #000;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.search-button:hover:not(:disabled) {
  background-color: #e6a91a;
  transform: translateY(-1px);
}

.search-button:disabled {
  background-color: #ccc;
  color: #666;
  cursor: not-allowed;
  transform: none;
}

@media (max-width: 768px) {
  .search-input-container {
    flex-direction: column;
  }
  
  .search-input {
    width: 100%;
  }
  
  .search-button {
    width: 100%;
  }
}
</style>