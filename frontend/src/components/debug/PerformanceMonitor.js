import React, { useEffect, useState } from 'react';

/**
 * PerformanceMonitor - Debug component to monitor app performance
 * Remove this component once performance issues are resolved
 */
const PerformanceMonitor = () => {
  const [renderCount, setRenderCount] = useState(0);
  const [lastRender, setLastRender] = useState(Date.now());

  useEffect(() => {
    setRenderCount(prev => prev + 1);
    setLastRender(Date.now());
  });

  const [memoryInfo, setMemoryInfo] = useState(null);

  useEffect(() => {
    const updateMemory = () => {
      if (performance.memory) {
        setMemoryInfo({
          used: Math.round(performance.memory.usedJSHeapSize / 1048576),
          total: Math.round(performance.memory.totalJSHeapSize / 1048576),
          limit: Math.round(performance.memory.jsHeapSizeLimit / 1048576)
        });
      }
    };

    updateMemory();
    const interval = setInterval(updateMemory, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{
      position: 'fixed',
      top: '60px',
      right: '10px',
      background: '#fff',
      border: '2px solid #00f',
      padding: '10px',
      zIndex: 9999,
      fontSize: '11px',
      maxWidth: '200px'
    }}>
      <div><strong>Performance Monitor</strong></div>
      <div>Renders: {renderCount}</div>
      <div>Last: {new Date(lastRender).toLocaleTimeString()}</div>
      {memoryInfo && (
        <div>
          <div>Memory: {memoryInfo.used}MB / {memoryInfo.total}MB</div>
          <div>Limit: {memoryInfo.limit}MB</div>
        </div>
      )}
    </div>
  );
};

export default PerformanceMonitor;