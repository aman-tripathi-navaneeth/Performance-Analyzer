import AppRouter from './routes/AppRouter';
import ErrorBoundary from './components/ErrorBoundary';
import { AuthProvider } from './contexts/AuthContext';
import './App.css';

/**
 * Main Application Component
 * Provides the overall layout structure and routing for the Performance Analyzer
 */
function App() {
  return (
    <AuthProvider>
      <div className="App">
        <ErrorBoundary>
          {/* Navigation is now working properly */}
          
          {/* Main Content Area - Header is included in each page */}
          <main className="main-content">
            <AppRouter />
          </main>
        </ErrorBoundary>
      </div>
    </AuthProvider>
  );
}

export default App;
