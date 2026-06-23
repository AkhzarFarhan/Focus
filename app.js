// Application State
let activeView = 'concepts'; // 'concepts' | 'patterns'
let conceptsData = null;
let patternsData = null;
let activeChapterId = null; // null means dashboard
let activeTab = 'learn'; // 'learn' | 'problems' | 'quiz'
let searchQuery = '';

// Local Storage Progress Structure
let userProgress = {
    completedTopics: [],   // list of topic IDs (e.g. "1.1")
    completedProblems: [], // list of problem IDs (e.g. "p1.1")
    completedChapters: [], // list of unique keys e.g. "concepts_1", "patterns_2"
    quizScores: {}         // key (concepts_1) -> { score, total }
};

// Initialize App
document.addEventListener('DOMContentLoaded', async () => {
    loadProgress();
    await fetchData();
    initUI();
    updateOverallProgress();
    showDashboard();
});

// Load Progress from LocalStorage
function loadProgress() {
    const saved = localStorage.getItem('samsung_prep_progress');
    if (saved) {
        try {
            userProgress = JSON.parse(saved);
            // Ensure properties exist
            if (!userProgress.completedTopics) userProgress.completedTopics = [];
            if (!userProgress.completedProblems) userProgress.completedProblems = [];
            if (!userProgress.completedChapters) userProgress.completedChapters = [];
            if (!userProgress.quizScores) userProgress.quizScores = {};
        } catch (e) {
            console.error("Error parsing progress from local storage", e);
        }
    }
}

// Save Progress to LocalStorage
function saveProgress() {
    localStorage.setItem('samsung_prep_progress', JSON.stringify(userProgress));
    updateOverallProgress();
    showToast("Progress saved automatically!");
}

// Fetch JSON Knowledgebase Files
async function fetchData() {
    try {
        const conceptsRes = await fetch('cpp_concepts.json');
        conceptsData = await conceptsRes.json();
        
        const patternsRes = await fetch('interview_patterns.json');
        patternsData = await patternsRes.json();
    } catch (error) {
        console.error("Error loading knowledgebase data", error);
        showToast("Error loading preparation data. Check console.", "error");
    }
}

// Initialize Global UI Event Listeners
function initUI() {
    // Configure marked parser
    if (typeof marked !== 'undefined') {
        marked.use({
            gfm: true,
            breaks: true,
            headerIds: false,
            mangle: false
        });
    }

    // Initialize Lucide Icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
    
    // Bind search Enter key
    document.getElementById('global-search').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSearch(e.target.value);
        }
    });
}

// Show Toast Alert Notification
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast-notification');
    const msgSpan = document.getElementById('toast-message');
    msgSpan.textContent = message;
    
    if (type === 'error') {
        toast.style.borderColor = 'var(--accent-rose)';
        toast.style.borderLeftColor = 'var(--accent-rose)';
    } else {
        toast.style.borderColor = 'var(--accent-indigo)';
        toast.style.borderLeftColor = 'var(--accent-indigo)';
    }
    
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 2500);
}

// Switch between C++ Concepts and Coding Patterns views
function switchView(view) {
    if (view === activeView && activeChapterId !== null) return;
    
    activeView = view;
    activeChapterId = null;
    activeTab = 'learn';
    
    // Highlight toggles
    document.getElementById('toggle-concepts').classList.toggle('active', view === 'concepts');
    document.getElementById('toggle-patterns').classList.toggle('active', view === 'patterns');
    
    // Reset Search
    clearSearch();
    
    // Update Chapter Sidebar
    renderSidebar();
    
    // Show Dashboard
    showDashboard();
    
    // Scroll content top
    document.getElementById('main-content').scrollTop = 0;
    
    // Close sidebar on mobile if open
    closeMobileSidebar();
}

// Render Sidebar Navigation
function renderSidebar() {
    const navList = document.getElementById('chapters-nav-list');
    const titleElement = document.getElementById('sidebar-title');
    navList.innerHTML = '';
    
    const data = activeView === 'concepts' ? conceptsData : patternsData;
    if (!data) return;
    
    titleElement.textContent = activeView === 'concepts' ? 'C/C++ Concepts' : 'Interview Patterns';
    
    data.chapters.forEach(chapter => {
        const itemKey = `${activeView}_${chapter.id}`;
        const isCompleted = userProgress.completedChapters.includes(itemKey);
        
        // Calculate dynamic completion percentage of this chapter
        const completionPct = calculateChapterCompletion(chapter);
        
        const item = document.createElement('div');
        item.className = `chapter-item ${activeChapterId === chapter.id ? 'active' : ''} ${isCompleted ? 'completed-item' : ''}`;
        item.onclick = () => selectChapter(chapter.id);
        
        item.innerHTML = `
            <div class="chapter-item-left">
                <span class="chapter-emoji">${chapter.icon || '📚'}</span>
                <div class="chapter-info">
                    <span class="chapter-title" title="${chapter.title}">${chapter.title}</span>
                    <div class="chapter-meta-line">
                        <span class="chapter-difficulty-dot ${chapter.difficulty}"></span>
                        <span>${chapter.difficulty}</span>
                    </div>
                </div>
            </div>
            <div class="chapter-progress-ring">${isCompleted ? '✓' : `${completionPct}%`}</div>
        `;
        
        navList.appendChild(item);
    });
    
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

// Calculate the percentage completion of a single chapter
function calculateChapterCompletion(chapter) {
    if (activeView === 'concepts') {
        // Topics completion
        const topics = chapter.topics || [];
        if (topics.length === 0) return 0;
        let completed = 0;
        topics.forEach(t => {
            if (userProgress.completedTopics.includes(t.id)) completed++;
        });
        return Math.round((completed / topics.length) * 100);
    } else {
        // Problems completion
        const problems = chapter.problems || [];
        if (problems.length === 0) return 0;
        let completed = 0;
        problems.forEach(p => {
            if (userProgress.completedProblems.includes(p.id)) completed++;
        });
        return Math.round((completed / problems.length) * 100);
    }
}

// Select a specific chapter to learn
function selectChapter(chapterId) {
    activeChapterId = chapterId;
    
    // Hide dashboard / search views and show chapter view
    document.getElementById('dashboard-view').style.display = 'none';
    document.getElementById('search-view').style.display = 'none';
    document.getElementById('chapter-view').style.display = 'flex';
    
    // Re-render sidebar to highlight active
    renderSidebar();
    
    const data = activeView === 'concepts' ? conceptsData : patternsData;
    const chapter = data.chapters.find(c => c.id === chapterId);
    if (!chapter) return;
    
    // Populate header info
    document.getElementById('chapter-number-val').textContent = chapter.id;
    document.getElementById('chapter-emoji').textContent = chapter.icon || '📚';
    document.getElementById('chapter-title-text').innerHTML = `<span id="chapter-emoji">${chapter.icon || '📚'}</span> ${chapter.title}`;
    document.getElementById('chapter-description-text').textContent = chapter.description;
    
    // Handle difficulty badge color
    const diffBadge = document.getElementById('chapter-difficulty-badge');
    diffBadge.className = `difficulty-badge ${chapter.difficulty}`;
    diffBadge.textContent = chapter.difficulty;
    
    // Checkbox state for chapter complete
    const chapterKey = `${activeView}_${chapter.id}`;
    document.getElementById('chapter-complete-checkbox').checked = userProgress.completedChapters.includes(chapterKey);
    
    // Set tabs depending on view type
    const problemsTab = document.getElementById('tab-problems');
    const patternOverview = document.getElementById('pattern-overview-container');
    
    if (activeView === 'concepts') {
        problemsTab.style.display = 'none';
        patternOverview.style.display = 'none';
        
        // Show "Learn Concepts" tab by default
        if (activeTab === 'problems') activeTab = 'learn';
        
        renderConceptsTab(chapter);
    } else {
        problemsTab.style.display = 'block';
        patternOverview.style.display = 'block';
        
        // Populate pattern overview details
        document.getElementById('pattern-overview-text').innerHTML = marked.parse(chapter.patternOverview || '');
        const whenToUseList = document.getElementById('pattern-when-to-use-list');
        whenToUseList.innerHTML = '';
        if (chapter.whenToUse) {
            chapter.whenToUse.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                whenToUseList.appendChild(li);
            });
        }
        
        // Show "Coding Problems" by default for interview patterns
        if (activeTab === 'learn') activeTab = 'problems';
        
        renderPatternsTab(chapter);
    }
    
    // Set active tab styling
    switchChapterTab(activeTab);
    
    // Render Quiz Tab for both
    renderQuizTab(chapter);
    
    // Scroll viewport to top
    document.getElementById('main-content').scrollTop = 0;
    
    // Close mobile menu
    closeMobileSidebar();
}

// Switch chapter active tabs (Learn, Problems, Quiz)
function switchChapterTab(tab) {
    activeTab = tab;
    
    // Toggle active class on buttons
    document.querySelectorAll('.chapter-tab').forEach(btn => {
        btn.classList.remove('active');
    });
    document.getElementById(`tab-${tab}`).classList.add('active');
    
    // Toggle active panel
    document.querySelectorAll('.tab-panel').forEach(panel => {
        panel.classList.remove('active');
        panel.style.display = 'none';
    });
    const activePanel = document.getElementById(`panel-${tab}`);
    activePanel.classList.add('active');
    activePanel.style.display = 'flex';
    
    // Refresh prism syntax highlighting
    if (tab === 'learn' || tab === 'problems') {
        setTimeout(() => {
            if (typeof Prism !== 'undefined') {
                Prism.highlightAllUnder(activePanel);
            }
        }, 50);
    }
}

// Render Content for C++ Concepts Tab
function renderConceptsTab(chapter) {
    const container = document.getElementById('topics-container');
    container.innerHTML = '';
    
    const topics = chapter.topics || [];
    
    topics.forEach(topic => {
        const isCompleted = userProgress.completedTopics.includes(topic.id);
        const card = document.createElement('article');
        card.className = `topic-card ${isCompleted ? 'completed-card' : ''}`;
        card.id = `topic-${topic.id.replace('.', '-')}`;
        
        // Build code examples HTML
        let codeExamplesHtml = '';
        if (topic.codeExamples) {
            topic.codeExamples.forEach((ex, idx) => {
                codeExamplesHtml += `
                    <div class="code-example-card">
                        <div class="code-header">
                            <span class="code-title">${ex.title}</span>
                            <span class="code-lang-tag">${ex.language}</span>
                        </div>
                        <pre class="language-${ex.language}"><code>${escapeHtml(ex.code)}</code></pre>
                        ${ex.explanation ? `<div class="code-explanation">${marked.parse(ex.explanation)}</div>` : ''}
                    </div>
                `;
            });
        }
        
        // Build common mistakes list
        let mistakesHtml = '';
        if (topic.commonMistakes && topic.commonMistakes.length > 0) {
            mistakesHtml += `
                <div class="alert-box error-alert">
                    <h4><i data-lucide="alert-triangle"></i> Common Pitfalls</h4>
                    <ul>
                        ${topic.commonMistakes.map(m => `<li>${marked.parseInline(m)}</li>`).join('')}
                    </ul>
                </div>
            `;
        }
        
        // Build interview tips list
        let tipsHtml = '';
        if (topic.interviewTips && topic.interviewTips.length > 0) {
            tipsHtml += `
                <div class="alert-box tip-alert">
                    <h4><i data-lucide="lightbulb"></i> Interview Tips</h4>
                    <ul>
                        ${topic.interviewTips.map(t => `<li>${marked.parseInline(t)}</li>`).join('')}
                    </ul>
                </div>
            `;
        }
        
        // Renders complete layout
        card.innerHTML = `
            <div class="topic-header">
                <h3>${topic.title}</h3>
                <label class="checkbox-container">
                    <input type="checkbox" ${isCompleted ? 'checked' : ''} onchange="toggleTopicCompletion('${topic.id}', this.checked)">
                    <span class="checkmark"></span>
                    <span class="check-label" style="font-size:0.75rem;">Mark as Read</span>
                </label>
            </div>
            
            <div class="topic-explanation">
                ${marked.parse(topic.explanation || '')}
            </div>
            
            ${topic.keyPoints && topic.keyPoints.length > 0 ? `
                <div class="key-points-box">
                    <h4>Key Fundamentals</h4>
                    <ul>
                        ${topic.keyPoints.map(p => `<li>${marked.parseInline(p)}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
            
            ${codeExamplesHtml}
            
            ${(mistakesHtml || tipsHtml) ? `
                <div class="mistakes-tips-row">
                    ${mistakesHtml}
                    ${tipsHtml}
                </div>
            ` : ''}
        `;
        
        container.appendChild(card);
    });
    
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

// Render Content for Coding Patterns Tab (Problems & Template patterns)
function renderPatternsTab(chapter) {
    // 1. Render patterns models
    const patternsSubcontainer = document.getElementById('patterns-subcontainer');
    patternsSubcontainer.innerHTML = '';
    
    const patterns = chapter.patterns || [];
    patterns.forEach(pat => {
        const div = document.createElement('div');
        div.className = 'pattern-card';
        div.id = `pattern-${pat.id.replace('.', '-')}`;
        
        div.innerHTML = `
            <div class="pattern-title-row">
                <h3>${pat.name}</h3>
                <div class="complexity-tag-group">
                    <span class="comp-tag time" title="Time Complexity">Time: ${pat.timeComplexity}</span>
                    <span class="comp-tag space" title="Space Complexity">Space: ${pat.spaceComplexity}</span>
                </div>
            </div>
            
            <p class="pattern-desc">${pat.description}</p>
            <div class="pattern-intuition">
                <strong>💡 Intuition:</strong> ${pat.intuition}
            </div>
            
            <div class="code-example-card">
                <div class="code-header">
                    <span class="code-title">Pattern Template Code</span>
                    <span class="code-lang-tag">cpp</span>
                </div>
                <pre class="language-cpp"><code>${escapeHtml(pat.template || '')}</code></pre>
            </div>
            
            <div class="pattern-meta-grid">
                <div class="pattern-meta-box">
                    <h4>Identification Signals</h4>
                    <div class="p-pill-group">
                        ${(pat.identificationSignals || []).map(sig => `<span class="p-pill">${sig}</span>`).join('')}
                    </div>
                </div>
                <div class="pattern-meta-box">
                    <h4>Variations / Applications</h4>
                    <div class="p-pill-group">
                        ${(pat.variations || []).map(v => `<span class="p-pill">${v}</span>`).join('')}
                    </div>
                </div>
            </div>
        `;
        patternsSubcontainer.appendChild(div);
    });
    
    // 2. Render actual coding problems list
    const problemsContainer = document.getElementById('problems-container');
    problemsContainer.innerHTML = '';
    
    const problems = chapter.problems || [];
    problems.forEach(prob => {
        const isSolved = userProgress.completedProblems.includes(prob.id);
        const card = document.createElement('article');
        card.className = `problem-card ${isSolved ? 'solved-card' : ''}`;
        card.id = `problem-${prob.id}`;
        
        // Build examples HTML
        let examplesHtml = '';
        if (prob.examples) {
            prob.examples.forEach((ex, idx) => {
                examplesHtml += `
                    <div class="example-item">
                        <strong>Example ${idx + 1}:</strong><br>
                        <strong>Input:</strong> ${ex.input}<br>
                        <strong>Output:</strong> ${ex.output}<br>
                        ${ex.explanation ? `<strong>Explanation:</strong> ${ex.explanation}` : ''}
                    </div>
                `;
            });
        }
        
        // Build constraints & hints HTML
        const constraintsHtml = prob.constraints && prob.constraints.length > 0 
            ? `<div class="details-block constraints">
                 <h4>Constraints</h4>
                 <ul>
                     ${prob.constraints.map(c => `<li>${escapeHtml(c)}</li>`).join('')}
                 </ul>
               </div>` 
            : '';
            
        const hintsHtml = prob.hints && prob.hints.length > 0 
            ? `<div class="details-block hints">
                 <h4>Hints & Strategy</h4>
                 <ul>
                     ${prob.hints.map(h => `<li>${escapeHtml(h)}</li>`).join('')}
                 </ul>
               </div>` 
            : '';
            
        // Build solution code tabs tabs layout
        card.innerHTML = `
            <div class="problem-header">
                <div class="problem-title-box">
                    <h3>${prob.title}</h3>
                    <span class="problem-source-tag">${prob.source || ''}</span>
                </div>
                <div class="problem-meta-right">
                    <span class="difficulty-badge ${prob.difficulty}">${prob.difficulty}</span>
                    <label class="checkbox-container">
                        <input type="checkbox" ${isSolved ? 'checked' : ''} onchange="toggleProblemCompletion('${prob.id}', this.checked)">
                        <span class="checkmark"></span>
                        <span class="check-label" style="font-size:0.75rem;">Mark Solved</span>
                    </label>
                </div>
            </div>
            
            <div class="problem-statement">
                ${marked.parse(prob.problemStatement || '')}
            </div>
            
            <div class="problem-examples-box">
                ${examplesHtml}
            </div>
            
            ${(constraintsHtml || hintsHtml) ? `
                <div class="problem-details-grid">
                    ${constraintsHtml}
                    ${hintsHtml}
                </div>
            ` : ''}
            
            <!-- Code Tab controls -->
            <div class="problem-tabs-bar">
                <button class="problem-tab active" onclick="switchProblemTab(this, '${prob.id}', 'optimal')">Optimal Solution</button>
                ${prob.bruteForce ? `<button class="problem-tab" onclick="switchProblemTab(this, '${prob.id}', 'brute')">Brute Force</button>` : ''}
            </div>
            
            <!-- Optimal Panel -->
            <div id="solution-optimal-${prob.id}" class="problem-panel active">
                <div class="solution-meta">
                    <span><strong>Approach:</strong> ${prob.optimalSolution.approach}</span>
                    <div class="complexity-tag-group">
                        <span class="comp-tag time">Time: ${prob.optimalSolution.timeComplexity}</span>
                        <span class="comp-tag space">Space: ${prob.optimalSolution.spaceComplexity}</span>
                    </div>
                </div>
                ${prob.optimalSolution.intuition ? `<div class="solution-description"><strong>Intuition:</strong> ${prob.optimalSolution.intuition}</div>` : ''}
                
                <div class="code-example-card">
                    <div class="code-header">
                        <span class="code-title">C++ Source</span>
                        <span class="code-lang-tag">cpp</span>
                    </div>
                    <pre class="language-cpp"><code>${escapeHtml(prob.optimalSolution.code)}</code></pre>
                </div>
                
                ${prob.optimalSolution.walkthrough ? `<div class="code-explanation"><strong>Line Walkthrough:</strong><br>${marked.parse(prob.optimalSolution.walkthrough)}</div>` : ''}
            </div>
            
            <!-- Brute Force Panel (if exists) -->
            ${prob.bruteForce ? `
            <div id="solution-brute-${prob.id}" class="problem-panel">
                <div class="solution-meta">
                    <span><strong>Approach:</strong> ${prob.bruteForce.approach}</span>
                    <div class="complexity-tag-group">
                        <span class="comp-tag time">Time: ${prob.bruteForce.timeComplexity}</span>
                        <span class="comp-tag space">Space: ${prob.bruteForce.spaceComplexity}</span>
                    </div>
                </div>
                ${prob.bruteForce.code ? `
                <div class="code-example-card">
                    <div class="code-header">
                        <span class="code-title">C++ Source</span>
                        <span class="code-lang-tag">cpp</span>
                    </div>
                    <pre class="language-cpp"><code>${escapeHtml(prob.bruteForce.code)}</code></pre>
                </div>` : ''}
            </div>
            ` : ''}
            
            ${prob.companiesAsked && prob.companiesAsked.length > 0 ? `
                <div style="display:flex; align-items:center; gap:8px; font-size:0.75rem; color:var(--text-muted);">
                    <strong>Asked in:</strong>
                    <div style="display:flex; gap:4px; flex-wrap:wrap;">
                        ${prob.companiesAsked.map(c => `<span style="background-color:rgba(255,255,255,0.03); border:1px solid var(--border-color); padding: 1px 6px; border-radius:10px;">${c}</span>`).join('')}
                    </div>
                </div>
            ` : ''}
        `;
        
        problemsContainer.appendChild(card);
    });
}

// Handler to switch Brute Force vs Optimal C++ Code tabs
function switchProblemTab(btnElement, problemId, type) {
    const parent = btnElement.closest('.problem-card');
    
    // Highlight buttons
    parent.querySelectorAll('.problem-tab').forEach(btn => btn.classList.remove('active'));
    btnElement.classList.add('active');
    
    // Toggle active panel
    parent.querySelectorAll('.problem-panel').forEach(panel => {
        panel.classList.remove('active');
        panel.style.display = 'none';
    });
    
    const targetPanel = parent.querySelector(`#solution-${type}-${problemId}`);
    targetPanel.classList.add('active');
    targetPanel.style.display = 'flex';
    
    // Highlight code inside
    if (typeof Prism !== 'undefined') {
        Prism.highlightAllUnder(targetPanel);
    }
}

// Render Content for Chapter Assessment / Quiz Tab
function renderQuizTab(chapter) {
    const questionsContainer = document.getElementById('quiz-questions-container');
    questionsContainer.innerHTML = '';
    
    const quizQuestions = activeView === 'concepts' 
        ? (chapter.quizQuestions || []) 
        : (chapter.chapterQuiz || []);
        
    document.getElementById('quiz-total-count').textContent = quizQuestions.length;
    
    // Reset grade values
    const scoreBox = document.getElementById('quiz-result-score');
    scoreBox.style.display = 'none';
    
    // Retrieve previous grade if any
    const scoreKey = `${activeView}_${chapter.id}`;
    const previousGrade = userProgress.quizScores[scoreKey];
    const statusText = document.getElementById('quiz-status-text');
    
    if (previousGrade) {
        statusText.textContent = `Completed (${previousGrade.score}/${previousGrade.total})`;
        statusText.style.color = 'var(--accent-emerald)';
    } else {
        statusText.textContent = 'Not Started';
        statusText.style.color = 'var(--text-muted)';
    }
    
    if (quizQuestions.length === 0) {
        questionsContainer.innerHTML = '<div style="padding:20px; text-align:center; color:var(--text-muted);">No quiz questions defined for this chapter yet.</div>';
        document.getElementById('btn-submit-quiz').style.display = 'none';
        return;
    }
    
    document.getElementById('btn-submit-quiz').style.display = 'block';
    
    quizQuestions.forEach((q, idx) => {
        const card = document.createElement('div');
        card.className = 'quiz-question-card';
        card.id = `q-card-${idx}`;
        
        let codeBlock = '';
        if (q.code) {
            codeBlock = `
                <div class="code-example-card" style="margin-bottom:10px;">
                    <pre class="language-cpp"><code>${escapeHtml(q.code)}</code></pre>
                </div>
            `;
        }
        
        // Renders question layout
        card.innerHTML = `
            <div class="quiz-question-meta">
                <span>Question ${idx + 1} of ${quizQuestions.length}</span>
                <span>Type: ${q.type ? q.type.replace('_', ' ') : 'Multiple Choice'}</span>
            </div>
            
            <p class="question-text">${marked.parseInline(q.question)}</p>
            
            ${codeBlock}
            
            <div class="quiz-options-list">
                ${q.options.map((opt, optIdx) => `
                    <label class="option-label" onclick="selectQuizOption(this, ${idx})">
                        <input type="radio" name="q-option-${idx}" value="${optIdx}">
                        <span class="option-radio-dot"></span>
                        <span class="option-text">${escapeHtml(opt)}</span>
                    </label>
                `).join('')}
            </div>
            
            <div class="quiz-explanation-box" id="explanation-${idx}">
                <strong>💡 Explanation:</strong> ${q.explanation ? marked.parse(q.explanation) : 'No explanation provided.'}
            </div>
        `;
        questionsContainer.appendChild(card);
    });
    
    // Highlight syntax inside quiz questions
    if (typeof Prism !== 'undefined') {
        Prism.highlightAllUnder(questionsContainer);
    }
}

// User selects a radio card option in quiz
function selectQuizOption(labelElement, qIdx) {
    const parentCard = labelElement.closest('.quiz-question-card');
    
    // Don't change selection if already graded
    if (parentCard.classList.contains('graded-correct') || parentCard.classList.contains('graded-incorrect')) {
        return;
    }
    
    parentCard.querySelectorAll('.option-label').forEach(label => {
        label.classList.remove('selected-option-card');
    });
    labelElement.classList.add('selected-option-card');
    labelElement.querySelector('input').checked = true;
}

// Grade the whole chapter assessment quiz
function gradeChapterQuiz() {
    const data = activeView === 'concepts' ? conceptsData : patternsData;
    const chapter = data.chapters.find(c => c.id === activeChapterId);
    if (!chapter) return;
    
    const quizQuestions = activeView === 'concepts' 
        ? (chapter.quizQuestions || []) 
        : (chapter.chapterQuiz || []);
        
    let correctCount = 0;
    
    quizQuestions.forEach((q, idx) => {
        const card = document.getElementById(`q-card-${idx}`);
        
        // Remove existing grade classes
        card.classList.remove('graded-correct', 'graded-incorrect');
        card.querySelectorAll('.option-label').forEach(lbl => {
            lbl.classList.remove('graded-correct-card', 'graded-incorrect-card');
        });
        
        // Remove existing grade badges if any
        const oldBadge = card.querySelector('.question-grade-badge');
        if (oldBadge) oldBadge.remove();
        
        // Fetch selected answer value
        const checkedInput = card.querySelector(`input[name="q-option-${idx}"]:checked`);
        let selectedIdx = checkedInput ? parseInt(checkedInput.value) : -1;
        
        // Resolve correct answer index. Note: JSON correctAnswer might be string (value) or number (index).
        // Let's resolve index correctly.
        let correctIdx = -1;
        
        if (typeof q.correctAnswer === 'number') {
            correctIdx = q.correctAnswer;
        } else {
            // Find index of option matching string value
            correctIdx = q.options.findIndex(opt => opt.trim() === q.correctAnswer.trim());
            // Fallback: if value is single char A, B, C, D
            if (correctIdx === -1 && q.correctAnswer.length === 1) {
                correctIdx = q.correctAnswer.charCodeAt(0) - 65; // 'A' = 0
            }
        }
        
        const isCorrect = (selectedIdx === correctIdx);
        
        // Highlight logic
        if (isCorrect) {
            correctCount++;
            card.classList.add('graded-correct');
            
            // Add correct badge
            const badge = document.createElement('span');
            badge.className = 'question-grade-badge correct';
            badge.textContent = 'Correct';
            card.appendChild(badge);
        } else {
            card.classList.add('graded-incorrect');
            
            // Add incorrect badge
            const badge = document.createElement('span');
            badge.className = 'question-grade-badge incorrect';
            badge.textContent = 'Incorrect';
            card.appendChild(badge);
            
            // Mark selected as incorrect
            if (checkedInput) {
                checkedInput.closest('.option-label').classList.add('graded-incorrect-card');
            }
        }
        
        // Always highlight the correct answer label green
        if (correctIdx >= 0 && correctIdx < q.options.length) {
            card.querySelectorAll('.option-label')[correctIdx].classList.add('graded-correct-card');
        }
        
        // Show explanation
        document.getElementById(`explanation-${idx}`).classList.add('show');
    });
    
    // Save quiz score
    const scoreKey = `${activeView}_${activeChapterId}`;
    userProgress.quizScores[scoreKey] = {
        score: correctCount,
        total: quizQuestions.length
    };
    
    // Update Score Indicator
    const scoreBox = document.getElementById('quiz-result-score');
    scoreBox.style.display = 'block';
    document.getElementById('quiz-score-val').textContent = `${correctCount}/${quizQuestions.length}`;
    
    const pct = quizQuestions.length > 0 ? Math.round((correctCount / quizQuestions.length) * 100) : 0;
    document.getElementById('quiz-percent-val').textContent = `${pct}%`;
    
    // Update Status header
    const statusText = document.getElementById('quiz-status-text');
    statusText.textContent = `Graded (${correctCount}/${quizQuestions.length})`;
    statusText.style.color = correctCount === quizQuestions.length ? 'var(--accent-emerald)' : 'var(--accent-amber)';
    
    saveProgress();
    
    // Auto-mark chapter as complete if they scored 100%
    if (correctCount === quizQuestions.length) {
        toggleChapterCompletion(true);
    }
}

// Toggle chapter complete checkbox manually or from quiz 100%
function toggleChapterCompletion(isChecked) {
    const chapterKey = `${activeView}_${activeChapterId}`;
    
    if (isChecked) {
        if (!userProgress.completedChapters.includes(chapterKey)) {
            userProgress.completedChapters.push(chapterKey);
        }
    } else {
        userProgress.completedChapters = userProgress.completedChapters.filter(k => k !== chapterKey);
    }
    
    document.getElementById('chapter-complete-checkbox').checked = isChecked;
    saveProgress();
    renderSidebar();
}

// Toggle reading complete checkbox for single C++ topic
function toggleTopicCompletion(topicId, isChecked) {
    if (isChecked) {
        if (!userProgress.completedTopics.includes(topicId)) {
            userProgress.completedTopics.push(topicId);
        }
    } else {
        userProgress.completedTopics = userProgress.completedTopics.filter(id => id !== topicId);
    }
    
    // Toggle completed class styling
    const card = document.getElementById(`topic-${topicId.replace('.', '-')}`);
    if (card) {
        card.classList.toggle('completed-card', isChecked);
    }
    
    saveProgress();
    renderSidebar();
}

// Toggle solve status checkbox for single coding problem
function toggleProblemCompletion(problemId, isChecked) {
    if (isChecked) {
        if (!userProgress.completedProblems.includes(problemId)) {
            userProgress.completedProblems.push(problemId);
        }
    } else {
        userProgress.completedProblems = userProgress.completedProblems.filter(id => id !== problemId);
    }
    
    // Toggle solved class styling
    const card = document.getElementById(`problem-${problemId}`);
    if (card) {
        card.classList.toggle('solved-card', isChecked);
    }
    
    saveProgress();
    renderSidebar();
}

// Reset ALL progress inside local storage
function resetProgress() {
    if (confirm("Are you sure you want to reset all completion progress? This will delete all your local completion marks, solved problems, and quiz results.")) {
        userProgress = {
            completedTopics: [],
            completedProblems: [],
            completedChapters: [],
            quizScores: {}
        };
        localStorage.removeItem('samsung_prep_progress');
        
        updateOverallProgress();
        showToast("All progress reset completed!");
        
        // Re-load sidebar and current chapter/dashboard
        if (activeChapterId !== null) {
            selectChapter(activeChapterId);
        } else {
            showDashboard();
        }
    }
}

// Calculate and update global header completion progress meter & dashboard counters
function updateOverallProgress() {
    if (!conceptsData || !patternsData) return;
    
    let totalItems = 0;
    let completedItems = 0;
    
    // Concepts: topics to read
    conceptsData.chapters.forEach(ch => {
        (ch.topics || []).forEach(t => {
            totalItems++;
            if (userProgress.completedTopics.includes(t.id)) completedItems++;
        });
    });
    
    // Patterns: coding problems to solve
    patternsData.chapters.forEach(ch => {
        (ch.problems || []).forEach(p => {
            totalItems++;
            if (userProgress.completedProblems.includes(p.id)) completedItems++;
        });
    });
    
    const pct = totalItems > 0 ? Math.round((completedItems / totalItems) * 100) : 0;
    
    // Set header values
    document.getElementById('overall-progress-text').textContent = `${pct}%`;
    document.getElementById('overall-progress-bar').style.width = `${pct}%`;
    
    // Calculate dashboard counters
    let readCount = userProgress.completedTopics.length;
    let totalTopics = 0;
    conceptsData.chapters.forEach(ch => totalTopics += (ch.topics || []).length);
    
    let solvedCount = userProgress.completedProblems.length;
    let totalProblems = 0;
    patternsData.chapters.forEach(ch => totalProblems += (ch.problems || []).length);
    
    let passedQuizzes = Object.keys(userProgress.quizScores).length;
    let totalQuizzes = conceptsData.chapters.length + patternsData.chapters.length;
    
    // Populate dashboard labels if elements exist
    const readEl = document.getElementById('stat-concepts-read');
    if (readEl) readEl.textContent = `${readCount}/${totalTopics}`;
    
    const solvedEl = document.getElementById('stat-problems-solved');
    if (solvedEl) solvedEl.textContent = `${solvedCount}/${totalProblems}`;
    
    const quizEl = document.getElementById('stat-quizzes-passed');
    if (quizEl) quizEl.textContent = `${passedQuizzes}/${totalQuizzes}`;
}

// Render Dashboard View / Home screen
function showDashboard() {
    activeChapterId = null;
    
    // Hide details panel, show dashboard
    document.getElementById('chapter-view').style.display = 'none';
    document.getElementById('search-view').style.display = 'none';
    document.getElementById('dashboard-view').style.display = 'block';
    
    // Highlight dashboard in sidebar
    renderSidebar();
    updateOverallProgress();
    
    // Build learning paths steps
    renderDashboardPaths();
}

// Renders the quick visual roadmap cards on the dashboard home screen
function renderDashboardPaths() {
    const conceptsPath = document.getElementById('concepts-path-steps');
    conceptsPath.innerHTML = '';
    
    if (conceptsData) {
        conceptsData.chapters.forEach(ch => {
            const itemKey = `concepts_${ch.id}`;
            const isCompleted = userProgress.completedChapters.includes(itemKey);
            const compPct = calculateChapterCompletion(ch);
            
            const li = document.createElement('li');
            li.className = 'path-step-item';
            li.onclick = () => {
                switchView('concepts');
                selectChapter(ch.id);
            };
            
            li.innerHTML = `
                <div class="path-step-left">
                    <span>${ch.icon || '🎯'}</span>
                    <span>${ch.title}</span>
                </div>
                <div class="path-step-right">
                    <span class="difficulty-badge ${ch.difficulty}" style="font-size: 0.6rem;">${ch.difficulty}</span>
                    <span style="font-size:0.75rem; font-weight:700; color:${isCompleted ? 'var(--accent-emerald)' : 'var(--text-muted)'}">
                        ${isCompleted ? '✓ Done' : `${compPct}%`}
                    </span>
                </div>
            `;
            conceptsPath.appendChild(li);
        });
    }
    
    const patternsPath = document.getElementById('patterns-path-steps');
    patternsPath.innerHTML = '';
    
    if (patternsData) {
        patternsData.chapters.forEach(ch => {
            const itemKey = `patterns_${ch.id}`;
            const isCompleted = userProgress.completedChapters.includes(itemKey);
            const compPct = calculateChapterCompletion(ch);
            
            const li = document.createElement('li');
            li.className = 'path-step-item';
            li.onclick = () => {
                switchView('patterns');
                selectChapter(ch.id);
            };
            
            li.innerHTML = `
                <div class="path-step-left">
                    <span>${ch.icon || '🧩'}</span>
                    <span>${ch.title}</span>
                </div>
                <div class="path-step-right">
                    <span class="difficulty-badge ${ch.difficulty}" style="font-size: 0.6rem;">${ch.difficulty}</span>
                    <span style="font-size:0.75rem; font-weight:700; color:${isCompleted ? 'var(--accent-emerald)' : 'var(--text-muted)'}">
                        ${isCompleted ? '✓ Done' : `${compPct}%`}
                    </span>
                </div>
            `;
            patternsPath.appendChild(li);
        });
    }
}

// Global Instant Search Filtering Logic
function handleSearch(query) {
    searchQuery = query.trim().toLowerCase();
    const clearBtn = document.getElementById('clear-search');
    
    if (!searchQuery) {
        clearSearch();
        return;
    }
    
    clearBtn.style.display = 'block';
    
    // Hide standard views and open search view
    document.getElementById('dashboard-view').style.display = 'none';
    document.getElementById('chapter-view').style.display = 'none';
    document.getElementById('search-view').style.display = 'block';
    
    document.getElementById('search-query-text').textContent = query;
    
    const resultsContainer = document.getElementById('search-results-list');
    resultsContainer.innerHTML = '';
    
    const matches = [];
    
    // 1. Search in C++ Concepts
    if (conceptsData) {
        conceptsData.chapters.forEach(ch => {
            // Check chapter title
            if (ch.title.toLowerCase().includes(searchQuery) || ch.description.toLowerCase().includes(searchQuery)) {
                matches.push({
                    type: 'chapter',
                    view: 'concepts',
                    chapterId: ch.id,
                    title: ch.title,
                    snippet: ch.description,
                    icon: ch.icon || '📚'
                });
            }
            
            // Check topics
            (ch.topics || []).forEach(topic => {
                if (topic.title.toLowerCase().includes(searchQuery) || 
                    topic.explanation.toLowerCase().includes(searchQuery) || 
                    (topic.keyPoints || []).some(k => k.toLowerCase().includes(searchQuery))) {
                    matches.push({
                        type: 'topic',
                        view: 'concepts',
                        chapterId: ch.id,
                        topicId: topic.id,
                        chapterTitle: ch.title,
                        title: topic.title,
                        snippet: topic.explanation.substring(0, 140) + '...',
                        icon: '📄'
                    });
                }
            });
        });
    }
    
    // 2. Search in Coding Patterns
    if (patternsData) {
        patternsData.chapters.forEach(ch => {
            // Check chapter title
            if (ch.title.toLowerCase().includes(searchQuery) || ch.description.toLowerCase().includes(searchQuery)) {
                matches.push({
                    type: 'chapter',
                    view: 'patterns',
                    chapterId: ch.id,
                    title: ch.title,
                    snippet: ch.description,
                    icon: ch.icon || '📚'
                });
            }
            
            // Check problems
            (ch.problems || []).forEach(prob => {
                const targetCompaniesMatch = (prob.companiesAsked || []).some(c => c.toLowerCase().includes(searchQuery));
                if (prob.title.toLowerCase().includes(searchQuery) || 
                    prob.problemStatement.toLowerCase().includes(searchQuery) ||
                    targetCompaniesMatch) {
                    matches.push({
                        type: 'problem',
                        view: 'patterns',
                        chapterId: ch.id,
                        problemId: prob.id,
                        chapterTitle: ch.title,
                        title: prob.title,
                        snippet: `Asked in: ${(prob.companiesAsked || []).join(', ') || 'N/A'}. Statement: ${prob.problemStatement.substring(0, 100)}...`,
                        icon: '💻'
                    });
                }
            });
            
            // Check patterns
            (ch.patterns || []).forEach(pat => {
                if (pat.name.toLowerCase().includes(searchQuery) || pat.description.toLowerCase().includes(searchQuery)) {
                    matches.push({
                        type: 'pattern',
                        view: 'patterns',
                        chapterId: ch.id,
                        patternId: pat.id,
                        chapterTitle: ch.title,
                        title: pat.name,
                        snippet: pat.description,
                        icon: '🧩'
                    });
                }
            });
        });
    }
    
    document.getElementById('search-results-count').textContent = matches.length;
    
    if (matches.length === 0) {
        resultsContainer.innerHTML = `
            <div style="text-align:center; padding:40px; color:var(--text-muted);">
                <i data-lucide="search-code" style="width:48px; height:48px; margin-bottom:12px;"></i>
                <p>No results found for "${query}". Try searching for concepts like "Pointer", "Unique Pointer", "LRU Cache", "Two Pointers" or companies like "Nvidia".</p>
            </div>
        `;
        if (typeof lucide !== 'undefined') lucide.createIcons();
        return;
    }
    
    matches.forEach(match => {
        const card = document.createElement('div');
        card.className = 'search-result-card';
        card.onclick = () => navigateToSearchResult(match);
        
        let metaHtml = '';
        if (match.type === 'chapter') {
            metaHtml = `<span class="path">${match.view === 'concepts' ? 'Concepts' : 'Patterns'} Path</span> • <span class="chapter">Full Chapter</span>`;
        } else {
            metaHtml = `<span class="path">${match.view === 'concepts' ? 'Concepts' : 'Patterns'} Path</span> • <span class="chapter">${match.chapterTitle}</span>`;
        }
        
        card.innerHTML = `
            <div class="result-meta">
                <span>${match.icon}</span>
                ${metaHtml}
            </div>
            <h3>${match.title}</h3>
            <p class="result-snippet">${match.snippet}</p>
        `;
        resultsContainer.appendChild(card);
    });
}

// Navigate to selected search result location
function navigateToSearchResult(match) {
    // 1. Switch global view first
    switchView(match.view);
    
    // 2. Select chapter
    selectChapter(match.chapterId);
    
    // 3. Switch tab depending on entry type
    if (match.type === 'topic') {
        switchChapterTab('learn');
        
        // Scroll to the specific topic card
        setTimeout(() => {
            const elId = `topic-${match.topicId.replace('.', '-')}`;
            const element = document.getElementById(elId);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth', block: 'center' });
                // Add a glow border effect momentarily
                element.style.borderColor = 'var(--accent-indigo)';
                element.style.boxShadow = '0 0 15px var(--accent-indigo-glow)';
                setTimeout(() => {
                    element.style.borderColor = '';
                    element.style.boxShadow = '';
                }, 3000);
            }
        }, 100);
    } else if (match.type === 'problem') {
        switchChapterTab('problems');
        
        // Scroll to problem
        setTimeout(() => {
            const elId = `problem-${match.problemId}`;
            const element = document.getElementById(elId);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth', block: 'center' });
                element.style.borderColor = 'var(--accent-indigo)';
                setTimeout(() => {
                    element.style.borderColor = '';
                }, 3000);
            }
        }, 100);
    } else if (match.type === 'pattern') {
        switchChapterTab('problems');
        
        // Scroll to pattern template
        setTimeout(() => {
            const elId = `pattern-${match.patternId.replace('.', '-')}`;
            const element = document.getElementById(elId);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth', block: 'center' });
                element.style.borderColor = 'var(--accent-cyan)';
                setTimeout(() => {
                    element.style.borderColor = '';
                }, 3000);
            }
        }, 100);
    }
}

// Clear Search box
function clearSearch() {
    document.getElementById('global-search').value = '';
    document.getElementById('clear-search').style.display = 'none';
    searchQuery = '';
    
    // Return to main layout views
    if (activeChapterId !== null) {
        document.getElementById('chapter-view').style.display = 'flex';
        document.getElementById('search-view').style.display = 'none';
    } else {
        showDashboard();
    }
}

// Helper: Escape HTML strings to render code safely inside code tags
function escapeHtml(unsafe) {
    if (!unsafe) return '';
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Mobile sidebar drawer controllers
function toggleSidebar() {
    const sidebar = document.getElementById('app-sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    const openIcon = document.getElementById('menu-icon-open');
    const closeIcon = document.getElementById('menu-icon-close');
    
    const isOpen = sidebar.classList.contains('mobile-open');
    
    sidebar.classList.toggle('mobile-open', !isOpen);
    overlay.classList.toggle('mobile-open', !isOpen);
    
    if (isOpen) {
        openIcon.style.display = 'block';
        closeIcon.style.display = 'none';
    } else {
        openIcon.style.display = 'none';
        closeIcon.style.display = 'block';
    }
}

function closeMobileSidebar() {
    const sidebar = document.getElementById('app-sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    const openIcon = document.getElementById('menu-icon-open');
    const closeIcon = document.getElementById('menu-icon-close');
    
    sidebar.classList.remove('mobile-open');
    overlay.classList.remove('mobile-open');
    if (openIcon) openIcon.style.display = 'block';
    if (closeIcon) closeIcon.style.display = 'none';
}
