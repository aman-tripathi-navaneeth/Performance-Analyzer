import { useState, useEffect, useCallback } from 'react';

/**
 * Simplified useFetch hook to avoid performance issues
 */
const useFetchSimple = (fetchFunction, dependencies = []) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const execute = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const result = await fetchFunction();
      
      // Handle API response format
      if (result && result.success) {
        setData(result.data);
      } else if (result) {
        setData(result);
      } else {
        throw new Error('No data received');
      }
    } catch (err) {
      console.error('Fetch error:', err);
      setError(err.message || 'An error occurred');
      setData(null);
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

export default useFetchSimple;