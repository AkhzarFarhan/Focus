/**
 * C++ Mastery Study Plan Webapp Logic
 * Premium interactive light-themed client-side application
 */

let db = null;
let activeDayIndex = 0;
let progress = {};

// DOM Elements
const sidebar = document.getElementById('sidebar');
const daysList = document.getElementById('daysList');
const currentTopicTitle = document.getElementById('currentTopicTitle');
const loadingState = document.getElementById('loadingState');
const contentCard = document.getElementById('contentCard');
const subtopicsContainer = document.getElementById('subtopicsContainer');
const overallPercentage = document.getElementById('overallPercentage');
const overallProgressBar = document.getElementById('overallProgressBar');
const overallStatsCount = document.getElementById('overallStatsCount');
const searchInput = document.getElementById('searchInput');
const clearSearchBtn = document.getElementById('clearSearchBtn');
const searchResultsView = document.getElementById('searchResultsView');
const searchQueryText = document.getElementById('searchQueryText');
const searchResultsStats = document.getElementById('searchResultsStats');
const searchResultsList = document.getElementById('searchResultsList');
const menuToggleBtn = document.getElementById('menuToggleBtn');
const sidebarCloseBtn = document.getElementById('sidebarCloseBtn');
const resetProgressBtn = document.getElementById('resetProgressBtn');
const toast = document.getElementById('toast');
const toastMessage = document.getElementById('toastMessage');

// Create mobile overlay backdrop
const backdrop = document.createElement('div');
backdrop.className = 'sidebar-backdrop';
document.body.appendChild(backdrop);

/* -------------------------------------------------------------
 * Initialization & Data Fetching
 * ------------------------------------------------------------- */
document.addEventListener('DOMContentLoaded', () => {
    loadProgress();
    fetchPlan();
    setupEventListeners();
});

function fetchPlan() {
    fetch('./cpp_knowledgebase.json')
        .then(response => {
            if (!response.ok) throw new Error('Failed to fetch knowledgebase data.');
            return response.json();
        })
        .then(data => {
            db = data;
            loadingState.style.display = 'none';
            contentCard.style.display = 'block';
            renderSidebar();
            loadDay(0);
            updateOverallProgress();
        })
        .catch(err => {
            console.error(err);
            loadingState.innerHTML = `
                <i class="fa-solid fa-triangle-exclamation" style="font-size: 48px; color: var(--danger-icon);"></i>
                <p style="margin-top: 16px; font-weight: 600;">Error Loading Knowledgebase</p>
                <p style="font-size: 14px; color: var(--text-secondary);">${err.message}</p>
            `;
        });
}

/* -------------------------------------------------------------
 * State & Progress Tracking (LocalStorage)
 * ------------------------------------------------------------- */
function loadProgress() {
    const saved = localStorage.getItem('cpp_study_progress');
    if (saved) {
        try {
            progress = JSON.parse(saved);
        } catch (e) {
            progress = {};
        }
    }
}

function saveProgress() {
    localStorage.setItem('cpp_study_progress', JSON.stringify(progress));
}

function getSubtopicKey(dayNum, subtopicIndex) {
    return `d${dayNum}_s${subtopicIndex}`;
}

function updateOverallProgress() {
    if (!db) return;
    
    let totalSubtopics = 0;
    let completedCount = 0;
    
    db.days.forEach(day => {
        const subtopics = day.subtopics || [];
        totalSubtopics += subtopics.length;
        subtopics.forEach((_, idx) => {
            if (progress[getSubtopicKey(day.day, idx)]) {
                completedCount++;
            }
        });
    });
    
    // Also include cross-topic questions if desired, but subtopics are standard.
    const percentage = totalSubtopics > 0 ? Math.round((completedCount / totalSubtopics) * 100) : 0;
    
    overallPercentage.textContent = `${percentage}%`;
    overallProgressBar.style.width = `${percentage}%`;
    overallStatsCount.textContent = `${completedCount} of ${totalSubtopics} subtopics completed`;
    
    // Update sidebar items checkmarks dynamically
    updateSidebarCheckmarks();
}

function updateSidebarCheckmarks() {
    const navItems = daysList.querySelectorAll('li');
    navItems.forEach((li, idx) => {
        if (idx >= db.days.length) return; // Skip revision day if no subtopics
        const day = db.days[idx];
        const subtopics = day.subtopics || [];
        
        let allCompleted = subtopics.length > 0;
        subtopics.forEach((_, sIdx) => {
            if (!progress[getSubtopicKey(day.day, sIdx)]) {
                allCompleted = false;
            }
        });
        
        const checkEl = li.querySelector('.nav-day-check');
        if (allCompleted && subtopics.length > 0) {
            checkEl.style.display = 'inline';
        } else {
            checkEl.style.display = 'none';
        }
    });
}

function toggleSubtopicProgress(dayNum, subtopicIndex, isChecked) {
    const key = getSubtopicKey(dayNum, subtopicIndex);
    if (isChecked) {
        progress[key] = true;
        showToast('Subtopic completed!');
    } else {
        delete progress[key];
    }
    saveProgress();
    updateOverallProgress();
    updateDayCompletionBanner(dayNum);
}

function updateDayCompletionBanner(dayNum) {
    const day = db.days.find(d => d.day === dayNum);
    if (!day || !day.subtopics) return;
    
    const subtopics = day.subtopics;
    let completed = 0;
    subtopics.forEach((_, idx) => {
        if (progress[getSubtopicKey(dayNum, idx)]) completed++;
    });
    
    const pct = Math.round((completed / subtopics.length) * 100);
    const dayCompletionStatusText = document.getElementById('dayCompletionStatusText');
    const dayProgressBar = document.getElementById('dayProgressBar');
    
    if (dayCompletionStatusText && dayProgressBar) {
        dayCompletionStatusText.textContent = `${pct}% Complete (${completed} of ${subtopics.length} items)`;
        dayProgressBar.style.width = `${pct}%`;
    }
}

/* -------------------------------------------------------------
 * UI Rendering
 * ------------------------------------------------------------- */
function renderSidebar() {
    daysList.innerHTML = '';
    
    db.days.forEach((day, idx) => {
        const li = document.createElement('li');
        li.className = idx === activeDayIndex ? 'active' : '';
        li.dataset.index = idx;
        
        const hoursText = day.estimated_hours ? `${day.estimated_hours} hrs` : '';
        const dayBadgeText = day.day === 17 ? 'Summary' : `Day ${day.day}`;
        
        li.innerHTML = `
            <span class="nav-day-num">${day.day === 17 ? '★' : day.day}</span>
            <div class="nav-day-info">
                <span class="nav-day-title">${day.topic}</span>
                <span class="nav-day-meta">${dayBadgeText} • ${hoursText}</span>
            </div>
            <span class="nav-day-check" style="display: none;">
                <i class="fa-solid fa-circle-check"></i>
            </span>
        `;
        
        li.addEventListener('click', () => {
            loadDay(idx);
            closeSidebar();
        });
        
        daysList.appendChild(li);
    });
}

function loadDay(idx) {
    if (!db || idx < 0 || idx >= db.days.length) return;
    
    activeDayIndex = idx;
    
    // Clear search
    clearSearch();

    // Toggle active sidebar item
    const navItems = daysList.querySelectorAll('li');
    navItems.forEach((li, i) => {
        if (i === idx) li.classList.add('active');
        else li.classList.remove('active');
    });

    const day = db.days[idx];
    
    // Update Header & Banner
    currentTopicTitle.textContent = day.topic;
    document.getElementById('dayBadge').textContent = day.day === 17 ? 'Revision' : `Day ${day.day}`;
    document.getElementById('estimatedHours').textContent = day.estimated_hours || '4';
    document.getElementById('dayTopicTitle').textContent = day.topic;

    // Render completion progress for this day
    updateDayCompletionBanner(day.day);
    
    // Render Content
    subtopicsContainer.innerHTML = '';
    
    if (day.day === 17) {
        renderDay17Revision(day);
    } else {
        renderStandardDay(day);
    }

    // Scroll main content to top
    document.querySelector('.main-content').scrollTop = 0;
}

function renderStandardDay(day) {
    const subtopics = day.subtopics || [];
    
    subtopics.forEach((subtopic, index) => {
        const subtopicCard = document.createElement('section');
        subtopicCard.className = 'subtopic-card';
        subtopicCard.id = `subtopic-${index}`;
        
        const isCompleted = progress[getSubtopicKey(day.day, index)] ? 'checked' : '';
        const completedClass = isCompleted ? 'completed' : '';
        
        // Build Subtopic Title & Checkbox
        let headerHtml = `
            <div class="subtopic-header">
                <div class="subtopic-title-wrapper">
                    <h3 class="subtopic-title">${subtopic.title}</h3>
                </div>
                <label class="subtopic-checkbox-label ${completedClass}" id="label-check-${day.day}-${index}">
                    <input type="checkbox" ${isCompleted} onchange="handleCheckboxChange(${day.day}, ${index}, this)">
                    <span>${isCompleted ? 'Completed' : 'Mark Complete'}</span>
                </label>
            </div>
        `;
        
        // Build Explanation
        let explanationHtml = `
            <div class="subtopic-explanation">
                ${subtopic.explanation.split('\n\n').map(p => `<p>${escapeHtmlText(p).replace(/\n/g, '<br>')}</p>`).join('')}
            </div>
        `;
        
        // Build Code Examples
        let codeHtml = '';
        if (subtopic.examples && subtopic.examples.length > 0) {
            codeHtml += '<div class="code-section"><span class="code-section-title">Code Demonstration</span>';
            subtopic.examples.forEach((ex, exIdx) => {
                const codeId = `code_${day.day}_${index}_${exIdx}`;
                codeHtml += `
                    <div class="code-wrapper">
                        <div class="code-header">
                            <span class="code-title">${escapeHtmlText(ex.title)}</span>
                            <button class="copy-code-btn" onclick="copyCode('${codeId}')" title="Copy to Clipboard">
                                <i class="fa-regular fa-copy"></i> Copy
                            </button>
                        </div>
                        <pre><code id="${codeId}">${highlightCpp(ex.code)}</code></pre>
                    </div>
                    ${ex.explanation ? `<div class="code-explanation">${escapeHtmlText(ex.explanation)}</div>` : ''}
                `;
            });
            codeHtml += '</div>';
        }
        
        // Build Pitfalls & Tips Callout Box Grid
        let calloutsHtml = '';
        const hasPitfalls = subtopic.pitfalls && subtopic.pitfalls.length > 0;
        const hasTips = subtopic.tips_to_remember && subtopic.tips_to_remember.length > 0;
        
        if (hasPitfalls || hasTips) {
            calloutsHtml += '<div class="callouts-grid">';
            
            if (hasPitfalls) {
                calloutsHtml += `
                    <div class="callout-box pitfalls">
                        <div class="callout-title">
                            <i class="fa-solid fa-circle-exclamation"></i> Common Pitfalls
                        </div>
                        <ul class="callout-list">
                            ${subtopic.pitfalls.map(p => `<li>${escapeHtmlText(p)}</li>`).join('')}
                        </ul>
                    </div>
                `;
            }
            
            if (hasTips) {
                calloutsHtml += `
                    <div class="callout-box tips">
                        <div class="callout-title">
                            <i class="fa-solid fa-lightbulb"></i> Tips to Remember
                        </div>
                        <ul class="callout-list">
                            ${subtopic.tips_to_remember.map(t => `<li>${escapeHtmlText(t)}</li>`).join('')}
                        </ul>
                    </div>
                `;
            }
            
            calloutsHtml += '</div>';
        }
        
        // Build Interview Questions Accordion
        let questionsHtml = '';
        if (subtopic.questions && subtopic.questions.length > 0) {
            questionsHtml += '<div class="questions-section"><span class="questions-section-title">Interview Q&A</span>';
            subtopic.questions.forEach((q, qIdx) => {
                questionsHtml += `
                    <div class="question-accordion">
                        <div class="question-header" onclick="toggleAccordion(this)">
                            <span class="question-text">${escapeHtmlText(q.question)}</span>
                            <span class="question-arrow"><i class="fa-solid fa-chevron-down"></i></span>
                        </div>
                        <div class="question-answer-panel">
                            <div class="question-answer-content">
                                ${escapeHtmlText(q.answer).replace(/\n/g, '<br>')}
                            </div>
                        </div>
                    </div>
                `;
            });
            questionsHtml += '</div>';
        }
        
        // Assemble Card
        subtopicCard.innerHTML = headerHtml + explanationHtml + codeHtml + calloutsHtml + questionsHtml;
        subtopicsContainer.appendChild(subtopicCard);
    });
}

function renderDay17Revision(day) {
    const revisionCard = document.createElement('section');
    revisionCard.className = 'subtopic-card';
    
    // Quick Reference Table
    let quickRefHtml = `
        <div class="questions-section">
            <span class="questions-section-title">Quick Reference Roadmap</span>
            <div style="overflow-x: auto; border: 1px solid var(--border-color); border-radius: var(--radius-md);">
                <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 14px;">
                    <thead>
                        <tr style="background-color: var(--bg-hover); border-bottom: 1px solid var(--border-color);">
                            <th style="padding: 12px 16px; font-weight: 700; width: 80px;">Day</th>
                            <th style="padding: 12px 16px; font-weight: 700; width: 220px;">Topic</th>
                            <th style="padding: 12px 16px; font-weight: 700;">Key Core Takeaways</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${day.quick_reference.map(ref => `
                            <tr style="border-bottom: 1px solid var(--border-color); cursor: pointer;" onclick="loadDay(${ref.day - 1})">
                                <td style="padding: 12px 16px; font-weight: 600; color: var(--brand-primary-dark);">Day ${ref.day}</td>
                                <td style="padding: 12px 16px; font-weight: 600;">${ref.topic}</td>
                                <td style="padding: 12px 16px; color: var(--text-secondary);">
                                    <ul style="padding-left: 16px;">
                                        ${ref.key_points.map(pt => `<li style="margin-bottom: 4px;">${escapeHtmlText(pt)}</li>`).join('')}
                                    </ul>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        </div>
    `;

    // Revision Cheat Sheet Checklist
    let cheatSheetHtml = `
        <div class="callout-box tips" style="margin-top: 12px;">
            <div class="callout-title" style="font-size: 16px;">
                <i class="fa-solid fa-circle-check"></i> Essential C++ Cheat Sheet Rules
            </div>
            <ul class="callout-list" style="font-size: 14.5px;">
                ${day.cheat_sheet.map(item => `<li>${escapeHtmlText(item)}</li>`).join('')}
            </ul>
        </div>
    `;

    // Cross-Topic Questions Accordion
    let crossTopicHtml = '';
    if (day.cross_topic_questions && day.cross_topic_questions.length > 0) {
        crossTopicHtml += `
            <div class="questions-section" style="margin-top: 24px;">
                <span class="questions-section-title">Deep Cross-Topic Integration Q&A</span>
                ${day.cross_topic_questions.map(q => `
                    <div class="question-accordion">
                        <div class="question-header" onclick="toggleAccordion(this)">
                            <span class="question-text" style="font-weight: 700; color: var(--text-primary);">
                                ${escapeHtmlText(q.question)}
                                <span style="display: block; font-size: 11px; font-weight: 500; color: var(--text-muted); margin-top: 4px;">
                                    Topics: ${q.topics_covered.join(', ')}
                                </span>
                            </span>
                            <span class="question-arrow"><i class="fa-solid fa-chevron-down"></i></span>
                        </div>
                        <div class="question-answer-panel">
                            <div class="question-answer-content">
                                ${escapeHtmlText(q.answer).replace(/\n/g, '<br>')}
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    revisionCard.innerHTML = quickRefHtml + cheatSheetHtml + crossTopicHtml;
    subtopicsContainer.appendChild(revisionCard);
}

function handleCheckboxChange(dayNum, index, checkbox) {
    const label = document.getElementById(`label-check-${dayNum}-${index}`);
    if (checkbox.checked) {
        label.classList.add('completed');
        label.querySelector('span').textContent = 'Completed';
        toggleSubtopicProgress(dayNum, index, true);
    } else {
        label.classList.remove('completed');
        label.querySelector('span').textContent = 'Mark Complete';
        toggleSubtopicProgress(dayNum, index, false);
    }
}

/* -------------------------------------------------------------
 * Accordion Handling (Answers Reveal)
 * ------------------------------------------------------------- */
function toggleAccordion(header) {
    const accordion = header.parentElement;
    const panel = header.nextElementSibling;
    
    // Toggle active state
    accordion.classList.toggle('active');
    
    if (accordion.classList.contains('active')) {
        panel.style.maxHeight = panel.scrollHeight + "px";
        // Listen for internal clicks in panels to adjust size if nested (though not nested here)
    } else {
        panel.style.maxHeight = null;
    }
}

/* -------------------------------------------------------------
 * Clipboard & Toast Notification
 * ------------------------------------------------------------- */
function copyCode(codeId) {
    const codeElement = document.getElementById(codeId);
    if (!codeElement) return;
    
    // Get text content (ignoring formatting tags)
    const codeText = codeElement.textContent;
    
    navigator.clipboard.writeText(codeText)
        .then(() => {
            showToast('Code copied to clipboard!');
        })
        .catch(err => {
            console.error('Failed to copy: ', err);
            showToast('Failed to copy code.');
        });
}

function showToast(message) {
    toastMessage.textContent = message;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 2500);
}

/* -------------------------------------------------------------
 * Search Functionality
 * ------------------------------------------------------------- */
function performSearch(query) {
    if (!db || !query) {
        clearSearch();
        return;
    }
    
    query = query.trim().toLowerCase();
    if (query.length < 2) return;
    
    clearSearchBtn.style.display = 'block';
    contentCard.style.display = 'none';
    searchResultsView.style.display = 'block';
    searchQueryText.textContent = query;
    searchResultsList.innerHTML = '';
    
    let matches = [];
    
    db.days.forEach((day, dayIdx) => {
        // Search day topic
        if (day.topic.toLowerCase().includes(query)) {
            matches.push({
                type: 'Day Topic',
                title: `Day ${day.day} — ${day.topic}`,
                snippet: `Day study topic covers ${day.topic}.`,
                dayIndex: dayIdx,
                subtopicIndex: null
            });
        }
        
        // Search subtopics
        const subtopics = day.subtopics || [];
        subtopics.forEach((sub, subIdx) => {
            let found = false;
            let snippet = '';
            
            if (sub.title.toLowerCase().includes(query)) {
                found = true;
                snippet = sub.explanation.substring(0, 140) + '...';
            } else if (sub.explanation.toLowerCase().includes(query)) {
                found = true;
                const idx = sub.explanation.toLowerCase().indexOf(query);
                const start = Math.max(0, idx - 40);
                const end = Math.min(sub.explanation.length, idx + query.length + 80);
                snippet = (start > 0 ? '...' : '') + sub.explanation.substring(start, end) + (end < sub.explanation.length ? '...' : '');
            } else {
                // Search code inside examples
                const examples = sub.examples || [];
                for (let i = 0; i < examples.length; i++) {
                    if (examples[i].code.toLowerCase().includes(query) || (examples[i].title && examples[i].title.toLowerCase().includes(query))) {
                        found = true;
                        snippet = `Found inside code example: "<strong>${examples[i].title || 'Example'}</strong>"`;
                        break;
                    }
                }
            }
            
            // Search Q&A
            if (!found && sub.questions) {
                for (let i = 0; i < sub.questions.length; i++) {
                    if (sub.questions[i].question.toLowerCase().includes(query) || sub.questions[i].answer.toLowerCase().includes(query)) {
                        found = true;
                        snippet = `Found inside Interview Q&A: "<em>${sub.questions[i].question}</em>"`;
                        break;
                    }
                }
            }
            
            if (found) {
                matches.push({
                    type: 'Subtopic Detail',
                    title: `Day ${day.day} — ${sub.title}`,
                    snippet: snippet,
                    dayIndex: dayIdx,
                    subtopicIndex: subIdx
                });
            }
        });
        
        // Search revision day specifically
        if (day.day === 17) {
            const cheatSheet = day.cheat_sheet || [];
            cheatSheet.forEach(item => {
                if (item.toLowerCase().includes(query)) {
                    matches.push({
                        type: 'Cheat Sheet Card',
                        title: `Day 17 Cheat Sheet`,
                        snippet: `... ${item} ...`,
                        dayIndex: dayIdx,
                        subtopicIndex: null
                    });
                }
            });
            
            const crossTopic = day.cross_topic_questions || [];
            crossTopic.forEach(q => {
                if (q.question.toLowerCase().includes(query) || q.answer.toLowerCase().includes(query)) {
                    matches.push({
                        type: 'Cross-Topic Q&A',
                        title: `Day 17 Integration Question`,
                        snippet: `Question: ${q.question}`,
                        dayIndex: dayIdx,
                        subtopicIndex: null
                    });
                }
            });
        }
    });
    
    // Render Results
    searchResultsStats.textContent = `Found ${matches.length} matches`;
    
    if (matches.length === 0) {
        searchResultsList.innerHTML = `
            <div class="loading-state">
                <i class="fa-solid fa-magnifying-glass-minus" style="font-size: 40px; color: var(--text-muted);"></i>
                <p>No results found for "${escapeHtmlText(query)}". Try another C++ term!</p>
            </div>
        `;
        return;
    }
    
    matches.forEach(match => {
        const card = document.createElement('div');
        card.className = 'result-card';
        card.innerHTML = `
            <div class="result-meta">
                <span class="result-day-badge">Day ${match.dayIndex + 1}</span>
                <span class="result-type-badge">${match.type}</span>
            </div>
            <h4 class="result-title">${highlightTerm(match.title, query)}</h4>
            <p class="result-snippet">${highlightTerm(match.snippet, query)}</p>
        `;
        
        card.addEventListener('click', () => {
            loadDay(match.dayIndex);
            if (match.subtopicIndex !== null) {
                setTimeout(() => {
                    const el = document.getElementById(`subtopic-${match.subtopicIndex}`);
                    if (el) {
                        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        el.classList.add('active-highlight-glow');
                        setTimeout(() => el.classList.remove('active-highlight-glow'), 2000);
                    }
                }, 150);
            }
        });
        
        searchResultsList.appendChild(card);
    });
}

function highlightTerm(text, query) {
    if (!text) return '';
    // Prevent highlighting HTML tags directly
    const escaped = text.replace(/<br>/g, '__BR_TAG__');
    const regex = new RegExp(`(${escapeRegExp(query)})`, 'gi');
    const highlighted = escaped.replace(regex, '<mark class="search-highlight">$1</mark>');
    return highlighted.replace(/__BR_TAG__/g, '<br>');
}

function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function clearSearch() {
    searchInput.value = '';
    clearSearchBtn.style.display = 'none';
    searchResultsView.style.display = 'none';
    contentCard.style.display = 'block';
}

/* -------------------------------------------------------------
 * Micro-Syntax Highlighter for C++
 * ------------------------------------------------------------- */
function highlightCpp(code) {
    const escape = (text) => text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    
    // Tokenization RegExp: strings, comments, preprocessor, std namespace types, keywords, numbers, punctuation, identifiers, whitespace
    const tokenRegex = /(?:\/\/[^\n]*)|(?:\/\*(?:[^*]|\*+[^\/*])*\*+\/)|(?:"(?:[^"\\]|\\.)*")|(?:'(?:[^'\\]|\\.)*')|(?:\b\d+f?|\b\d+\.\d+f?|\b0x[0-9a-fA-F]+\b)|(?:\bstd::[a-zA-Z0-9_]+\b)|(?:\b[a-zA-Z_][a-zA-Z0-9_]*\b)|(?:#[a-zA-Z_]+)|(?:[{}()\[\]+\-*\/%&|^=<>!~:;,?.]+)|(?:\s+)/g;
    
    const keywords = new Set([
        'template', 'typename', 'class', 'struct', 'union', 'enum',
        'const', 'constexpr', 'consteval', 'constinit', 'inline', 'static', 
        'extern', 'thread_local', 'return', 'if', 'else', 'for', 'while', 'do', 'switch', 
        'case', 'default', 'break', 'continue', 'throw', 'try', 'catch', 'noexcept',
        'static_cast', 'dynamic_cast', 'const_cast', 'reinterpret_cast', 'using', 'namespace',
        'delete', 'new', 'explicit', 'operator', 'virtual', 'override', 'final', 'concept', 
        'requires', 'co_await', 'co_yield', 'co_return', 'import', 'module', 'public', 'private', 'protected'
    ]);
    
    const types = new Set([
        'int', 'double', 'float', 'bool', 'char', 'void', 'size_t',
        'uint32_t', 'uint64_t', 'int32_t', 'int64_t', 'wchar_t', 'char16_t',
        'char32_t', 'nullptr_t', 'string', 'vector', 'pair', 'unique_ptr',
        'shared_ptr', 'weak_ptr', 'thread', 'jthread', 'atomic', 'mutex',
        'lock_guard', 'unique_lock', 'scoped_lock', 'expected', 'optional',
        'variant', 'any', 'span', 'string_view', 'ostream', 'istream', 'exception'
    ]);
    
    let result = '';
    let match;
    tokenRegex.lastIndex = 0;
    
    while ((match = tokenRegex.exec(code)) !== null) {
        const token = match[0];
        
        if (token.startsWith('//') || token.startsWith('/*')) {
            result += `<span class="code-comment">${escape(token)}</span>`;
        } else if (token.startsWith('"') || token.startsWith("'")) {
            result += `<span class="code-string">${escape(token)}</span>`;
        } else if (token.startsWith('#')) {
            result += `<span class="code-preprocessor">${escape(token)}</span>`;
        } else if (/^\b\d+/.test(token)) {
            result += `<span class="code-number">${escape(token)}</span>`;
        } else if (token.startsWith('std::')) {
            const name = token.substring(5);
            if (types.has(name)) {
                result += `<span class="code-std">std::</span><span class="code-type">${escape(name)}</span>`;
            } else {
                result += `<span class="code-std">std::</span>${escape(name)}`;
            }
        } else if (keywords.has(token)) {
            result += `<span class="code-keyword">${escape(token)}</span>`;
        } else if (types.has(token)) {
            result += `<span class="code-type">${escape(token)}</span>`;
        } else {
            result += escape(token);
        }
    }
    
    return result || escape(code);
}

/* -------------------------------------------------------------
 * Event Listeners & Utilities
 * ------------------------------------------------------------- */
function setupEventListeners() {
    // Search listener
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value;
        if (query.trim() === '') {
            clearSearch();
        } else {
            performSearch(query);
        }
    });

    clearSearchBtn.addEventListener('click', clearSearch);
    
    if (document.getElementById('closeSearchBtn')) {
        document.getElementById('closeSearchBtn').addEventListener('click', clearSearch);
    }

    // Reset Progress
    resetProgressBtn.addEventListener('click', () => {
        if (confirm('Are you sure you want to reset all your C++ study progress? This cannot be undone.')) {
            progress = {};
            saveProgress();
            updateOverallProgress();
            
            // Reload active day
            loadDay(activeDayIndex);
            
            showToast('Progress reset successfully!');
        }
    });

    // Mobile Sidebar Drawer
    menuToggleBtn.addEventListener('click', openSidebar);
    sidebarCloseBtn.addEventListener('click', closeSidebar);
    backdrop.addEventListener('click', closeSidebar);
}

function openSidebar() {
    sidebar.classList.add('open');
    backdrop.classList.add('active');
}

function closeSidebar() {
    sidebar.classList.remove('open');
    backdrop.classList.remove('active');
}

function escapeHtmlText(text) {
    if (!text) return '';
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
}
