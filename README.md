# Walmart Price Scraper

A Vue.js web application that allows you to search for product prices on Walmart.com.

## Features

- Search for products by name
- View product prices, images, and ratings
- Responsive design that works on mobile and desktop
- Direct links to products on Walmart.com

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher (for frontend only)

### Backend Setup (Python Flask)

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Python backend server:**
   ```bash
   python server.py
   ```
   The server will run on http://localhost:3001

### Frontend Setup (Vue.js)

1. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

2. **Start the frontend development server:**
   ```bash
   npm run dev
   ```
   The app will be available at http://localhost:3000

## Usage

1. Make sure both servers are running (Python backend on :3001, Vue frontend on :3000)
2. Open your browser and go to http://localhost:3000
3. Enter a product name in the search bar (e.g., "iPhone 15", "Nike shoes")
4. Click "Search" to see the results
5. Browse through the product listings with prices and click "View on Walmart" to go to the product page

## Technical Details

- **Frontend:** Vue.js 3 with Vite
- **Backend:** Python Flask with CORS support
- **Web Scraping:** BeautifulSoup for HTML parsing
- **HTTP Requests:** Python requests library with user-agent rotation
- **Styling:** Custom CSS with Walmart-inspired colors

## API Endpoints

- `GET /search?q=<query>` - Search for products
- `GET /health` - Health check endpoint

## Important Notes

- This app scrapes publicly available data from Walmart.com for educational purposes
- The scraping functionality may break if Walmart changes their website structure
- Includes fallback mock data when scraping fails
- Uses random delays and user-agent rotation to be respectful to the target website
- Use responsibly and in accordance with Walmart's terms of service
- For production use, consider using official APIs when available