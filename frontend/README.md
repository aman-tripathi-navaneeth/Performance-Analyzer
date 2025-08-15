# Performance Analyzer Frontend

A React-based frontend for the Student Performance Analyzer application.

## Recent Optimizations

### Performance Improvements
- **Simplified Fetch Hook**: Replaced complex `useFetch` with optimized `useFetchSimple`
- **Reduced Re-renders**: Minimized unnecessary component re-renders
- **Performance Utilities**: Added debounce, throttle, and memoization utilities
- **Cleaned Debug Components**: Removed temporary debug components

### Navigation Fixes
- **Fixed Upload Route**: Added missing upload route to navigation
- **Proper Routing**: All routes now work correctly in the header navigation

### Code Structure
```
src/
├── components/
│   ├── common/          # Reusable components (Header, StatCard, etc.)
│   ├── dashboard/       # Dashboard-specific components
│   └── student/         # Student-specific components
├── hooks/
│   └── useFetchSimple.js # Optimized data fetching hook
├── pages/               # Main page components
├── routes/              # Application routing
├── utils/               # Utility functions and helpers
└── api/                 # API service layer
```

## Key Features

### Dashboard
- Class performance overview
- Subject comparison charts
- Grade distribution visualization

### Students Page
- Student list with search functionality
- Performance summaries
- Quick navigation to student profiles

### Student Profile
- Detailed performance metrics
- Radar charts for subject performance
- Historical data visualization

### Upload Page
- CSV file upload for student data
- Data validation and processing
- Progress feedback

## Performance Features

### Optimized Hooks
- `useFetchSimple`: Lightweight data fetching with minimal re-renders
- Performance utilities for debouncing and throttling

### Error Handling
- Global error boundary
- Graceful error states in components
- User-friendly error messages

## Getting Started

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

## Browser Support
- Modern browsers with ES6+ support
- React 18+ features utilized