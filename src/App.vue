<template>
  <div id="app">
    <header class="header">
      <h1>Walmart Price Finder</h1>
      <p>Search for product prices on Walmart.com</p>
    </header>
    
    <main class="main">
      <ProductSearch @search="handleSearch" :loading="loading" />
      <ProductResults :results="searchResults" :error="error" />
    </main>
  </div>
</template>

<script>
import ProductSearch from './components/ProductSearch.vue'
import ProductResults from './components/ProductResults.vue'
import axios from 'axios'

export default {
  name: 'App',
  components: {
    ProductSearch,
    ProductResults
  },
  data() {
    return {
      searchResults: [],
      loading: false,
      error: null
    }
  },
  methods: {
    async handleSearch(query) {
      this.loading = true
      this.error = null
      this.searchResults = []
      
      try {
        const response = await axios.get(`/api/search?q=${encodeURIComponent(query)}`)
        this.searchResults = response.data
      } catch (error) {
        this.error = 'Failed to search products. Please try again.'
        console.error('Search error:', error)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background-color: #f5f5f5;
}

#app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.header h1 {
  color: #0071ce;
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.header p {
  color: #666;
  font-size: 1.1rem;
}

.main {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}
</style>