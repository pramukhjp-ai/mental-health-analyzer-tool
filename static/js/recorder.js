// Enhanced Voice Recorder for MindScope AI
class VoiceRecorder {
    constructor() {
        this.mediaRecorder = null;
        this.audioContext = null;
        this.analyser = null;
        this.dataArray = null;
        this.stream = null;
        this.chunks = [];
        this.isRecording = false;
        this.recordingTime = 0;
        this.recordingTimer = null;
        this.visualizer = null;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.createAudioVisualizer();
    }

    setupEventListeners() {
        const startBtn = document.getElementById('startRecording');
        const stopBtn = document.getElementById('stopRecording');

        if (startBtn) {
            startBtn.addEventListener('click', () => this.startRecording());
        }

        if (stopBtn) {
            stopBtn.addEventListener('click', () => this.stopRecording());
        }
    }

    createAudioVisualizer() {
        // Create a simple audio visualizer for better UX
        this.visualizer = {
            canvas: null,
            ctx: null,
            animationId: null
        };
    }

    async startRecording() {
        try {
            // Request microphone permission
            this.stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true
                } 
            });

            // Setup audio context for visualization
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.analyser = this.audioContext.createAnalyser();
            const source = this.audioContext.createMediaStreamSource(this.stream);
            source.connect(this.analyser);

            this.analyser.fftSize = 256;
            const bufferLength = this.analyser.frequencyBinCount;
            this.dataArray = new Uint8Array(bufferLength);

            // Setup MediaRecorder
            this.mediaRecorder = new MediaRecorder(this.stream, {
                mimeType: this.getSupportedMimeType()
            });

            this.chunks = [];
            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.chunks.push(event.data);
                }
            };

            this.mediaRecorder.onstop = () => {
                this.handleRecordingStop();
            };

            // Start recording
            this.mediaRecorder.start();
            this.isRecording = true;
            this.recordingTime = 0;

            // Update UI
            this.updateUI();
            this.startTimer();
            this.startVisualization();

            this.showNotification('Recording started', 'success');

        } catch (error) {
            console.error('Error starting recording:', error);
            this.showNotification('Error accessing microphone: ' + error.message, 'error');
        }
    }

    stopRecording() {
        if (!this.isRecording || !this.mediaRecorder) {
            return;
        }

        this.mediaRecorder.stop();
        this.isRecording = false;

        // Stop all tracks
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
        }

        // Stop timer and visualization
        this.stopTimer();
        this.stopVisualization();

        // Update UI
        this.updateUI();

        this.showNotification('Recording stopped', 'success');
    }

    handleRecordingStop() {
        if (this.chunks.length === 0) {
            this.showNotification('No audio data recorded', 'error');
            return;
        }

        // Create audio blob
        const audioBlob = new Blob(this.chunks, { 
            type: this.getSupportedMimeType() 
        });

        // Store globally for analysis
        window.audioBlob = audioBlob;

        // Enable analysis button
        const analyzeBtn = document.getElementById('analyzeVoiceBtn');
        if (analyzeBtn) {
            analyzeBtn.disabled = false;
        }

        // Create audio preview
        this.createAudioPreview(audioBlob);

        // Clean up
        this.cleanup();
    }

    createAudioPreview(audioBlob) {
        // Remove existing preview
        const existingPreview = document.querySelector('.audio-preview');
        if (existingPreview) {
            existingPreview.remove();
        }

        // Create new preview
        const recordingControls = document.querySelector('.recording-controls');
        if (recordingControls) {
            const preview = document.createElement('div');
            preview.className = 'audio-preview mt-3';
            preview.innerHTML = `
                <div class="glass-card">
                    <h6 class="text-white mb-2">
                        <i data-lucide="headphones"></i>
                        Recording Preview
                    </h6>
                    <audio controls class="w-100" style="filter: sepia(100%) saturate(200%) hue-rotate(240deg);">
                        <source src="${URL.createObjectURL(audioBlob)}" type="${audioBlob.type}">
                        Your browser does not support the audio element.
                    </audio>
                    <div class="text-muted mt-2" style="font-size: 0.85rem;">
                        Duration: ${this.formatTime(this.recordingTime)} | 
                        Size: ${this.formatFileSize(audioBlob.size)}
                    </div>
                </div>
            `;
            
            recordingControls.parentNode.insertBefore(preview, recordingControls.nextSibling);
            
            // Reinitialize Lucide icons
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        }
    }

    updateUI() {
        const startBtn = document.getElementById('startRecording');
        const stopBtn = document.getElementById('stopRecording');
        const statusElement = document.getElementById('recordingStatus');

        if (startBtn && stopBtn && statusElement) {
            if (this.isRecording) {
                startBtn.disabled = true;
                startBtn.classList.add('recording');
                stopBtn.disabled = false;
                
                statusElement.className = 'status-badge negative';
                statusElement.innerHTML = '<i data-lucide="mic"></i> Recording...';
            } else {
                startBtn.disabled = false;
                startBtn.classList.remove('recording');
                stopBtn.disabled = true;
                
                statusElement.className = 'status-badge neutral';
                statusElement.innerHTML = '<i data-lucide="circle"></i> Ready to Record';
            }

            // Reinitialize Lucide icons
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        }
    }

    startTimer() {
        this.recordingTimer = setInterval(() => {
            this.recordingTime++;
            this.updateTimerDisplay();
        }, 1000);
    }

    stopTimer() {
        if (this.recordingTimer) {
            clearInterval(this.recordingTimer);
            this.recordingTimer = null;
        }
    }

    updateTimerDisplay() {
        const timerElement = document.getElementById('recordingTime');
        if (timerElement) {
            timerElement.textContent = this.formatTime(this.recordingTime);
        }
    }

    startVisualization() {
        if (!this.analyser || !this.dataArray) return;

        const visualize = () => {
            if (!this.isRecording) return;

            this.analyser.getByteFrequencyData(this.dataArray);
            
            // Simple visualization using button animation
            const startBtn = document.getElementById('startRecording');
            if (startBtn) {
                const average = this.dataArray.reduce((a, b) => a + b) / this.dataArray.length;
                const intensity = average / 255;
                
                // Animate recording button based on audio level
                startBtn.style.transform = `scale(${1 + intensity * 0.2})`;
                startBtn.style.boxShadow = `0 0 ${20 + intensity * 20}px rgba(245, 87, 108, ${0.5 + intensity * 0.5})`;
            }

            this.visualizer.animationId = requestAnimationFrame(visualize);
        };

        visualize();
    }

    stopVisualization() {
        if (this.visualizer.animationId) {
            cancelAnimationFrame(this.visualizer.animationId);
            this.visualizer.animationId = null;
        }

        // Reset button styling
        const startBtn = document.getElementById('startRecording');
        if (startBtn) {
            startBtn.style.transform = '';
            startBtn.style.boxShadow = '';
        }
    }

    cleanup() {
        if (this.audioContext) {
            this.audioContext.close();
            this.audioContext = null;
        }
        
        this.analyser = null;
        this.dataArray = null;
        this.stream = null;
        this.chunks = [];
    }

    getSupportedMimeType() {
        const types = [
            'audio/webm;codecs=opus',
            'audio/webm',
            'audio/mp4',
            'audio/wav'
        ];

        for (const type of types) {
            if (MediaRecorder.isTypeSupported(type)) {
                return type;
            }
        }

        return 'audio/webm'; // fallback
    }

    formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    showNotification(message, type = 'info') {
        // Create a premium notification
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 2rem;
            right: 2rem;
            background: ${type === 'success' ? 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)' : 
                        type === 'error' ? 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' : 
                        'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(20px);
            z-index: 10000;
            font-weight: 600;
            animation: slideInFromRight 0.3s ease-out;
            max-width: 300px;
            word-wrap: break-word;
        `;
        
        notification.textContent = message;
        document.body.appendChild(notification);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOutToRight 0.3s ease-in';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    // Public methods for external access
    getCurrentRecordingTime() {
        return this.recordingTime;
    }

    isCurrentlyRecording() {
        return this.isRecording;
    }

    hasRecording() {
        return window.audioBlob !== undefined;
    }
}

// Legacy function support for backward compatibility
function toggleRecording() {
    if (window.voiceRecorder) {
        if (window.voiceRecorder.isCurrentlyRecording()) {
            window.voiceRecorder.stopRecording();
        } else {
            window.voiceRecorder.startRecording();
        }
    }
}

function stopRecording() {
    if (window.voiceRecorder) {
        window.voiceRecorder.stopRecording();
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Check if we're on a page that needs the voice recorder
    if (document.getElementById('startRecording')) {
        window.voiceRecorder = new VoiceRecorder();
    }
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VoiceRecorder;
} 