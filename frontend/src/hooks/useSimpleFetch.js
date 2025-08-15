import { useState, useEffect, useCallback } from 'react';

/**
 * useSimpleFetch - Simplified, performance-optimized fetch hook
 * Fixes performance issues with the original useFetch hook
 */
const useSimpleFetch = (fetchFunction, dependencies = []) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const execute = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const result = await fetchFunction();
      
      if (result && result.success) {
        setData(result.data);
      } else {
        setData(result);
      }
    } catch (err) {
      console.error('Fetch error:', err);
      setError(err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  }, [fetchFunction]);

  useEffect(() => {
    execute();
  }, dependencies); // eslint-disable-line react-hooks/exhaustive-deps

  const refresh = useCallback(() => {
    execute();
  }, [execute]);

  return {
    data,
    loading,
    error,
    refresh
  };
};

export default useSimpleFetch;