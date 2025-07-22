// Voice Recorder Module - Handles individual question recording
class VoiceRecorder {
    constructor() {
        this.recordings = {};
        this.currentRecordingIndex = null;
        this.timers = {};
        this.init();
    }

    init() {
        this.setupGlobalEventListeners();
    }

    setupGlobalEventListeners() {
        // Listen for question recording events
        document.addEventListener('questionRecording:start', (e) => {
            this.startRecording(e.detail.questionIndex);
        });

        document.addEventListener('questionRecording:stop', (e) => {
            this.stopRecording(e.detail.questionIndex);
        });
    }

    async startRecording(questionIndex) {
        try {
            // Stop any other recording first
            if (this.currentRecordingIndex !== null && this.currentRecordingIndex !== questionIndex) {
                await this.stopRecording(this.currentRecordingIndex);
            }

            // Request microphone permission
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true
                } 
            });

            // Setup MediaRecorder
            const mediaRecorder = new MediaRecorder(stream, {
                mimeType: this.getSupportedMimeType()
            });

            const chunks = [];
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.recordings[questionIndex].chunks.push(event.data);
                }
            };

            mediaRecorder.onstop = () => {
                this.handleRecordingStop(questionIndex, stream);
            };

            // Start recording
            mediaRecorder.start();
            this.currentRecordingIndex = questionIndex;
            this.recordings[questionIndex] = { 
                mediaRecorder, 
                stream, 
                startTime: Date.now(),
                chunks: chunks
            };

            // Update UI
            this.updateUI(questionIndex, 'recording');
            this.startTimer(questionIndex);

            // Dispatch event
            this.dispatchEvent('recordingStarted', { questionIndex });

        } catch (error) {
            console.error('Error starting recording:', error);
            this.dispatchEvent('recordingError', { questionIndex, error: error.message });
        }
    }

    async stopRecording(questionIndex) {
        const recording = this.recordings[questionIndex];
        if (!recording) return;

        recording.mediaRecorder.stop();
        recording.stream.getTracks().forEach(track => track.stop());
        
        this.stopTimer(questionIndex);
        this.currentRecordingIndex = null;
    }

    handleRecordingStop(questionIndex, stream) {
        const recording = this.recordings[questionIndex];
        if (!recording || !recording.chunks || recording.chunks.length === 0) {
            this.dispatchEvent('recordingError', { 
                questionIndex, 
                error: 'No audio data recorded' 
            });
            this.updateUI(questionIndex, 'ready');
            return;
        }

        // Create audio blob from stored chunks
        const audioBlob = new Blob(recording.chunks, { type: this.getSupportedMimeType() });
        
        // Store recording
        recording.audioBlob = audioBlob;
        recording.duration = this.calculateDuration(questionIndex);

        // Update UI
        this.updateUI(questionIndex, 'recorded');
        this.createAudioPreview(questionIndex, audioBlob);
        
        // Dispatch event
        this.dispatchEvent('recordingCompleted', { 
            questionIndex, 
            audioBlob,
            duration: recording.duration
        });
    }

    updateUI(questionIndex, status) {
        const startBtn = document.getElementById(`startRecord_${questionIndex}`);
        const stopBtn = document.getElementById(`stopRecord_${questionIndex}`);
        const statusElement = document.getElementById(`status_${questionIndex}`);

        if (startBtn && stopBtn && statusElement) {
            if (status === 'recording') {
                startBtn.disabled = true;
                startBtn.classList.add('recording');
                stopBtn.disabled = false;
                
                statusElement.className = 'question-status-badge recording';
                statusElement.innerHTML = '<i data-lucide="mic"></i> Recording...';
            } else if (status === 'recorded') {
                startBtn.disabled = false;
                startBtn.classList.remove('recording');
                stopBtn.disabled = true;
                
                statusElement.className = 'question-status-badge recorded';
                statusElement.innerHTML = '<i data-lucide="check-circle-2"></i> Recorded';
            } else {
                startBtn.disabled = false;
                startBtn.classList.remove('recording');
                stopBtn.disabled = true;
                
                statusElement.className = 'question-status-badge ready';
                statusElement.innerHTML = '<i data-lucide="headphones"></i> Ready to Record';
            }

            // Reinitialize Lucide icons
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        }
    }

    startTimer(questionIndex) {
        this.timers[questionIndex] = setInterval(() => {
            const recording = this.recordings[questionIndex];
            if (recording) {
                const elapsed = Math.floor((Date.now() - recording.startTime) / 1000);
                this.updateTimerDisplay(questionIndex, elapsed);
            }
        }, 1000);
    }

    stopTimer(questionIndex) {
        if (this.timers[questionIndex]) {
            clearInterval(this.timers[questionIndex]);
            delete this.timers[questionIndex];
        }
    }

    updateTimerDisplay(questionIndex, seconds) {
        const timerElement = document.getElementById(`timer_${questionIndex}`);
        if (timerElement) {
            const mins = Math.floor(seconds / 60);
            const secs = seconds % 60;
            timerElement.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        }
    }

    createAudioPreview(questionIndex, audioBlob) {
        const previewElement = document.getElementById(`audioPreview_${questionIndex}`);
        const audioElement = document.getElementById(`audio_${questionIndex}`);
        const infoElement = document.getElementById(`audioInfo_${questionIndex}`);

        if (previewElement && audioElement && infoElement) {
            audioElement.src = URL.createObjectURL(audioBlob);
            infoElement.textContent = `Duration: ${this.formatTime(this.recordings[questionIndex].duration)} | Size: ${this.formatFileSize(audioBlob.size)}`;
            previewElement.style.display = 'block';
        }
    }

    calculateDuration(questionIndex) {
        const recording = this.recordings[questionIndex];
        if (recording && recording.startTime) {
            return Math.floor((Date.now() - recording.startTime) / 1000);
        }
        return 0;
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
        return 'audio/webm';
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

    getAllRecordings() {
        const recordings = {};
        Object.keys(this.recordings).forEach(index => {
            if (this.recordings[index].audioBlob) {
                recordings[index] = this.recordings[index];
            }
        });
        return recordings;
    }

    hasAllRecordings(questionCount) {
        return Object.keys(this.getAllRecordings()).length === questionCount;
    }

    clearRecordings() {
        Object.keys(this.recordings).forEach(index => {
            this.stopTimer(index);
            this.updateUI(index, 'ready');
        });
        this.recordings = {};
        this.currentRecordingIndex = null;
    }

    dispatchEvent(eventName, detail) {
        document.dispatchEvent(new CustomEvent(eventName, { detail }));
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.voiceRecorder = new VoiceRecorder();
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VoiceRecorder;
} 