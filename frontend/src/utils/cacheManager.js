/**
 * Cache Manager - Handles cache invalidation for API data
 */

// Event system for cache invalidation
class CacheManager {
  constructor() {
    this.listeners = new Set();
  }

  // Add a listener for cache invalidation events
  addListener(callback) {
    this.listeners.add(callback);
    
    // Return cleanup function
    return () => {
      this.listeners.delete(callback);
    };
  }

  // Trigger cache invalidation
  invalidateCache(reason = 'manual') {
    console.log(`Cache invalidated: ${reason}`);
    this.listeners.forEach(callback => {
      try {
        callback(reason);
      } catch (error) {
        console.error('Error in cache invalidation listener:', error);
      }
    });
  }

  // Specific invalidation methods
  invalidateAfterUpload() {
    this.invalidateCache('file_upload');
  }

  invalidateAfterDataChange() {
    this.invalidateCache('data_change');
  }

  invalidateAll() {
    this.invalidateCache('manual_refresh');
  }
}

// Create singleton instance
const cacheManager = new CacheManager();

export default cacheManager;