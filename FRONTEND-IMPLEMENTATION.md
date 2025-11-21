# Frontend Implementation Documentation

## Overview

The X-UAV frontend is a modern Vue.js 3 + Vite application that provides an interactive interface for browsing and comparing military UAVs.

**Status:** ✅ Fully Implemented and Functional

---

## Technology Stack

- **Framework:** Vue.js 3 (Composition API)
- **Build Tool:** Vite 5
- **HTTP Client:** Axios
- **Styling:** Custom CSS with CSS Variables
- **Port:** 7677 (auto-selected by Vite due to 7676 conflict)

---

## Features Implemented

### ✅ Core Functionality

1. **UAV Listing**
   - Display all 16 UAVs in a responsive table
   - Real-time data fetching from backend API
   - Loading states and error handling

2. **Sorting**
   - Click column headers to sort
   - Sort by: Designation, Name, Country, Type, Wingspan, Endurance, Range, Cost
   - Toggle ascending/descending order
   - Visual sort indicators (▲ ▼)

3. **Filtering**
   - Filter by country (dropdown)
   - Filter by UAV type (dropdown)
   - Text search (designation, name, manufacturer)
   - Clear filters button

4. **Pagination**
   - 20 items per page
   - Previous/Next navigation
   - Page counter display
   - Automatic pagination when filtering

5. **UAV Details Modal**
   - Click any UAV row to view full details
   - Comprehensive specifications display
   - Organized into sections:
     - General Information
     - Physical Characteristics
     - Performance
     - Mission
     - Economics
     - Notes
   - Close with X button or click outside

6. **Responsive Design**
   - Mobile-friendly (480px+)
   - Tablet optimized (768px+)
   - Desktop optimized (1024px+)
   - Touch-friendly controls

7. **Performance**
   - Lazy loading
   - Efficient rendering
   - Optimized API calls
   - Fast sorting/filtering

---

## File Structure

```
frontend/
├── index.html                    # Entry HTML
├── package.json                  # Dependencies and scripts
├── vite.config.js                # Vite configuration
└── src/
    ├── main.js                   # App entry point
    ├── App.vue                   # Root component
    ├── components/
    │   └── UAVList.vue           # Main UAV table component
    ├── services/
    │   └── api.js                # Backend API client
    └── assets/
        └── css/
            └── main.css          # Global styles
```

---

## Components

### App.vue

**Purpose:** Root application component

**Features:**
- Header with branding
- Footer with statistics
- Container for UAVList component
- Fetches and displays total UAV and country count

**Template:**
```vue
<header>
  <h1>X-UAV</h1>
  <p>Unmanned Aerial Vehicle Comparison Platform</p>
</header>
<main>
  <UAVList />
</main>
<footer>
  {uavCount} UAVs from {countryCount} countries
</footer>
```

### UAVList.vue

**Purpose:** Main component for UAV data display and interaction

**State Management:**
- `uavs` - All UAVs from API
- `countries` - Filter options (from API)
- `types` - Filter options (from API)
- `loading` - Loading state
- `error` - Error state
- `selectedUAV` - Currently viewed UAV in modal
- `filters` - Active filters
- `searchQuery` - Text search input
- `sortKey` - Current sort column
- `sortOrder` - Sort direction
- `currentPage` - Pagination state

**Key Functions:**
- `loadUAVs()` - Fetch all UAVs
- `loadFilters()` - Fetch filter options
- `applyFilters()` - Apply backend filters
- `filterUAVs()` - Client-side search filtering
- `sort(key)` - Sort by column
- `selectUAV(uav)` - Open detail modal
- `formatNumber()` - Format numeric values
- `formatCurrency()` - Format USD values

**Computed Properties:**
- `filteredUAVs` - UAVs after search and sort
- `paginatedUAVs` - Current page of UAVs
- `totalPages` - Total number of pages

---

## API Service (api.js)

**Purpose:** Centralized backend API communication

**Base URL:** `/api` (proxied through Vite to http://localhost:8877)

**Methods:**
- `getHealth()` - Health check
- `getStats()` - Database statistics
- `getAllUAVs()` - Fetch all UAVs
- `getUAV(designation)` - Get specific UAV
- `compareUAVs(designations)` - Compare multiple UAVs
- `searchUAVs(filters)` - Search with filters
- `getCountries()` - Get country list
- `getTypes()` - Get type list

**Configuration:**
```javascript
axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' }
})
```

---

## Styling System

### Design System

**Colors:**
- Primary: `#2563eb` (Blue)
- Secondary: `#64748b` (Slate)
- Success: `#10b981` (Green)
- Warning: `#f59e0b` (Amber)
- Danger: `#ef4444` (Red)
- Background: `#f8fafc` (Light gray)
- Card: `#ffffff` (White)
- Text: `#1e293b` (Dark slate)

**Typography:**
- Font: System fonts (-apple-system, Segoe UI, Roboto)
- Base size: 16px
- Line height: 1.6

**Spacing:**
- Consistent padding: 0.625rem, 1rem, 1.5rem, 2rem
- Gaps: 0.5rem, 1rem, 1.5rem

**Shadows:**
- Small: `0 1px 2px rgba(0,0,0,0.05)`
- Medium: `0 4px 6px rgba(0,0,0,0.1)`
- Large: `0 10px 15px rgba(0,0,0,0.1)`

### Key UI Elements

**Header:**
- Gradient background (blue)
- White text
- Prominent title and subtitle

**Controls:**
- Card-style container
- Flexbox filter layout
- Responsive wrapping

**Table:**
- Striped hover effect
- Sortable column headers
- Numeric right-aligned columns
- Badge-style type display
- Color-coded status

**Modal:**
- Overlay with backdrop blur
- Centered content
- Grid layout for details
- Scrollable content
- Close button

**Buttons:**
- Primary (blue)
- Secondary (slate)
- Hover effects with transform
- Disabled states

---

## Responsive Breakpoints

### Desktop (1024px+)
- Multi-column filter layout
- Full table width
- 3-column detail grid

### Tablet (768px - 1024px)
- Stack filters vertically
- Smaller fonts in table
- 2-column detail grid

### Mobile (480px - 768px)
- Single column layout
- Compact table styling
- Single column details
- Larger touch targets

---

## Data Flow

```
User Action
    ↓
Vue Component (UAVList.vue)
    ↓
API Service (api.js)
    ↓
Vite Proxy (/api → http://localhost:8877)
    ↓
FastAPI Backend
    ↓
DuckDB Database
    ↓
Response JSON
    ↓
Vue Component State Update
    ↓
Template Re-render
    ↓
User sees updated UI
```

---

## Installation & Setup

### Prerequisites
- Node.js 18+
- npm or yarn

### Install Dependencies
```bash
cd frontend
npm install
```

### Development Server
```bash
npm run dev
```
- Starts on port 7676 (or next available)
- Hot module replacement enabled
- Auto-opens in browser

### Build for Production
```bash
npm run build
```
- Output in `dist/` directory
- Optimized and minified
- Ready for deployment

### Preview Production Build
```bash
npm run preview
```

---

## Configuration

### vite.config.js

```javascript
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 7676,
    proxy: {
      '/api': {
        target: 'http://localhost:8877',
        changeOrigin: true,
      }
    }
  }
})
```

**Key Settings:**
- Port: 7676 (with auto-increment if occupied)
- API Proxy: /api → http://localhost:8877
- Vue plugin enabled
- HMR (Hot Module Replacement) enabled

---

## API Integration

### Example: Loading UAVs

```javascript
async loadUAVs() {
  try {
    loading.value = true
    error.value = null
    const response = await api.getAllUAVs()
    uavs.value = response.data.uavs
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
```

### Example: Filtering

```javascript
async applyFilters() {
  try {
    loading.value = true
    const response = await api.searchUAVs(filters.value)
    uavs.value = response.data.uavs
    currentPage.value = 1
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
```

---

## User Interactions

### Sorting
1. User clicks column header
2. `sort(key)` function called
3. If same column: toggle order (asc ↔ desc)
4. If different column: set new key, order = asc
5. `filteredUAVs` computed property recalculates
6. Table re-renders with sorted data

### Filtering
1. User selects filter option
2. `applyFilters()` called on change
3. API request with filter parameters
4. Backend returns filtered results
5. Update local state
6. Reset pagination to page 1

### Detail View
1. User clicks UAV row
2. `selectUAV(uav)` called
3. `selectedUAV` set to clicked UAV
4. Modal rendered (v-if="selectedUAV")
5. Click outside or close button
6. `closeModal()` sets selectedUAV = null

---

## Performance Optimizations

1. **Computed Properties**
   - Reactive caching
   - Only recalculate when dependencies change

2. **Pagination**
   - Only render visible rows
   - 20 items at a time

3. **Lazy Loading**
   - Data fetched on mount, not eagerly

4. **API Proxy**
   - No CORS issues
   - Single domain

5. **CSS Optimizations**
   - CSS variables for theming
   - Minimal repaints
   - Hardware-accelerated transforms

---

## Accessibility

- ✅ Semantic HTML5 elements
- ✅ Keyboard navigation
- ✅ Focus states on interactive elements
- ✅ ARIA labels where needed
- ✅ Contrast ratios meet WCAG AA
- ⚠️ Screen reader testing needed
- ⚠️ Full keyboard accessibility audit needed

---

## Browser Compatibility

**Tested:**
- ✅ Chrome 120+
- ✅ Firefox 121+
- ✅ Edge 120+
- ⚠️ Safari (needs testing)
- ⚠️ Mobile browsers (needs testing)

**Requirements:**
- ES6+ support
- CSS Grid support
- Flexbox support
- Modern JavaScript features

---

## Future Enhancements

### Phase 2
- [ ] Add comparison mode (side-by-side)
- [ ] Export to CSV/PDF
- [ ] Save favorite UAVs
- [ ] Share filtered views

### Phase 3
- [ ] Display UAV imagery
- [ ] Show overhead silhouettes (scaled)
- [ ] Interactive size comparison

### Phase 4
- [ ] 3D model viewer with Three.js
- [ ] Rotate and zoom models
- [ ] Component annotations

---

## Troubleshooting

### Frontend won't start
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### API calls failing
- Check backend is running on port 8877
- Verify proxy configuration in vite.config.js
- Check browser console for CORS errors

### Port 7676 in use
- Vite will auto-increment to 7677, 7678, etc.
- Or manually specify: `vite --port 8000`

### Build errors
```bash
# Update dependencies
npm update
npm audit fix
```

---

## Testing

### Manual Testing Checklist
- [x] UAV table displays all 16 UAVs
- [x] Sorting works on all columns
- [x] Country filter works
- [x] Type filter works
- [x] Search filter works
- [x] Clear filters button works
- [x] Pagination works
- [x] Detail modal opens/closes
- [x] Responsive on mobile
- [x] API proxy works
- [x] Error states display
- [x] Loading states display

### Automated Testing (Future)
- [ ] Unit tests with Vitest
- [ ] Component tests with Vue Test Utils
- [ ] E2E tests with Playwright
- [ ] Visual regression tests

---

## Deployment

### Development
```bash
./start.sh   # Starts both backend and frontend
```

### Production

**Option 1: Static Hosting**
```bash
npm run build
# Deploy dist/ folder to:
# - Netlify
# - Vercel
# - GitHub Pages
# - AWS S3 + CloudFront
```

**Option 2: Node Server**
```bash
npm run preview
# Or use a static server like 'serve'
npx serve dist -p 7676
```

**Environment Variables** (for production):
```
VITE_API_BASE_URL=https://api.x-uav.com
```

---

## Maintenance

### Updating Dependencies
```bash
npm outdated              # Check for updates
npm update                # Update to latest compatible
npm audit                 # Check for vulnerabilities
npm audit fix             # Fix vulnerabilities
```

### Code Quality
```bash
# Add these to package.json scripts:
"lint": "eslint src/**/*.{js,vue}"
"format": "prettier --write src/**/*.{js,vue,css}"
```

---

## Contact

For frontend issues or questions, refer to the main README.md

---

**Last Updated:** 2025-11-20
**Version:** 0.1.0
**Status:** Production Ready ✅
