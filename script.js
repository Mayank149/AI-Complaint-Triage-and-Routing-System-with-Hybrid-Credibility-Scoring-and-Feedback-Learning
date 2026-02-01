document.addEventListener('DOMContentLoaded', () => {

    // DOM Elements
    const complaintText = document.getElementById('complaint-text');
    const charCount = document.getElementById('char-count');
    const analyzeBtn = document.getElementById('analyze-btn');
    const loadingIndicator = document.getElementById('loading-indicator');
    const errorMessage = document.getElementById('error-message');
    const resultsSection = document.getElementById('results-section');
    const feedbackSection = document.getElementById('feedback-section');
    const feedbackSuccess = document.getElementById('feedback-success');

    // Result Elements
    const deptValue = document.getElementById('dept-value');
    const deptConfidence = document.getElementById('dept-confidence');
    const urgencyValue = document.getElementById('urgency-value');
    const urgencyConfidence = document.getElementById('urgency-confidence');
    const credibilityValue = document.getElementById('credibility-value');
    const credibilityBar = document.getElementById('credibility-bar');
    const followupContainer = document.getElementById('followup-container');
    const followupList = document.getElementById('followup-list');

    // Feedback Elements
    const feedbackBtns = document.querySelectorAll('.feedback-btn');
    const deptCorrectionDiv = document.getElementById('dept-correction');
    const urgencyCorrectionDiv = document.getElementById('urgency-correction');
    const submitFeedbackBtn = document.getElementById('submit-feedback-btn');
    const correctDeptSelect = document.getElementById('correct-dept');
    const correctUrgencySelect = document.getElementById('correct-urgency');

    // State
    const MIN_CHARS = 20;
    let currentComplaintId = null;
    let currentPrediction = {};
    let feedbackState = {
        deptCorrect: null, // true/false
        urgencyCorrect: null // true/false
    };

    // --- Event Listeners ---

    // Input Validation
    complaintText.addEventListener('input', () => {
        const len = complaintText.value.length;
        charCount.textContent = `${len} characters (minimal ${MIN_CHARS} required)`;

        if (len >= MIN_CHARS) {
            analyzeBtn.disabled = false;
            charCount.style.color = 'var(--success-color)';
        } else {
            analyzeBtn.disabled = true;
            charCount.style.color = 'var(--text-secondary)';
        }
    });

    // Analyze Action
    analyzeBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        resetUI();
        loadingIndicator.classList.remove('hidden');
        analyzeBtn.disabled = true; // Prevent double click

        try {
            const text = complaintText.value;
            const response = await fetch('http://127.0.0.1:5000/analyze-complaint', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: text })
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const data = await response.json();
            displayResults(data);

        } catch (error) {
            console.error('Error:', error);
            showError('Failed to analyze complaint. Is the server running?');
        } finally {
            loadingIndicator.classList.add('hidden');
            analyzeBtn.disabled = false;
        }
    });

    // Feedback Buttons Logic
    feedbackBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const type = btn.dataset.type; // 'dept' or 'urgency'
            const value = btn.dataset.value; // 'yes' or 'no'
            const isCorrect = value === 'yes';

            // Visual Selection
            // Remove selected from siblings
            btn.parentElement.querySelectorAll('.btn').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');

            // Logic
            if (type === 'dept') {
                feedbackState.deptCorrect = isCorrect;
                toggleCorrection(deptCorrectionDiv, !isCorrect);
            } else if (type === 'urgency') {
                feedbackState.urgencyCorrect = isCorrect;
                toggleCorrection(urgencyCorrectionDiv, !isCorrect);
            }

            checkFeedbackReady();
        });
    });

    // Submit Feedback Action
    submitFeedbackBtn.addEventListener('click', async () => {
        if (!currentComplaintId) return;

        const payload = {
            complaint_id: currentComplaintId,
            predicted_department: currentPrediction.department,
            predicted_urgency: currentPrediction.urgency,
            correct_department: feedbackState.deptCorrect ? currentPrediction.department : correctDeptSelect.value,
            correct_urgency: feedbackState.urgencyCorrect ? currentPrediction.urgency : correctUrgencySelect.value
        };

        // Validate payload
        if ((!feedbackState.deptCorrect && !payload.correct_department) ||
            (!feedbackState.urgencyCorrect && !payload.correct_urgency)) {
            showError("Please select the correct values for any incorrect predictions.");
            return;
        }

        submitFeedbackBtn.disabled = true;
        submitFeedbackBtn.textContent = 'Submitting...';

        try {
            const response = await fetch('http://127.0.0.1:5000/feedback', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                // Lock the input parts (disable buttons and select)
                feedbackBtns.forEach(btn => btn.disabled = true);
                correctDeptSelect.disabled = true;
                correctUrgencySelect.disabled = true;

                // Hide the submit button
                submitFeedbackBtn.parentElement.classList.add('hidden');

                // Show success
                feedbackSuccess.classList.remove('hidden');
                feedbackSuccess.textContent = "Thanks for the feedback";

            } else {
                showError("Failed to submit feedback.");
            }
        } catch (e) {
            showError("Error submitting feedback.");
        }
    });


    // --- Helper Functions ---

    function displayResults(data) {
        currentComplaintId = data.complaint_id;
        currentPrediction = data;

        // Populate Cards
        deptValue.textContent = data.department;
        // Handle confidence format (might be 0-1 or 0-100)
        const dConf = data.department_confidence > 1 ? data.department_confidence : (data.department_confidence * 100).toFixed(1);
        deptConfidence.textContent = dConf;

        urgencyValue.textContent = data.urgency;
        const uConf = data.urgency_confidence > 1 ? data.urgency_confidence : (data.urgency_confidence * 100).toFixed(1);
        urgencyConfidence.textContent = uConf;

        credibilityValue.textContent = data.credibility_score;
        credibilityBar.style.width = `${data.credibility_score}%`;

        // Color code credibility bar
        if (data.credibility_score < 40) credibilityBar.style.backgroundColor = '#C62828'; // Red
        else if (data.credibility_score < 70) credibilityBar.style.backgroundColor = '#FBC02D'; // Yellow
        else credibilityBar.style.backgroundColor = '#2E7D32'; // Green

        // Follow-up Questions
        if (data.followup_questions && data.followup_questions.length > 0) {
            followupList.innerHTML = '';
            data.followup_questions.forEach(q => {
                const li = document.createElement('li');
                li.textContent = q;
                followupList.appendChild(li);
            });
            followupContainer.classList.remove('hidden');
        } else {
            followupContainer.classList.add('hidden');
        }

        // Show Sections
        resultsSection.classList.remove('hidden');
        feedbackSection.classList.remove('hidden');

        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    function resetUI() {
        errorMessage.classList.add('hidden');
        errorMessage.textContent = '';
        resultsSection.classList.add('hidden');
        feedbackSection.classList.add('hidden');
        feedbackSuccess.classList.add('hidden');

        // Restore feedback section visibility for next run
        // We no longer hide them, but we need to ensure they are enabled
        correctDeptSelect.disabled = false;
        correctUrgencySelect.disabled = false;
        submitFeedbackBtn.parentElement.classList.remove('hidden');

        // Reset feedback state
        feedbackState = { deptCorrect: null, urgencyCorrect: null };
        feedbackBtns.forEach(btn => {
            btn.classList.remove('selected');
            btn.disabled = false;
        });
        deptCorrectionDiv.classList.add('hidden');
        urgencyCorrectionDiv.classList.add('hidden');
        correctDeptSelect.value = "";
        correctUrgencySelect.value = "";
        submitFeedbackBtn.disabled = true;
        submitFeedbackBtn.textContent = 'Submit Feedback';
    }

    function toggleCorrection(element, show) {
        if (show) element.classList.remove('hidden');
        else element.classList.add('hidden');
    }

    function checkFeedbackReady() {
        const deptDone = feedbackState.deptCorrect !== null;
        const urgencyDone = feedbackState.urgencyCorrect !== null;

        if (deptDone && urgencyDone) {
            submitFeedbackBtn.disabled = false;
        } else {
            submitFeedbackBtn.disabled = true;
        }
    }

    function showError(msg) {
        errorMessage.textContent = msg;
        errorMessage.classList.remove('hidden');
    }
});
