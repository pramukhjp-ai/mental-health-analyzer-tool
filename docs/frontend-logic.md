# 🎨 Frontend Logic Explained

## Understanding the JavaScript Frontend

The Mental Health Analyzer frontend is built with vanilla JavaScript, HTML5, and CSS3, providing an interactive user interface for all analysis features.

## 📁 Frontend Structure

```
static/
├── css/
│   └── style.css          # All styling and animations
├── js/
│   ├── app.js            # Main application logic
│   ├── recorder.js       # Audio recording functionality
│   └── voiceRecorder.js  # Enhanced voice recording
templates/
└── index.html            # Main HTML template
```

## 🏗️ Main Application Class (app.js)

### MindScopeAnalyzer Class
```javascript
class MindScopeAnalyzer {
    constructor() {
        this.results = {};
        this.isRecording = false;
        this.mediaRecorder = null;
        this.audioChunks = [];
        
        // Initialize UI components
        this.initializeUI();
        this.loadQuestions();
    }
    
    initializeUI() {
        // Set up event listeners for all interactive elements
        this.setupTabNavigation();
        this.setupFormHandlers();
        this.setupFileUploadHandlers();
        this.setupVoiceRecording();
    }
}
```

**Key Concepts:**
- **Class-based architecture**: Organized code structure
- **Event-driven programming**: User interactions trigger analysis
- **State management**: Track recording status and results
- **DOM manipulation**: Dynamic UI updates

### Tab Navigation System
```javascript
setupTabNavigation() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const targetTab = e.target.dataset.tab;
            
            // Remove active class from all tabs
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked tab
            e.target.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
}
```

**Learning Points:**
- **Query Selectors**: `document.querySelectorAll()` for multiple elements
- **Event Listeners**: `addEventListener()` for user interactions
- **Data Attributes**: `dataset.tab` for storing tab information
- **CSS Class Manipulation**: `classList.add/remove()` for styling

## 📝 Text Analysis Implementation

### Form Handling
```javascript
setupFormHandlers() {
    const textForm = document.getElementById('text-analysis-form');
    textForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent page reload
        
        const formData = new FormData(e.target);
        const textInput = formData.get('user_text');
        
        if (!textInput.trim()) {
            this.showError('Please enter some text to analyze');
            return;
        }
        
        await this.analyzeText(textInput);
    });
}

async analyzeText(text) {
    try {
        // Show loading state
        this.showLoading('text-results');
        
        // Make API call
        const response = await fetch('/analyze_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const results = await response.json();
        this.displayTextResults(results);
        
    } catch (error) {
        this.showError(`Analysis failed: ${error.message}`);
    } finally {
        this.hideLoading('text-results');
    }
}
```

**Key Concepts:**
- **Async/Await**: Modern JavaScript for handling promises
- **Fetch API**: Making HTTP requests to the backend
- **Form Data**: Extracting user input from forms
- **Error Handling**: Try/catch blocks for robust error management
- **Loading States**: UI feedback during processing

### Results Display
```javascript
displayTextResults(results) {
    const resultsContainer = document.getElementById('text-results');
    
    // Create sentiment visualization
    const sentimentHtml = this.createSentimentVisualization(results.sentiment);
    
    // Create detailed breakdown
    const detailsHtml = this.createTextDetailsBreakdown(results);
    
    resultsContainer.innerHTML = `
        <div class="results-card">
            <h3>📊 Analysis Results</h3>
            ${sentimentHtml}
            ${detailsHtml}
        </div>
    `;
    
    // Animate results appearance
    resultsContainer.style.opacity = '0';
    resultsContainer.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        resultsContainer.style.transition = 'all 0.3s ease';
        resultsContainer.style.opacity = '1';
        resultsContainer.style.transform = 'translateY(0)';
    }, 100);
}

createSentimentVisualization(sentiment) {
    const polarity = sentiment.polarity;
    const percentage = ((polarity + 1) / 2) * 100; // Convert -1,1 to 0,100
    
    return `
        <div class="sentiment-meter">
            <div class="sentiment-label">Sentiment: ${sentiment.classification}</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${percentage}%"></div>
            </div>
            <div class="sentiment-details">
                <span>Negative</span>
                <span>Neutral</span>
                <span>Positive</span>
            </div>
        </div>
    `;
}
```

## 🎙️ Voice Recording Implementation

### MediaRecorder API Usage
```javascript
setupVoiceRecording() {
    const recordButton = document.getElementById('record-button');
    const stopButton = document.getElementById('stop-button');
    
    recordButton.addEventListener('click', () => this.startRecording());
    stopButton.addEventListener('click', () => this.stopRecording());
}

async startRecording() {
    try {
        // Request microphone access
        const stream = await navigator.mediaDevices.getUserMedia({ 
            audio: {
                echoCancellation: true,
                noiseSuppression: true,
                sampleRate: 44100
            }
        });
        
        // Initialize MediaRecorder
        this.mediaRecorder = new MediaRecorder(stream, {
            mimeType: 'audio/webm'
        });
        
        this.audioChunks = [];
        
        // Handle data collection
        this.mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                this.audioChunks.push(event.data);
            }
        };
        
        // Handle recording completion
        this.mediaRecorder.onstop = () => {
            const audioBlob = new Blob(this.audioChunks, { 
                type: 'audio/webm' 
            });
            this.uploadVoiceRecording(audioBlob);
        };
        
        // Start recording
        this.mediaRecorder.start();
        this.updateRecordingUI(true);
        
    } catch (error) {
        this.showError(`Microphone access denied: ${error.message}`);
    }
}

stopRecording() {
    if (this.mediaRecorder && this.isRecording) {
        this.mediaRecorder.stop();
        this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
        this.updateRecordingUI(false);
    }
}
```

**Advanced Concepts:**
- **Web APIs**: `navigator.mediaDevices.getUserMedia()`
- **MediaRecorder**: Browser-native audio recording
- **Blob Objects**: Binary data handling
- **Promise-based APIs**: Async operations with proper error handling

### File Upload and Processing
```javascript
async uploadVoiceRecording(audioBlob) {
    const formData = new FormData();
    formData.append('voice_file', audioBlob, 'recording.webm');
    
    try {
        this.showLoading('voice-results');
        
        const response = await fetch('/analyze_voice', {
            method: 'POST',
            body: formData  // No Content-Type header for FormData
        });
        
        if (!response.ok) {
            throw new Error(`Upload failed: ${response.status}`);
        }
        
        const results = await response.json();
        this.displayVoiceResults(results);
        
    } catch (error) {
        this.showError(`Voice analysis failed: ${error.message}`);
    } finally {
        this.hideLoading('voice-results');
    }
}
```

## 📸 Image Upload and Preview

### File Input Handling
```javascript
setupFileUploadHandlers() {
    const imageInput = document.getElementById('image-upload');
    const dropZone = document.getElementById('image-drop-zone');
    
    // Handle file selection
    imageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            this.handleImageUpload(file);
        }
    });
    
    // Handle drag and drop
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });
    
    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-over');
    });
    
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            this.handleImageUpload(file);
        }
    });
}

handleImageUpload(file) {
    // Validate file type and size
    if (!this.validateImageFile(file)) {
        return;
    }
    
    // Show image preview
    this.showImagePreview(file);
    
    // Upload for analysis
    this.uploadImageForAnalysis(file);
}

validateImageFile(file) {
    const validTypes = ['image/jpeg', 'image/png', 'image/jpg'];
    const maxSize = 16 * 1024 * 1024; // 16MB
    
    if (!validTypes.includes(file.type)) {
        this.showError('Please upload a JPEG or PNG image');
        return false;
    }
    
    if (file.size > maxSize) {
        this.showError('Image file too large. Maximum size is 16MB');
        return false;
    }
    
    return true;
}

showImagePreview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        const preview = document.getElementById('image-preview');
        preview.innerHTML = `
            <img src="${e.target.result}" alt="Uploaded image" 
                 style="max-width: 300px; max-height: 300px; border-radius: 8px;">
        `;
        preview.style.display = 'block';
    };
    reader.readAsDataURL(file);
}
```

## 🎨 UI Feedback and Animations

### Loading States
```javascript
showLoading(containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = `
        <div class="loading-spinner">
            <div class="spinner"></div>
            <p>Analyzing your data...</p>
        </div>
    `;
}

hideLoading(containerId) {
    // Loading will be replaced by results or hidden
}

showError(message) {
    const errorContainer = document.getElementById('error-messages');
    errorContainer.innerHTML = `
        <div class="error-alert">
            <span class="error-icon">⚠️</span>
            <span class="error-text">${message}</span>
            <button class="close-error" onclick="this.parentElement.remove()">×</button>
        </div>
    `;
    errorContainer.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        errorContainer.style.display = 'none';
    }, 5000);
}
```

### Progress Indicators
```javascript
updateUploadProgress(percentage) {
    const progressBar = document.querySelector('.upload-progress');
    const progressFill = progressBar.querySelector('.progress-fill');
    const progressText = progressBar.querySelector('.progress-text');
    
    progressFill.style.width = `${percentage}%`;
    progressText.textContent = `${Math.round(percentage)}%`;
    
    if (percentage >= 100) {
        setTimeout(() => {
            progressBar.style.display = 'none';
        }, 1000);
    }
}
```

## 📱 Responsive Design Patterns

### Mobile-First CSS Integration
```javascript
// Handle responsive layout changes
handleResponsiveLayout() {
    const isMobile = window.innerWidth <= 768;
    
    if (isMobile) {
        this.enableMobileOptimizations();
    } else {
        this.enableDesktopFeatures();
    }
}

enableMobileOptimizations() {
    // Simplify UI for mobile
    document.body.classList.add('mobile-layout');
    
    // Use touch-friendly controls
    this.setupTouchControls();
}

setupTouchControls() {
    // Add touch event listeners for better mobile experience
    const buttons = document.querySelectorAll('.action-button');
    buttons.forEach(button => {
        button.addEventListener('touchstart', (e) => {
            button.classList.add('pressed');
        });
        
        button.addEventListener('touchend', (e) => {
            button.classList.remove('pressed');
        });
    });
}
```

## 🔄 Data Flow and State Management

### Application State
```javascript
class AppState {
    constructor() {
        this.currentAnalysis = {
            text: null,
            voice: null,
            facial: null
        };
        this.analysisHistory = [];
        this.isProcessing = false;
    }
    
    updateAnalysis(type, results) {
        this.currentAnalysis[type] = results;
        this.saveToHistory();
        this.triggerStateUpdate();
    }
    
    saveToHistory() {
        const analysisSnapshot = {
            timestamp: new Date().toISOString(),
            data: { ...this.currentAnalysis }
        };
        this.analysisHistory.push(analysisSnapshot);
        
        // Keep only last 10 analyses
        if (this.analysisHistory.length > 10) {
            this.analysisHistory.shift();
        }
    }
    
    triggerStateUpdate() {
        // Notify UI components of state changes
        document.dispatchEvent(new CustomEvent('stateUpdate', {
            detail: this.currentAnalysis
        }));
    }
}
```

## 🎯 Key JavaScript Concepts Used

### Modern ES6+ Features
- **Classes**: Object-oriented structure
- **Arrow Functions**: Concise function syntax
- **Template Literals**: String interpolation with `${}`
- **Destructuring**: Extract values from objects/arrays
- **Async/Await**: Promise-based asynchronous code

### DOM Manipulation Patterns
- **Event Delegation**: Efficient event handling
- **Query Selectors**: Finding elements in the DOM
- **Dynamic Content**: Creating HTML with JavaScript
- **CSS Class Management**: Styling changes via JavaScript

### API Integration
- **Fetch API**: Modern way to make HTTP requests
- **FormData**: Handling file uploads
- **JSON Handling**: Parsing and stringifying data
- **Error Handling**: Robust error management

### Browser APIs
- **MediaRecorder**: Audio recording
- **FileReader**: Reading uploaded files
- **Drag and Drop**: File upload via drag/drop
- **Local Storage**: Saving user preferences

## 🧪 Testing Frontend Code

### Console Testing
```javascript
// Test text analysis in browser console
MindScope.analyzeText("I feel great today!")
  .then(results => console.log('Results:', results))
  .catch(error => console.error('Error:', error));

// Test voice recording state
console.log('Recording state:', MindScope.isRecording);

// Test file validation
const testFile = new File(['test'], 'test.jpg', { type: 'image/jpeg' });
console.log('Valid file:', MindScope.validateImageFile(testFile));
```

### Debug Mode
```javascript
// Enable debug logging
const DEBUG = true;

function debugLog(message, data = null) {
    if (DEBUG) {
        console.log(`[Debug] ${message}`, data);
    }
}

// Use throughout the code
debugLog('Starting text analysis', { text: inputText });
debugLog('API response received', results);
```

**Understanding this frontend helps you:**
- 🌐 Learn modern JavaScript web development
- 📱 Understand responsive design principles
- 🎨 See how to create interactive user interfaces
- 🔌 Learn frontend-backend communication
- 📁 Understand file handling in browsers
- 🎙️ Work with browser media APIs

**Next Steps:**
- 🏗️ Check [System Architecture](architecture) to see how frontend and backend connect
- 🔌 Review [API Overview](api-overview) to understand the data flow
- 🎨 Explore the CSS styling patterns in the actual `style.css` file 