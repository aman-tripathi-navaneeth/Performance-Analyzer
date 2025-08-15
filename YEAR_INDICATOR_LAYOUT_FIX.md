# Year Indicator Layout Fix

## 🎯 Layout Description
Fixed the student card year indicator to have:
- **Small symbol at top-left corner** (🌱🌿🌳🎓)
- **Year text centered in the same row** ("1st Year", "2nd Year", etc.)

## 🔧 Implementation

### **Visual Layout**
```
┌─────────────────────────────────────┐
│ 🌱        2nd Year                  │ ← Year indicator row
├─────────────────────────────────────┤
│  👤  John Doe                    →  │ ← Main card content
│      12345678                       │
│      CSE A                          │
│      85% A                          │
└─────────────────────────────────────┘
```

### **CSS Structure**
```css
.year-indicator-row {
  position: absolute;
  top: 0.25rem;
  left: 0;
  right: 0;
  height: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.year-symbol {
  position: absolute;
  left: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.6rem;
}

.year-text {
  font-size: 0.6rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  text-align: center;
}
```

## 📱 Responsive Behavior

### **Desktop**
- Symbol: 0.6rem at left edge
- Text: 0.6rem centered
- Row height: 1.5rem

### **Tablet (768px)**
- Symbol: 0.55rem at left edge
- Text: 0.55rem centered
- Row height: 1.25rem

### **Mobile (480px)**
- Symbol: 0.5rem at left edge
- Text: 0.5rem centered
- Row height: 1rem

## 🎨 Visual Result
Each student card now has:
1. **Top-left corner**: Very small year symbol (🌱🌿🌳🎓)
2. **Center of same row**: Year text ("1st Year", "2nd Year", etc.)
3. **Clean separation**: Year info doesn't interfere with main content

This creates a professional, space-efficient layout perfect for teachers to quickly identify student years while maintaining card readability.