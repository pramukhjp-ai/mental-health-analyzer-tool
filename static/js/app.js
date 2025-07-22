// Enhanced Mental Health Analyzer - Premium UI JavaScript
class MindScopeAnalyzer {
    constructor() {
        this.questions = [];
        this.results = {
            text: null,
            voice: null,
            facial: null
        };
        this.init();
    }

    init() {
        // Store instance globally for access from other components
        window.analyzer = this;
        
        // Load questions
        this.loadQuestions().then(() => {
            // Setup event listeners
            this.setupEventListeners();
            
            // Initialize animations
            this.initializeAnimations();
        });
    }

    setupEventListeners() {
        // Store reference to 'this' for use in event handlers
        const self = this;
        
        // Text form submission
        document.getElementById('textForm')?.addEventListener('submit', function(e) {
            e.preventDefault();
            self.analyzeText();
        });

        // Voice form submission
        document.getElementById('voiceForm')?.addEventListener('submit', function(e) {
            e.preventDefault();
            self.analyzeVoice();
        });

        // Facial analysis button click
        document.getElementById('analyzeFacialBtn')?.addEventListener('click', (e) => {
            console.log("Analyze Facial button clicked");
            e.preventDefault();
            this.analyzeFacial();
        });

        // Combined analysis
        document.getElementById('generateReportBtn')?.addEventListener('click', function() {
            self.generateCombinedAnalysis();
        });

        // Tab change handlers
        document.querySelectorAll('[data-bs-toggle="tab"]').forEach(tab => {
            tab.addEventListener('shown.bs.tab', function(e) {
                self.handleTabChange(e.target.getAttribute('data-bs-target'));
            });
        });

        // Setup individual question recording controls after questions are rendered
        this.setupQuestionRecordingControls();
    }

    setupQuestionRecordingControls() {
        // Setup recording controls for each question
        this.questions.forEach((question, index) => {
            const startBtn = document.getElementById(`startRecord_${index}`);
            const stopBtn = document.getElementById(`stopRecord_${index}`);
            
            if (startBtn && stopBtn) {
                startBtn.addEventListener('click', () => {
                    document.dispatchEvent(new CustomEvent('questionRecording:start', { 
                        detail: { questionIndex: index } 
                    }));
                });
                stopBtn.addEventListener('click', () => {
                    document.dispatchEvent(new CustomEvent('questionRecording:stop', { 
                        detail: { questionIndex: index } 
                    }));
                });
            }
        });

        // Listen for recording events
        document.addEventListener('recordingCompleted', (e) => {
            this.checkAllQuestionsRecorded();
        });

        document.addEventListener('recordingError', (e) => {
            this.showError(`Recording error for question ${e.detail.questionIndex + 1}: ${e.detail.error}`);
        });
    }

    initializeAnimations() {
        // Initialize Lucide icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }

        // Add intersection observer for animations
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('.question-card, .metric-card').forEach(el => {
            observer.observe(el);
        });
    }

    handleTabChange(target) {
        const targetPane = document.querySelector(target);
        if (targetPane) {
            targetPane.classList.add('slide-in');
            
            // Reload questions for the active tab
            this.loadQuestionsForTab(target);
            
            // Initialize video recorder if facial tab is selected
            if (target === '#facial' && !window.videoRecorder) {
                console.log('Initializing VideoRecorder for facial tab');
                window.videoRecorder = new VideoRecorder();
                this.setupVideoRecordingControls();
            }
            
            // FOR DEMO: Enable facial analyze button when facial tab is selected
            if (target === '#facial') {
                setTimeout(() => {
                    const analyzeBtn = document.getElementById('analyzeFacialBtn');
                    if (analyzeBtn) {
                        analyzeBtn.disabled = false;
                        analyzeBtn.style.opacity = '1';
                        analyzeBtn.style.cursor = 'pointer';
                        console.log("Facial analyze button enabled for demo (tab change)");
                    }
                }, 100);
            }
            
            // Reinitialize Lucide icons
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        }
    }

    async loadQuestions() {
        try {
            this.showLoading('Loading questions...');
            const response = await fetch('/get_questions');
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Handle both direct questions array and wrapped format
            if (data.questions) {
                this.questions = data.questions;
            } else if (Array.isArray(data)) {
                this.questions = data;
            } else {
                throw new Error('Invalid questions format received');
            }
            
            if (this.questions && this.questions.length > 0) {
                this.renderQuestions();
                this.showSuccess('Questions loaded successfully!');
            } else {
                throw new Error('No questions found');
            }
            
            return this.questions;
        } catch (error) {
            console.error('Error loading questions:', error);
            this.showError('Failed to load questions: ' + error.message);
            
            // Load fallback questions
            this.questions = [
                "How was your day today?",
                "Have you been feeling anxious or overwhelmed lately?",
                "Can you share something that made you smile recently?",
                "How are your sleeping patterns lately?",
                "Do you often feel tired or restless?"
            ];
            this.renderQuestions();
            
            return this.questions;
        } finally {
            this.hideLoading();
        }
    }

    loadQuestionsForTab(target) {
        if (this.questions.length > 0) {
            this.renderQuestions();
        }
    }

    renderQuestions() {
        // Render questions for text analysis
        const textContainer = document.getElementById('textQuestions');
        if (textContainer) {
            textContainer.innerHTML = this.questions.map((q, index) => this.createQuestionHTML(q, index, 'text')).join('');
        }

        // Render questions for voice analysis
        const voiceContainer = document.getElementById('voiceQuestions');
        if (voiceContainer) {
            voiceContainer.innerHTML = this.questions.map((q, index) => this.createQuestionHTML(q, index, 'voice')).join('');
            // Setup recording controls after rendering
            this.setupQuestionRecordingControls();
        }

        // Render questions for facial analysis
        const facialContainer = document.getElementById('facialQuestions');
        if (facialContainer) {
            facialContainer.innerHTML = this.questions.map((q, index) => this.createQuestionHTML(q, index, 'facial')).join('');
            // Setup video recording controls after rendering
            this.setupVideoRecordingControls();
        }

        // Add animation to question cards
        setTimeout(() => {
            document.querySelectorAll('.question-card').forEach((card, index) => {
                setTimeout(() => {
                    card.classList.add('slide-in');
                }, index * 100);
            });
        }, 100);

        // Reinitialize Lucide icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }

    createQuestionHTML(question, index, type) {
        const isTextType = type === 'text';
        const isVoiceType = type === 'voice';
        const isFacialType = type === 'facial';
        
        let inputElement;
        
        if (isTextType) {
            inputElement = `<textarea class="form-control" name="question_${index}" placeholder="Please share your thoughts..." rows="4" required></textarea>`;
        } else if (isVoiceType) {
            inputElement = `
                <div class="question-recording-controls">
                    <button type="button" class="question-record-btn start" id="startRecord_${index}" data-question="${index}">
                        <i data-lucide="mic"></i>
                    </button>
                    <button type="button" class="question-record-btn stop" id="stopRecord_${index}" data-question="${index}" disabled>
                        <i data-lucide="stop-circle"></i>
                    </button>
                    <div class="question-status">
                        <div class="question-status-badge ready" id="status_${index}">
                            <i data-lucide="headphones"></i>
                            Ready to Record
                        </div>
                        <div class="question-timer" id="timer_${index}">00:00</div>
                    </div>
                </div>
                <div class="question-audio-preview" id="audioPreview_${index}" style="display: none;">
                    <audio controls id="audio_${index}" style="width: 100%; border-radius: 12px; background: rgba(255, 255, 255, 0.9);">
                        Your browser does not support the audio element.
                    </audio>
                    <div class="question-audio-info" id="audioInfo_${index}"></div>
                </div>
            `;
        } else if (isFacialType) {
            inputElement = `
                <div class="question-video-controls">
                    <button type="button" class="question-video-btn start" id="startVideoRecord_${index}" data-question="${index}">
                        <i data-lucide="play-circle"></i>
                    </button>
                    <button type="button" class="question-video-btn stop" id="stopVideoRecord_${index}" data-question="${index}" disabled>
                        <i data-lucide="stop-circle"></i>
                    </button>
                    <div class="question-status">
                        <div class="question-status-badge ready" id="videoStatus_${index}">
                            <i data-lucide="camera"></i>
                            Ready to Record
                        </div>
                        <div class="question-timer" id="videoTimer_${index}">00:00</div>
                    </div>
                </div>
                <div class="question-video-preview" id="videoPreview_${index}" style="display: none;">
                    <video controls id="video_${index}" style="width: 100%; max-width: 300px; border-radius: 12px; border: 2px solid rgba(102, 126, 234, 0.2);">
                        Your browser does not support the video element.
                    </video>
                    <div class="question-video-info" id="videoInfo_${index}"></div>
                </div>
                <div class="question-upload-fallback mt-2">
                    <small style="color: #7f8c8d; font-weight: 500;">Or upload a video file:</small>
                    <input type="file" id="videoFile_${index}" accept="video/*" style="display: none;" data-question="${index}">
                    <button type="button" class="btn btn-sm" style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; border-radius: 20px; padding: 0.5rem 1rem; font-weight: 600;" onclick="document.getElementById('videoFile_${index}').click()">
                        <i data-lucide="upload-cloud"></i>
                        Upload Video
                    </button>
                </div>
            `;
        } else {
            inputElement = `<p class="text-muted mb-0" style="font-size: 0.9rem;">Record your response or upload a file to answer this question.</p>`;
        }

        return `
            <div class="question-card" style="animation-delay: ${index * 0.1}s;">
                <div class="question-number">${index + 1}</div>
                <div class="question-text">${question}</div>
                ${inputElement}
            </div>
        `;
    }

    async analyzeText() {
        try {
            this.showLoading('Analyzing your text responses...');
            
            const responses = [];
            
            // Collect answers from text areas
            const textareas = document.querySelectorAll('#textQuestions textarea');
            textareas.forEach((textarea, index) => {
                if (textarea.value.trim()) {
                    responses.push(textarea.value.trim());
                }
            });

            if (responses.length === 0) {
                this.showError('Please answer at least one question');
                return;
            }

            const response = await fetch('/analyze_text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ responses: responses })
            });

            const result = await response.json();
            
            if (result.success) {
                this.results.text = result.analysis;
                this.displayTextResults(result.analysis);
                this.updateCombinedScores();
                this.showSuccess('Text analysis completed successfully!');
            } else {
                this.showError('Text analysis failed: ' + (result.error || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error analyzing text:', error);
            this.showError('Error analyzing text responses');
        } finally {
            this.hideLoading();
        }
    }

    checkAllQuestionsRecorded() {
        const allRecorded = window.voiceRecorder?.hasAllRecordings(this.questions.length);

        const analyzeBtn = document.getElementById('analyzeVoiceBtn');
        if (analyzeBtn) {
            analyzeBtn.disabled = !allRecorded;
        }
    }

    async analyzeVoice() {
        try {
            if (!window.voiceRecorder?.hasAllRecordings(this.questions.length)) {
                this.showError('Please record responses for all questions first');
                return;
            }

            this.showLoading('Analyzing your voice patterns...');
            
            const formData = new FormData();
            const recordings = window.voiceRecorder.getAllRecordings();
            
            // Add all question recordings
            Object.keys(recordings).forEach(index => {
                const recording = recordings[index];
                if (recording.audioBlob) {
                    formData.append(`audio_${index}`, recording.audioBlob, `question_${index}.wav`);
                }
            });

            const response = await fetch('/analyze_voice', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            
            if (result.success) {
                this.results.voice = result.overall_analysis;
                this.displayVoiceResults(result);
                this.updateCombinedScores();
                this.showSuccess('Voice analysis completed successfully!');
            } else {
                this.showError('Voice analysis failed: ' + (result.error || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error analyzing voice:', error);
            this.showError('Error analyzing voice recording');
        } finally {
            this.hideLoading();
        }
    }

    async analyzeFacial() {
        try {
            console.log("analyzeFacial method called - using mock data for demo");
            
            // FOR DEMO: Always allow analysis with mock data
            this.showLoading('Analyzing your facial expressions...');
            
            // Mock facial analysis result for demo
            const mockResult = {
                "success": true,
                "question_analyses": {
                    "0": {
                        "primary_emotion": "happy",
                        "confidence": 0.82,
                        "emotion_scores": {
                            "happy": 0.82,
                            "neutral": 0.15,
                            "surprised": 0.03
                        },
                        "features_summary": {
                            "average_face_width": 120,
                            "average_face_height": 145,
                            "average_mean_brightness": 128,
                            "face_detection_rate": 0.95
                        },
                        "recommendations": ["Great! Your facial expression shows positive emotions", "Continue with activities that bring you joy"],
                        "emotion_score": 0.574
                    },
                    "1": {
                        "primary_emotion": "neutral",
                        "confidence": 0.75,
                        "emotion_scores": {
                            "neutral": 0.75,
                            "happy": 0.20,
                            "sad": 0.05
                        },
                        "features_summary": {
                            "average_face_width": 118,
                            "average_face_height": 142,
                            "average_mean_brightness": 125,
                            "face_detection_rate": 0.88
                        },
                        "recommendations": ["Your expression appears calm and balanced"],
                        "emotion_score": 0.0
                    },
                    "2": {
                        "primary_emotion": "happy",
                        "confidence": 0.78,
                        "emotion_scores": {
                            "happy": 0.78,
                            "neutral": 0.18,
                            "surprised": 0.04
                        },
                        "features_summary": {
                            "average_face_width": 122,
                            "average_face_height": 148,
                            "average_mean_brightness": 130,
                            "face_detection_rate": 0.92
                        },
                        "recommendations": ["Positive facial expressions detected", "Keep engaging with uplifting content"],
                        "emotion_score": 0.546
                    },
                    "3": {
                        "primary_emotion": "neutral",
                        "confidence": 0.73,
                        "emotion_scores": {
                            "neutral": 0.73,
                            "happy": 0.22,
                            "thoughtful": 0.05
                        },
                        "features_summary": {
                            "average_face_width": 119,
                            "average_face_height": 144,
                            "average_mean_brightness": 127,
                            "face_detection_rate": 0.90
                        },
                        "recommendations": ["Balanced emotional expression observed"],
                        "emotion_score": 0.0
                    },
                    "4": {
                        "primary_emotion": "happy",
                        "confidence": 0.85,
                        "emotion_scores": {
                            "happy": 0.85,
                            "neutral": 0.12,
                            "excited": 0.03
                        },
                        "features_summary": {
                            "average_face_width": 125,
                            "average_face_height": 150,
                            "average_mean_brightness": 132,
                            "face_detection_rate": 0.97
                        },
                        "recommendations": ["Excellent! Strong positive emotions detected", "Your facial expressions indicate good mental wellness"],
                        "emotion_score": 0.595
                    }
                },
                "overall_analysis": {
                    "emotions": ["happy", "neutral", "happy", "neutral", "happy"],
                    "confidence_scores": [0.82, 0.75, 0.78, 0.73, 0.85],
                    "emotion_scores": [0.574, 0.0, 0.546, 0.0, 0.595],
                    "facial_features": {
                        "average_detection_rate": 0.924,
                        "average_brightness": 128.4,
                        "expression_consistency": "stable"
                    },
                    "recommendations": [
                        "Overall facial analysis shows predominantly positive emotions",
                        "Good facial expression variety indicates emotional responsiveness",
                        "Continue maintaining activities that promote positive emotions",
                        "Your facial expressions suggest good mental wellness"
                    ],
                    "overall_emotion": "happy",
                    "stress_level": "low",
                    "average_confidence": 0.786,
                    "emotion_score": 0.343
                }
            };

            // Simulate API delay for realism
            await new Promise(resolve => setTimeout(resolve, 2000));

            this.results.facial = mockResult;
            this.displayFacialResults(mockResult);
            this.updateCombinedScores();
            this.showSuccess('Facial analysis completed successfully! (Demo Data)');
            
        } catch (error) {
            console.error('Error analyzing facial expressions:', error);
            this.showError('Error analyzing facial expressions');
        } finally {
            this.hideLoading();
        }
    }

    displayTextResults(result) {
        const container = document.getElementById('textResults');
        if (!container) return;

        const html = `
            <div class="fade-in">
                <h6 class="text-white mb-3">
                    <i data-lucide="bar-chart-3"></i>
                    Text Analysis Results
                </h6>
                
                <div class="metric-card mb-3">
                    <div class="metric-value">${this.formatScore(result.overall_sentiment_score)}</div>
                    <div class="metric-label">Overall Sentiment</div>
                </div>

                <div class="metric-card mb-3">
                    <div class="metric-value">${result.primary_emotion || 'N/A'}</div>
                    <div class="metric-label">Primary Emotion</div>
                </div>

                <div class="metric-card mb-3">
                    <div class="metric-value">${this.formatScore(result.confidence)}</div>
                    <div class="metric-label">Confidence</div>
                </div>

                <div class="status-badge ${this.getStatusClass(result.overall_mood)} mb-3">
                    <i data-lucide="brain"></i>
                    ${result.overall_mood || 'Neutral'}
                </div>

                ${result.recommendations && result.recommendations.length > 0 ? `
                    <div class="mt-3">
                        <h6 class="text-white mb-2">
                            <i data-lucide="lightbulb"></i>
                            Recommendations
                        </h6>
                        ${result.recommendations.map(rec => `
                            <div class="text-muted mb-2" style="font-size: 0.9rem;">• ${rec}</div>
                        `).join('')}
                    </div>
                ` : ''}

                ${result.sentiment_breakdown ? `
                    <div class="mt-3">
                        <h6 class="text-white mb-2">
                            <i data-lucide="pie-chart"></i>
                            Sentiment Breakdown
                        </h6>
                        <div class="text-muted" style="font-size: 0.85rem;">
                            <div>Positive: ${this.formatScore(result.sentiment_breakdown.positive)}</div>
                            <div>Negative: ${this.formatScore(result.sentiment_breakdown.negative)}</div>
                            <div>Neutral: ${this.formatScore(result.sentiment_breakdown.neutral)}</div>
                        </div>
                    </div>
                ` : ''}
            </div>
        `;

        container.innerHTML = html;
        
        // Reinitialize icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }

    displayVoiceResults(result) {
        const container = document.getElementById('voiceResults');
        if (!container) return;

        const overallAnalysis = result.overall_analysis;
        const questionAnalyses = result.question_analyses;

        const html = `
            <div class="fade-in">
                <h6 class="text-white mb-3">
                    <i data-lucide="activity"></i>
                    Comprehensive Voice Analysis
                </h6>
                
                <div class="metric-card mb-3">
                    <div class="metric-value">${overallAnalysis.dominant_emotion || 'N/A'}</div>
                    <div class="metric-label">Dominant Emotion</div>
                </div>

                <div class="metric-card mb-3">
                    <div class="metric-value">${this.formatScore(overallAnalysis.average_confidence)}</div>
                    <div class="metric-label">Average Confidence</div>
                </div>

                <div class="status-badge ${this.getStatusClass(overallAnalysis.overall_mood)} mb-3">
                    <i data-lucide="brain"></i>
                    ${overallAnalysis.overall_mood || 'Neutral'} Mood
                </div>

                <div class="status-badge ${this.getStressLevelClass(overallAnalysis.stress_level)} mb-3">
                    <i data-lucide="activity"></i>
                    ${overallAnalysis.stress_level || 'Low'} Stress Level
                </div>

                ${overallAnalysis.comprehensive_recommendations && overallAnalysis.comprehensive_recommendations.length > 0 ? `
                    <div class="mt-3">
                        <h6 class="text-white mb-2">
                            <i data-lucide="lightbulb"></i>
                            Recommendations
                        </h6>
                        ${overallAnalysis.comprehensive_recommendations.slice(0, 5).map(rec => `
                            <div class="text-muted mb-2" style="font-size: 0.9rem;">• ${rec}</div>
                        `).join('')}
                        ${overallAnalysis.comprehensive_recommendations.length > 5 ? `
                            <div class="text-muted" style="font-size: 0.85rem;">+ ${overallAnalysis.comprehensive_recommendations.length - 5} more recommendations</div>
                        ` : ''}
                    </div>
                ` : ''}

                ${overallAnalysis.emotion_distribution ? `
                    <div class="mt-3">
                        <h6 class="text-white mb-2">
                            <i data-lucide="pie-chart"></i>
                            Emotion Distribution
                        </h6>
                        <div class="text-muted" style="font-size: 0.85rem;">
                            ${Object.entries(overallAnalysis.emotion_distribution).map(([emotion, count]) => 
                                `<div>${emotion.charAt(0).toUpperCase() + emotion.slice(1)}: ${count} response${count > 1 ? 's' : ''}</div>`
                            ).join('')}
                        </div>
                    </div>
                ` : ''}

                <div class="mt-3">
                    <h6 class="text-white mb-2">
                        <i data-lucide="check-circle"></i>
                        Analysis Summary
                    </h6>
                    <div class="text-muted" style="font-size: 0.85rem;">
                        <div>Questions Analyzed: ${overallAnalysis.questions_analyzed || Object.keys(questionAnalyses || {}).length}</div>
                        <div>Overall Assessment: ${overallAnalysis.overall_mood || 'neutral'} mood with ${overallAnalysis.stress_level || 'low'} stress</div>
                    </div>
                </div>
            </div>
        `;

        container.innerHTML = html;
        
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }

    displayFacialResults(result) {
        const container = document.getElementById('facialResults');
        if (!container) return;

        // Handle multiple question analyses
        let html = `
            <div class="fade-in">
                <h6 class="text-white mb-3">
                    <i data-lucide="bar-chart-3"></i>
                    Facial Analysis Results
                </h6>
                
                <div class="metric-card mb-3">
                    <div class="metric-value">${result.overall_analysis.overall_emotion}</div>
                    <div class="metric-label">Overall Emotion</div>
                </div>

                <div class="metric-card mb-3">
                    <div class="metric-value">${this.formatScore(result.overall_analysis.average_confidence)}</div>
                    <div class="metric-label">Average Confidence</div>
                </div>

                <div class="metric-card mb-3">
                    <div class="metric-value">${result.overall_analysis.stress_level}</div>
                    <div class="metric-label">Stress Level</div>
                </div>

                ${result.overall_analysis.recommendations && result.overall_analysis.recommendations.length > 0 ? `
                    <div class="mt-3">
                        <h6 class="text-white mb-2">
                            <i data-lucide="lightbulb"></i>
                            Recommendations
                        </h6>
                        ${result.overall_analysis.recommendations.map(rec => `
                            <div class="text-muted mb-2" style="font-size: 0.9rem;">• ${rec}</div>
                        `).join('')}
                    </div>
                ` : ''}

                <div class="mt-4">
                    <h6 class="text-white mb-2">
                        <i data-lucide="list"></i>
                        Per Question Analysis
                    </h6>
                    ${Object.keys(result.question_analyses).map(index => {
                        const qResult = result.question_analyses[index];
                        return `
                            <div class="question-result-card">
                                <div class="question-number">Q${parseInt(index) + 1}</div>
                                <div class="status-badge ${this.getStatusClass(qResult.primary_emotion)}">
                                    ${qResult.primary_emotion}
                                </div>
                                <small class="text-muted">Confidence: ${this.formatScore(qResult.confidence)}</small>
                            </div>
                        `;
                    }).join('')}
                </div>
            </div>
        `;

        container.innerHTML = html;
        lucide.createIcons();
    }

    updateCombinedScores() {
        // Update individual score displays
        const textScore = document.getElementById('combinedTextScore');
        const voiceScore = document.getElementById('combinedVoiceScore');
        const facialScore = document.getElementById('combinedFacialScore');

        if (textScore) {
            textScore.textContent = this.results.text ? 
                this.formatScore(this.results.text.confidence) : '--';
        }
        
        if (voiceScore) {
            voiceScore.textContent = this.results.voice ? 
                this.formatScore(this.results.voice.average_confidence) : '--';
        }
        
        if (facialScore) {
            facialScore.textContent = this.results.facial ? 
                this.formatScore(this.results.facial.confidence) : '--';
        }

        // Update combined chart if we have data
        if (this.hasAnyResults()) {
            this.updateCombinedChart();
        }
    }

    updateCombinedChart() {
        const canvas = document.getElementById('combinedChart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        
        // Destroy existing chart if it exists and has destroy method
        if (window.combinedChart && typeof window.combinedChart.destroy === 'function') {
            try {
                window.combinedChart.destroy();
            } catch (error) {
                console.warn('Error destroying existing chart:', error);
            }
        }
        
        // Clear the chart reference
        window.combinedChart = null;

        const data = {
            labels: ['Text Analysis', 'Voice Analysis', 'Facial Analysis'],
            datasets: [{
                label: 'Analysis Scores',
                data: [
                    this.results.text?.overall_sentiment_score || 0,
                    this.results.voice?.average_confidence || 0,
                    this.results.facial?.confidence || 0
                ],
                backgroundColor: [
                    'rgba(102, 126, 234, 0.8)',
                    'rgba(79, 172, 254, 0.8)',
                    'rgba(240, 147, 251, 0.8)'
                ],
                borderColor: [
                    'rgba(102, 126, 234, 1)',
                    'rgba(79, 172, 254, 1)',
                    'rgba(240, 147, 251, 1)'
                ],
                borderWidth: 2
            }]
        };

        const options = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: 'white'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1,
                    ticks: {
                        color: 'white'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                x: {
                    ticks: {
                        color: 'white'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                }
            }
        };

        // Check if Chart.js is available before creating the chart
        if (typeof Chart !== 'undefined') {
            try {
                window.combinedChart = new Chart(ctx, {
                    type: 'bar',
                    data: data,
                    options: options
                });
            } catch (error) {
                console.error('Error creating chart:', error);
                this.showError('Chart library not properly loaded. Please refresh the page.');
            }
        } else {
            console.error('Chart.js library not found');
            this.showError('Chart library not loaded. Please check your internet connection and refresh.');
        }
    }

    async generateCombinedAnalysis() {
        if (!this.hasAnyResults()) {
            this.showError('Please complete at least one analysis first');
            return;
        }

        try {
            this.showLoading('Generating comprehensive report...');
            
            const response = await fetch('/combined_analysis', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text_result: this.results.text,
                    voice_result: this.results.voice,
                    facial_result: this.results.facial
                })
            });

            const result = await response.json();
            
            if (result.success) {
                this.displayCombinedResults(result);
                this.showSuccess('Comprehensive analysis completed!');
            } else {
                this.showError('Combined analysis failed: ' + (result.error || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error generating combined analysis:', error);
            this.showError('Error generating combined analysis');
        } finally {
            this.hideLoading();
        }
    }

    displayCombinedResults(result) {
        // Implementation for displaying combined results
        console.log('Combined results:', result);
        this.showSuccess('Combined analysis report generated successfully!');
    }

    hasAnyResults() {
        return this.results.text || this.results.voice || this.results.facial;
    }

    formatScore(score) {
        if (score === null || score === undefined) return 'N/A';
        return typeof score === 'number' ? (score * 100).toFixed(0) + '%' : score;
    }

    getStatusClass(emotion) {
        if (!emotion) return 'neutral';
        
        const positive = ['happy', 'joy', 'positive', 'content', 'excited'];
        const negative = ['sad', 'angry', 'fear', 'negative', 'anxious', 'stressed'];
        
        const emotionLower = emotion.toLowerCase();
        
        if (positive.some(p => emotionLower.includes(p))) return 'positive';
        if (negative.some(n => emotionLower.includes(n))) return 'negative';
        
        return 'neutral';
    }

    getStressLevelClass(stressLevel) {
        if (!stressLevel) return 'neutral';
        
        const stressLower = stressLevel.toLowerCase();
        
        if (stressLower === 'high') return 'negative';
        if (stressLower === 'medium') return 'neutral';
        if (stressLower === 'low') return 'positive';
        
        return 'neutral';
    }

    showLoading(message = 'Processing...') {
        const overlay = document.getElementById('loadingOverlay');
        const text = document.getElementById('loadingText');
        
        if (overlay && text) {
            text.textContent = message;
            overlay.style.display = 'flex';
        }
    }

    hideLoading() {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.style.display = 'none';
        }
    }

    showSuccess(message) {
        this.showNotification(message, 'success');
    }

    showError(message) {
        this.showNotification(message, 'error');
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
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOutToRight 0.3s ease-in';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 5000);
    }
}

// New VideoRecorder class for facial analysis
class VideoRecorder {
    constructor() {
        this.recordings = {};
        this.mediaRecorders = {};
        this.timers = {};
        this.streams = {};
    }

    // Add showError method
    showError(message) {
        console.error('VideoRecorder error:', message);
        // If analyzer instance is available, use its showError method
        if (window.analyzer && typeof window.analyzer.showError === 'function') {
            window.analyzer.showError(message);
        } else {
            // Fallback to alert
            alert('Error: ' + message);
        }
    }

    async startRecording(index, statusBadge, timer, preview, element, info) {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
            this.streams[index] = stream;
            element.srcObject = stream;
            element.play();
            preview.style.display = 'block';
            
            const recorder = new MediaRecorder(stream);
            recorder.ondataavailable = (e) => {
                if (e.data.size > 0) {
                    if (!this.recordings[index]) this.recordings[index] = [];
                    this.recordings[index].push(e.data);
                }
            };
            recorder.onstop = () => {
                const blob = new Blob(this.recordings[index], { type: 'video/webm' });
                this.recordings[index] = { blob, url: URL.createObjectURL(blob) };
                element.srcObject = null;
                element.src = this.recordings[index].url;
                element.load();
                info.innerHTML = `Duration: ${this.formatTime(this.timers[index].duration)} | Size: ${(blob.size / 1024).toFixed(1)} KB`;
            };
            recorder.start();
            this.mediaRecorders[index] = recorder;
            
            statusBadge.className = 'question-status-badge recording';
            statusBadge.innerHTML = '<i data-lucide="record-circle"></i> Recording';
            lucide.createIcons();
            
            this.timers[index] = { start: Date.now(), duration: 0, interval: setInterval(() => {
                this.timers[index].duration = Date.now() - this.timers[index].start;
                timer.innerHTML = this.formatTime(this.timers[index].duration);
            }, 1000) };
        } catch (error) {
            console.error('Error starting video recording:', error);
            this.showError('Unable to access camera. Please check permissions.');
        }
    }

    stopRecording(index, statusBadge, timer, preview, element, info) {
        if (this.mediaRecorders[index]) {
            this.mediaRecorders[index].stop();
        }
        if (this.timers[index]) {
            clearInterval(this.timers[index].interval);
            timer.innerHTML = this.formatTime(this.timers[index].duration);
        }
        if (this.streams[index]) {
            this.streams[index].getTracks().forEach(track => track.stop());
        }
        
        statusBadge.className = 'question-status-badge ready';
        statusBadge.innerHTML = '<i data-lucide="check-circle-2"></i> Recorded';
        lucide.createIcons();
    }

    formatTime(ms) {
        const seconds = Math.floor(ms / 1000);
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }

    getRecording(index) {
        return this.recordings[index] ? this.recordings[index].blob : null;
    }

    hasAllRecordings(total) {
        return Object.keys(this.recordings).length === total && Object.values(this.recordings).every(r => r.blob);
    }

    getAllRecordings() {
        return this.recordings;
    }

    handleFileUpload(index, file, statusBadge, preview, element, info) {
        const url = URL.createObjectURL(file);
        this.recordings[index] = { blob: file, url };
        element.src = url;
        preview.style.display = 'block';
        info.innerHTML = `File: ${file.name} | Size: ${(file.size / 1024).toFixed(1)} KB`;
        statusBadge.className = 'question-status-badge ready';
        statusBadge.innerHTML = '<i data-lucide="upload-cloud"></i> Uploaded';
        lucide.createIcons();
    }
}

// Add to MindScopeAnalyzer class
MindScopeAnalyzer.prototype.setupVideoRecordingControls = function() {
    console.log("Setting up video recording controls");
    if (!window.videoRecorder) {
        console.log("Creating new VideoRecorder");
        window.videoRecorder = new VideoRecorder();
    }
    
    // FOR DEMO: Enable the analyze button immediately
    const analyzeBtn = document.getElementById('analyzeFacialBtn');
    if (analyzeBtn) {
        analyzeBtn.disabled = false;
        console.log("Facial analyze button enabled for demo");
    }
    
    this.questions.forEach((q, index) => {
        const startBtn = document.getElementById(`startVideoRecord_${index}`);
        const stopBtn = document.getElementById(`stopVideoRecord_${index}`);
        const statusBadge = document.getElementById(`videoStatus_${index}`);
        const timer = document.getElementById(`videoTimer_${index}`);
        const preview = document.getElementById(`videoPreview_${index}`);
        const videoElement = document.getElementById(`video_${index}`);
        const info = document.getElementById(`videoInfo_${index}`);
        const fileInput = document.getElementById(`videoFile_${index}`);

        if (startBtn && stopBtn) {
            startBtn.addEventListener('click', () => {
                window.videoRecorder.startRecording(index, statusBadge, timer, preview, videoElement, info);
                startBtn.disabled = true;
                stopBtn.disabled = false;
            });
            
            stopBtn.addEventListener('click', () => {
                window.videoRecorder.stopRecording(index, statusBadge, timer, preview, videoElement, info);
                startBtn.disabled = false;
                stopBtn.disabled = true;
                this.checkAllVideoQuestionsRecorded();
            });
        }

        if (fileInput) {
            fileInput.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) {
                    window.videoRecorder.handleFileUpload(index, file, statusBadge, preview, videoElement, info);
                    this.checkAllVideoQuestionsRecorded();
                }
            });
        }
    });
};

MindScopeAnalyzer.prototype.checkAllVideoQuestionsRecorded = function() {
    // FOR DEMO: Always enable the facial analysis button
    const analyzeBtn = document.getElementById('analyzeFacialBtn');
    if (analyzeBtn) {
        analyzeBtn.disabled = false;
        console.log("Facial analyze button enabled for demo");
    }
};

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInFromRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutToRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Initialize the analyzer when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.mindScopeAnalyzer = new MindScopeAnalyzer();
});

// Expose some functions globally for compatibility
window.analyzeText = () => window.mindScopeAnalyzer?.analyzeText();
window.analyzeVoice = () => window.mindScopeAnalyzer?.analyzeVoice();
window.analyzeFacial = () => window.mindScopeAnalyzer?.analyzeFacial(); 