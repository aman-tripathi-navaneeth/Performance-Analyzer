import React from 'react';
import { useNavigate } from 'react-router-dom';

/**
 * SimpleYearCard - A professional year card component
 */
const SimpleYearCard = ({ yearNumber, studentCount }) => {
  const navigate = useNavigate();
  
  const handleClick = () => {
    if (studentCount > 0) {
      navigate(`/students/year/${yearNumber}`);
    }
  };
  
  const getYearIcon = (year) => {
    switch (year) {
      case 1: return '🌱';
      case 2: return '🌿';
      case 3: return '🌳';
      case 4: return '🎓';
      default: return '📚';
    }
  };
  
  const getCountColor = (count) => {
    if (count >= 50) return '#059669';
    if (count >= 20) return '#0284c7';
    if (count > 0) return '#d97706';
    return '#94a3b8';
  };
  
  const cardStyle = {
    background: studentCount > 0 
      ? 'rgba(255, 255, 255, 0.95)' 
      : 'rgba(248, 249, 250, 0.8)',
    backdropFilter: 'blur(10px)',
    border: '1px solid rgba(226, 232, 240, 0.5)',
    borderRadius: '24px',
    padding: '2rem',
    margin: '0',
    cursor: studentCount > 0 ? 'pointer' : 'not-allowed',
    opacity: studentCount > 0 ? 1 : 0.5,
    userSelect: 'none',
    transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
    boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
    display: 'flex',
    alignItems: 'center',
    gap: '1.5rem',
    position: 'relative',
    overflow: 'hidden'
  };
  
  const hoverStyle = {
    ...cardStyle,
    background: studentCount > 0 ? 'rgba(255, 255, 255, 1)' : cardStyle.background,
    transform: studentCount > 0 ? 'translateY(-8px) scale(1.02)' : 'none',
    boxShadow: studentCount > 0 
      ? '0 32px 64px rgba(0, 0, 0, 0.15), 0 8px 16px rgba(0, 0, 0, 0.1)'
      : cardStyle.boxShadow
  };
  
  const iconStyle = {
    fontSize: '3rem',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '80px',
    height: '80px',
    background: 'linear-gradient(135deg, #667eea, #764ba2)',
    borderRadius: '50%',
    color: 'white',
    flexShrink: 0,
    boxShadow: '0 8px 24px rgba(102, 126, 234, 0.3)'
  };
  
  const infoStyle = {
    flex: 1
  };
  
  const titleStyle = {
    fontSize: '1.5rem',
    fontWeight: '800',
    color: '#1a202c',
    margin: '0 0 1rem 0',
    letterSpacing: '-0.02em'
  };
  
  const countStyle = {
    fontSize: '2rem',
    fontWeight: '900',
    color: getCountColor(studentCount),
    margin: '0',
    textShadow: studentCount > 0 ? `0 2px 4px ${getCountColor(studentCount)}20` : 'none'
  };
  
  const labelStyle = {
    fontSize: '0.75rem',
    color: '#64748b',
    textTransform: 'uppercase',
    letterSpacing: '1px',
    fontWeight: '600',
    margin: '0.25rem 0 0 0'
  };
  
  const arrowStyle = {
    fontSize: '1.5rem',
    color: studentCount > 0 ? '#cbd5e1' : '#e2e8f0',
    fontWeight: 'bold',
    transition: 'all 0.4s ease',
    opacity: studentCount > 0 ? 0.7 : 0.3
  };
  
  return (
    <div
      style={cardStyle}
      onClick={handleClick}
      onMouseEnter={(e) => {
        if (studentCount > 0) {
          Object.assign(e.target.style, hoverStyle);
          const arrow = e.target.querySelector('.arrow');
          if (arrow) {
            arrow.style.color = '#667eea';
            arrow.style.transform = 'translateX(8px) scale(1.1)';
            arrow.style.opacity = '1';
          }
        }
      }}
      onMouseLeave={(e) => {
        Object.assign(e.target.style, cardStyle);
        const arrow = e.target.querySelector('.arrow');
        if (arrow) {
          arrow.style.color = arrowStyle.color;
          arrow.style.transform = 'none';
          arrow.style.opacity = arrowStyle.opacity;
        }
      }}
    >
      <div style={iconStyle}>
        {getYearIcon(yearNumber)}
      </div>
      
      <div style={infoStyle}>
        <h3 style={titleStyle}>Year {yearNumber}</h3>
        <div style={countStyle}>{studentCount}</div>
        <div style={labelStyle}>Students</div>
      </div>
      
      <div className="arrow" style={arrowStyle}>
        →
      </div>
    </div>
  );
};

export default SimpleYearCard;