# Walmart Price Scraper

A Vue.js web application that allows you to search for product prices on Walmart.com.

## Features

- Search for products by name
- View product prices, images, and ratings
- Responsive design that works on mobile and desktop
- Direct links to products on Walmart.com

## Setup Instructions

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start the backend server:**
   ```bash
   node server.js
   ```
   The server will run on http://localhost:3001

3. **Start the frontend development server:**
   ```bash
   npm run dev
   ```
   The app will be available at http://localhost:3000

## Usage

1. Open your browser and go to http://localhost:3000
2. Enter a product name in the search bar (e.g., "iPhone 15", "Nike shoes")
3. Click "Search" to see the results
4. Browse through the product listings with prices and click "View on Walmart" to go to the product page

## Technical Details

- **Frontend:** Vue.js 3 with Vite
- **Backend:** Node.js with Express
- **Web Scraping:** Cheerio for HTML parsing
- **Styling:** Custom CSS with Walmart-inspired colors

## Important Notes

- This app scrapes publicly available data from Walmart.com for educational purposes
- The scraping functionality may break if Walmart changes their website structure
- Use responsibly and in accordance with Walmart's terms of service
- For production use, consider using official APIs when available