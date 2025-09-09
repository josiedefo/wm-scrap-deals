from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
import time
import random

app = Flask(__name__)
CORS(app)

def get_headers():
    """Return headers that mimic a real browser"""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]
    
    return {
        'User-Agent': random.choice(user_agents),
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
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive'
    }

def extract_price(price_text):
    """Extract numeric price from text"""
    if not price_text:
        return None
    
    # Remove all non-digit and non-decimal characters
    price_clean = re.sub(r'[^\d.]', '', price_text)
    
    try:
        return float(price_clean) if price_clean else None
    except ValueError:
        return None

def scrape_walmart_products(query, max_products=12):
    """Scrape products from Walmart search results"""
    search_url = f"https://www.walmart.com/search?q={requests.utils.quote(query)}"
    
    try:
        print(f"Searching for: {query}")
        print(f"URL: {search_url}")
        
        # Add random delay to appear more human-like
        time.sleep(random.uniform(1, 3))
        
        response = requests.get(search_url, headers=get_headers(), timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        products = []
        
        # Multiple selector strategies
        selectors = [
            '[data-testid="item-stack"]',
            '[data-testid="item-product-card"]',
            '[data-automation-id="product-tile"]',
            '.search-result-gridview-item',
            '[data-item-id]',
            '.Grid-col'
        ]
        
        for selector in selectors:
            if len(products) >= max_products:
                break
                
            elements = soup.select(selector)
            print(f"Found {len(elements)} elements with selector: {selector}")
            
            for i, element in enumerate(elements):
                if len(products) >= max_products:
                    break
                
                # Extract product name
                name_selectors = [
                    '[data-automation-id="product-title"]',
                    'h3',
                    'a[aria-label]',
                    '.product-title-link',
                    '[data-testid="product-title"]'
                ]
                
                name = None
                for name_sel in name_selectors:
                    name_elem = element.select_one(name_sel)
                    if name_elem:
                        if name_sel == 'a[aria-label]':
                            name = name_elem.get('aria-label', '').strip()
                        else:
                            name = name_elem.get_text(strip=True)
                        if name:
                            break
                
                # Extract price
                price_selectors = [
                    '[itemprop="price"]',
                    '[data-automation-id="product-price"] .notranslate',
                    '.price-current',
                    '[data-testid="price-current"]',
                    '.price'
                ]
                
                price = None
                for price_sel in price_selectors:
                    price_elem = element.select_one(price_sel)
                    if price_elem:
                        price_text = price_elem.get('content') or price_elem.get_text(strip=True)
                        price = extract_price(price_text)
                        if price:
                            break
                
                # Extract image
                img_selectors = [
                    'img[data-automation-id="product-image"]',
                    'img'
                ]
                
                image_url = None
                for img_sel in img_selectors:
                    img_elem = element.select_one(img_sel)
                    if img_elem:
                        image_url = img_elem.get('src') or img_elem.get('data-src')
                        if image_url:
                            break
                
                # Extract product URL
                link_selectors = [
                    '[data-automation-id="product-title"]',
                    'a'
                ]
                
                product_url = None
                for link_sel in link_selectors:
                    link_elem = element.select_one(link_sel)
                    if link_elem:
                        href = link_elem.get('href')
                        if href:
                            if href.startswith('http'):
                                product_url = href
                            else:
                                product_url = f"https://www.walmart.com{href}"
                            break
                
                # Add product if we have essential data
                if name and price:
                    products.append({
                        'id': f'walmart-{len(products)}',
                        'name': name[:100],  # Limit name length
                        'price': price,
                        'image': image_url or '',
                        'url': product_url or '',
                        'source': 'Walmart'
                    })
                    print(f"Added product: {name} - ${price}")
        
        print(f"Total products found: {len(products)}")
        return products
        
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return []
    except Exception as e:
        print(f"Scraping error: {e}")
        return []

@app.route('/search', methods=['GET'])
def search_products():
    try:
        query = request.args.get('q')
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        products = scrape_walmart_products(query)
        
        # If no products found, return mock data for testing
        if not products:
            print("No products scraped, returning mock data for testing")
            products = [
                {
                    'id': 'mock-1',
                    'name': f'Mock Product for "{query}"',
                    'price': 29.99,
                    'image': 'https://i5.walmartimages.com/seo/Generic-Product-Image_2000x.jpg',
                    'url': 'https://www.walmart.com',
                    'source': 'Walmart (Mock)'
                },
                {
                    'id': 'mock-2',
                    'name': f'Another {query} Product',
                    'price': 45.50,
                    'image': 'https://i5.walmartimages.com/seo/Generic-Product-Image_2000x.jpg',
                    'url': 'https://www.walmart.com',
                    'source': 'Walmart (Mock)'
                },
                {
                    'id': 'mock-3',
                    'name': f'Premium {query} Edition',
                    'price': 79.99,
                    'image': 'https://i5.walmartimages.com/seo/Generic-Product-Image_2000x.jpg',
                    'url': 'https://www.walmart.com',
                    'source': 'Walmart (Mock)'
                }
            ]
        
        return jsonify(products)
        
    except Exception as e:
        print(f"API error: {e}")
        return jsonify({
            'error': 'Failed to search products',
            'message': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Python Flask server is running'})

if __name__ == '__main__':
    print("Starting Walmart Price Scraper Python Server...")
    print("Server will run on http://localhost:3001")
    app.run(debug=True, host='0.0.0.0', port=3001)