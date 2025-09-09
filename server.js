const express = require('express')
const cors = require('cors')
const axios = require('axios')
const cheerio = require('cheerio')

const app = express()
const PORT = 3001

app.use(cors())
app.use(express.json())

app.get('/search', async (req, res) => {
  try {
    const query = req.query.q
    if (!query) {
      return res.status(400).json({ error: 'Search query is required' })
    }

    console.log(`Searching for: ${query}`)
    
    const searchUrl = `https://www.walmart.com/search?q=${encodeURIComponent(query)}`
    
    const response = await axios.get(searchUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1'
      },
      timeout: 10000
    })

    const $ = cheerio.load(response.data)
    const products = []

    // Try multiple selector patterns
    const selectors = [
      '[data-testid="item-stack"]',
      '[data-testid="item-product-card"]', 
      '[data-automation-id="product-tile"]',
      '[data-item-id]',
      '.search-result-gridview-item',
      '.Grid-col'
    ]

    for (const selector of selectors) {
      if (products.length > 0) break
      
      $(selector).each((index, element) => {
        if (products.length >= 12) return false
        
        const $element = $(element)
        
        // Try different name selectors
        let name = $element.find('[data-automation-id="product-title"]').text().trim() ||
                  $element.find('h3').text().trim() ||
                  $element.find('a[aria-label]').attr('aria-label') ||
                  $element.find('.product-title-link').text().trim() ||
                  $element.find('[data-testid="product-title"]').text().trim()

        // Try different price selectors  
        let price = $element.find('[itemprop="price"]').attr('content') ||
                   $element.find('[data-automation-id="product-price"] .notranslate').first().text() ||
                   $element.find('.price-current').text() ||
                   $element.find('[data-testid="price-current"]').text() ||
                   $element.find('.price').text()

        if (price) {
          price = price.replace(/[^0-9.]/g, '')
        }

        // Try different image selectors
        let image = $element.find('img[data-automation-id="product-image"]').attr('src') ||
                   $element.find('img').first().attr('src') ||
                   $element.find('img').first().attr('data-src')

        // Try different URL selectors
        let linkElement = $element.find('[data-automation-id="product-title"]').first() ||
                         $element.find('a').first()
        let url = linkElement.attr('href')
        if (url && !url.startsWith('http')) {
          url = `https://www.walmart.com${url}`
        }

        if (name && price && parseFloat(price)) {
          products.push({
            id: `walmart-${index}`,
            name: name.substring(0, 100), // Limit name length
            price: parseFloat(price),
            image: image || '',
            url: url || '',
            source: 'Walmart'
          })
        }
      })
    }

    // If still no products, try to extract from script tags (JSON data)
    if (products.length === 0) {
      const scriptTags = $('script[type="application/json"]')
      scriptTags.each((i, script) => {
        try {
          const content = $(script).html()
          if (content && content.includes('products')) {
            const data = JSON.parse(content)
            // This would need to be customized based on actual JSON structure
            console.log('Found JSON data, might contain product info')
          }
        } catch (e) {
          // Ignore JSON parsing errors
        }
      })
    }

    console.log(`Found ${products.length} products`)
    
    // If no products found, return mock data for testing
    if (products.length === 0) {
      console.log('No products scraped, returning mock data for testing')
      return res.json([
        {
          id: 'mock-1',
          name: `Mock Product for "${query}"`,
          price: 29.99,
          image: 'https://i5.walmartimages.com/seo/Generic-Product-Image_2000x.jpg',
          url: 'https://www.walmart.com',
          source: 'Walmart (Mock)'
        },
        {
          id: 'mock-2', 
          name: `Another ${query} Product`,
          price: 45.50,
          image: 'https://i5.walmartimages.com/seo/Generic-Product-Image_2000x.jpg',
          url: 'https://www.walmart.com',
          source: 'Walmart (Mock)'
        }
      ])
    }

    res.json(products)

  } catch (error) {
    console.error('Error searching products:', error.message)
    res.status(500).json({ 
      error: 'Failed to search products',
      message: error.message 
    })
  }
})

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`)
})