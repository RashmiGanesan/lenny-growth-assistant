# Design Document: Lenny Growth Assistant

## UI/UX Design

### Layout Structure
```
┌─────────────────────────────────────────────────────────────┐
│ Logo      Lenny Growth Assistant                     v1.0.0 │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────────────────┐ ┌─────────────┐ │
│ │             │ │                         │ │             │ │
│ │   Sidebar   │ │     Chat Messages       │ │ Artifact    │ │
│ │             │ │                         │ │ Viewer      │ │
│ │ - New Chat  │ │ - User messages         │ │ - HTML      │ │
│ │ - Settings  │ │ - AI responses          │ │ - Markdown  │ │
│ │ - Info      │ │ - Loading states        │ │             │ │
│ │             │ │                         │ │             │ │
│ └─────────────┘ └─────────────────────────┘ └─────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │                     Input Area                          │ │
│ │  ┌───────────────────────────────────────┐ [ Send ]    │ │
│ │  │ Type message...                       │             │ │
│ │  └───────────────────────────────────────┘             │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Color Palette
- Primary: `#667eea` to `#764ba2` (gradient)
- Background: `#fafafa`
- Text: `#333333`
- Cards: `#ffffff`
- Borders: `#eaeaea`
- Accent: `#007acc`

### Typography
- Primary: System font stack
- Headers: 18-32px, bold
- Body: 16px, 1.6 line height
- Code: 'Courier New', monospace

### Interactive States
- Hover effects on buttons
- Loading animations
- Smooth transitions
- Error states
- Success notifications

## Component Design

### 1. Chat Message Component
```html
<div class="message user-message">
  <div class="message-header">
    <i class="fas fa-user"></i>
    <span>You</span>
  </div>
  <div class="message-content">
    Message content here
  </div>
  <div class="message-timestamp">
    14:32
  </div>
</div>
```

### 2. Artifact Viewer Component
```html
<div class="artifact-viewer active">
  <div class="artifact-header">
    <h3><i class="fas fa-file-code"></i> Artifact Viewer</h3>
    <button class="close-artifact">×</button>
  </div>
  <div class="artifact-content">
    <!-- HTML iframe or Markdown preview -->
  </div>
</div>
```

### 3. Settings Panel
```html
<div class="settings">
  <h3>Settings</h3>
  <div class="setting-option">
    <label for="llmProvider">LLM Provider:</label>
    <select id="llmProvider">
      <option value="groq">Groq (Llama 3.3)</option>
      <option value="ollama">Ollama (Local)</option>
    </select>
  </div>
</div>
```

## Responsive Design

### Desktop (> 1200px)
- Sidebar: 280px
- Chat: Flexible
- Artifact Viewer: 400px

### Tablet (768px - 1200px)
- Sidebar becomes header
- Artifact viewer overlay
- Adjusted spacing

### Mobile (< 768px)
- Single column layout
- Collapsed sidebar
- Full-width chat
- Bottom input

## Animation Specifications

### Fade In
```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
```

### Loading Spinner
```css
.loading {
  animation: spin 1s linear infinite;
}
```

### Notification
```css
@keyframes fadeInOut {
  0% { opacity: 0; transform: translateY(-20px); }
  10% { opacity: 1; transform: translateY(0); }
  90% { opacity: 1; transform: translateY(0); }
  100% { opacity: 0; transform: translateY(-20px); }
}
```

## Accessibility

### Keyboard Navigation
- Tab through interactive elements
- Enter to send messages
- Escape to close artifact viewer
- Arrow keys for history (future)

### Screen Reader Support
- Semantic HTML structure
- ARIA labels for icons
- Alt text for images
- Proper heading hierarchy

### Color Contrast
- AA compliant contrast ratios
- Text on background: 4.5:1 minimum
- Large text: 3:1 minimum

## Performance Considerations

### Frontend
- Lazy loading for artifacts
- Debounced input
- Optimized images
- Minified assets

### Backend
- Async API calls
- Connection pooling
- Response caching
- Efficient indexing

## Error States

### API Unavailable
- Graceful degradation
- Mock responses
- Clear error messages
- Recovery options

### Network Issues
- Retry logic
- Offline indicators
- Queue messages
- Sync on reconnect

### Invalid Input
- Form validation
- Helpful error messages
- Suggested fixes
- Character limits

## User Flow Diagrams

### New Chat Flow
1. User clicks "New Chat"
2. API creates session
3. Chat cleared
4. Welcome message shown

### Message Flow
1. User types message
2. Selects response type
3. Clicks send
4. Loading indicator
5. Response displayed
6. Artifact shown (if applicable)

### Artifact Flow
1. User selects HTML/Markdown
2. Sends message
3. Response generated
4. Artifact viewer opens
5. Content rendered
6. User can close viewer