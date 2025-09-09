<template>
  <div class="results-container">
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    
    <div v-else-if="results.length === 0" class="no-results">
      <p>No results found. Try searching for a product above!</p>
    </div>
    
    <div v-else class="results-grid">
      <div 
        v-for="product in results" 
        :key="product.id"
        class="product-card"
      >
        <div class="product-image">
          <img 
            :src="product.image" 
            :alt="product.name"
            @error="handleImageError"
          />
        </div>
        
        <div class="product-info">
          <h3 class="product-name">{{ product.name }}</h3>
          
          <div class="price-container">
            <span class="current-price">${{ product.price }}</span>
            <span v-if="product.originalPrice && product.originalPrice !== product.price" 
                  class="original-price">${{ product.originalPrice }}</span>
          </div>
          
          <div v-if="product.rating" class="rating">
            <span class="stars">{{ '★'.repeat(Math.floor(product.rating)) }}</span>
            <span class="rating-text">({{ product.rating }}/5)</span>
          </div>
          
          <a 
            :href="product.url" 
            target="_blank" 
            rel="noopener noreferrer"
            class="view-button"
          >
            View on Walmart
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductResults',
  props: {
    results: {
      type: Array,
      default: () => []
    },
    error: {
      type: String,
      default: null
    }
  },
  methods: {
    handleImageError(event) {
      event.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjRjVGNUY1Ii8+CjxwYXRoIGQ9Ik03MCA3MEgxMzBWMTMwSDcwVjcwWiIgZmlsbD0iI0NDQ0NDQyIvPgo8L3N2Zz4K'
    }
  }
}
</script>

<style scoped>
.results-container {
  padding: 30px;
}

.error-message {
  background-color: #fee;
  color: #c33;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  border: 1px solid #fcc;
}

.no-results {
  text-align: center;
  color: #666;
  padding: 40px 20px;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.product-card {
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  background: white;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.product-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
  background-color: #f9f9f9;
  display: flex;
  align-items: center;
  justify-content: center;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-info {
  padding: 20px;
}

.product-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.4;
}

.price-container {
  margin-bottom: 12px;
}

.current-price {
  font-size: 24px;
  font-weight: 700;
  color: #0071ce;
}

.original-price {
  font-size: 16px;
  color: #666;
  text-decoration: line-through;
  margin-left: 8px;
}

.rating {
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.stars {
  color: #ffc220;
  font-size: 14px;
}

.rating-text {
  font-size: 14px;
  color: #666;
}

.view-button {
  display: inline-block;
  background-color: #0071ce;
  color: white;
  padding: 12px 20px;
  text-decoration: none;
  border-radius: 6px;
  font-weight: 600;
  text-align: center;
  transition: background-color 0.3s ease;
}

.view-button:hover {
  background-color: #004c87;
}

@media (max-width: 768px) {
  .results-grid {
    grid-template-columns: 1fr;
  }
}
</style>