/**
 * NETRUNNER: The Nautobot Protocol
 * LitRPG Interactive System
 */

// ============================================
// CHARACTER STATE (persisted in localStorage)
// ============================================
const DEFAULT_CHARACTER = {
    name: "Unknown",
    class: "Netrunner",
    level: 1,
    xp: 0,
    xpToNext: 100,
    stats: {
        INT: 8,
        FOCUS: 6,
        MEMORY: 7,
        STEALTH: 5,
        REPUTATION: 0
    },
    skills: [],
    questsCompleted: [],
    currentQuest: null,
    choices: {},
    flags: {}
};

function getCharacter() {
    const saved = localStorage.getItem('netrunner_character');
    return saved ? JSON.parse(saved) : { ...DEFAULT_CHARACTER };
}

function saveCharacter(char) {
    localStorage.setItem('netrunner_character', JSON.stringify(char));
}

function resetCharacter() {
    localStorage.removeItem('netrunner_character');
    location.reload();
}

// ============================================
// SYSTEM MESSAGES
// ============================================
function showSystemMessage(message, type = 'info') {
    const container = document.getElementById('system-messages') || createSystemContainer();
    const msg = document.createElement('div');
    msg.className = `system-message system-${type}`;
    msg.innerHTML = `<span class="system-prefix">[SYSTEM]</span> ${message}`;
    container.appendChild(msg);
    
    // Animate in
    setTimeout(() => msg.classList.add('visible'), 10);
    
    // Auto-remove after delay
    setTimeout(() => {
        msg.classList.remove('visible');
        setTimeout(() => msg.remove(), 500);
    }, 4000);
}

function createSystemContainer() {
    const container = document.createElement('div');
    container.id = 'system-messages';
    document.body.appendChild(container);
    return container;
}

// ============================================
// SKILL ACQUISITION
// ============================================
function acquireSkill(skillName, description) {
    const char = getCharacter();
    if (!char.skills.includes(skillName)) {
        char.skills.push(skillName);
        saveCharacter(char);
        showSkillPopup(skillName, description);
    }
}

function showSkillPopup(skillName, description) {
    const popup = document.createElement('div');
    popup.className = 'skill-popup';
    popup.innerHTML = `
        <div class="skill-popup-content">
            <div class="skill-popup-header">★ SKILL ACQUIRED ★</div>
            <div class="skill-popup-name">${skillName}</div>
            <div class="skill-popup-desc">${description}</div>
            <button onclick="this.parentElement.parentElement.remove()">ACKNOWLEDGE</button>
        </div>
    `;
    document.body.appendChild(popup);
    setTimeout(() => popup.classList.add('visible'), 10);
}

// ============================================
// XP AND LEVELING
// ============================================
function gainXP(amount) {
    const char = getCharacter();
    char.xp += amount;
    
    showSystemMessage(`+${amount} XP gained!`, 'xp');
    
    // Check for level up
    while (char.xp >= char.xpToNext) {
        char.xp -= char.xpToNext;
        char.level++;
        char.xpToNext = Math.floor(char.xpToNext * 1.5);
        showLevelUp(char.level);
    }
    
    saveCharacter(char);
    updateStatusDisplay();
}

function showLevelUp(newLevel) {
    const popup = document.createElement('div');
    popup.className = 'levelup-popup';
    popup.innerHTML = `
        <div class="levelup-content">
            <div class="levelup-flash"></div>
            <div class="levelup-text">LEVEL UP!</div>
            <div class="levelup-level">LEVEL ${newLevel}</div>
            <div class="levelup-stats">+1 to all stats</div>
        </div>
    `;
    document.body.appendChild(popup);
    
    // Update stats
    const char = getCharacter();
    Object.keys(char.stats).forEach(stat => char.stats[stat]++);
    saveCharacter(char);
    
    setTimeout(() => popup.classList.add('visible'), 10);
    setTimeout(() => {
        popup.classList.remove('visible');
        setTimeout(() => popup.remove(), 500);
    }, 3000);
}

// ============================================
// STATUS DISPLAY
// ============================================
function updateStatusDisplay() {
    const char = getCharacter();
    const statusEl = document.getElementById('character-status');
    if (!statusEl) return;
    
    statusEl.innerHTML = `
        <div class="status-header">
            <span class="status-name">${char.name}</span>
            <span class="status-class">${char.class} Lv.${char.level}</span>
        </div>
        <div class="status-xp">
            <div class="xp-bar-bg">
                <div class="xp-bar-fill" style="width: ${(char.xp / char.xpToNext) * 100}%"></div>
            </div>
            <span class="xp-text">${char.xp}/${char.xpToNext} XP</span>
        </div>
        <div class="status-stats">
            ${Object.entries(char.stats).map(([stat, val]) => 
                `<div class="stat-item"><span class="stat-name">${stat}</span><span class="stat-value">${val}</span></div>`
            ).join('')}
        </div>
    `;
}

// ============================================
// DIALOGUE SYSTEM
// ============================================
function showDialogue(speaker, text, portrait = null) {
    return new Promise(resolve => {
        const dialogueBox = document.createElement('div');
        dialogueBox.className = 'dialogue-box';
        dialogueBox.innerHTML = `
            ${portrait ? `<div class="dialogue-portrait" style="background-image: url('${portrait}')"></div>` : ''}
            <div class="dialogue-content">
                <div class="dialogue-speaker">${speaker}</div>
                <div class="dialogue-text"></div>
                <div class="dialogue-continue">▼ Click to continue</div>
            </div>
        `;
        document.body.appendChild(dialogueBox);
        
        // Typewriter effect
        const textEl = dialogueBox.querySelector('.dialogue-text');
        let i = 0;
        const typewriter = setInterval(() => {
            textEl.textContent += text[i];
            i++;
            if (i >= text.length) clearInterval(typewriter);
        }, 30);
        
        setTimeout(() => dialogueBox.classList.add('visible'), 10);
        
        dialogueBox.onclick = () => {
            clearInterval(typewriter);
            textEl.textContent = text;
            dialogueBox.classList.remove('visible');
            setTimeout(() => {
                dialogueBox.remove();
                resolve();
            }, 300);
        };
    });
}

// ============================================
// CHOICES
// ============================================
function showChoice(prompt, options) {
    return new Promise(resolve => {
        const choiceBox = document.createElement('div');
        choiceBox.className = 'choice-box';
        choiceBox.innerHTML = `
            <div class="choice-prompt">${prompt}</div>
            <div class="choice-options">
                ${options.map((opt, i) => 
                    `<button class="choice-btn" data-index="${i}">${opt.text}</button>`
                ).join('')}
            </div>
        `;
        document.body.appendChild(choiceBox);
        setTimeout(() => choiceBox.classList.add('visible'), 10);
        
        choiceBox.querySelectorAll('.choice-btn').forEach(btn => {
            btn.onclick = () => {
                const index = parseInt(btn.dataset.index);
                const char = getCharacter();
                if (options[index].flag) {
                    char.flags[options[index].flag] = true;
                    saveCharacter(char);
                }
                choiceBox.classList.remove('visible');
                setTimeout(() => {
                    choiceBox.remove();
                    resolve(index);
                }, 300);
            };
        });
    });
}

// ============================================
// QUEST LOG
// ============================================
function updateQuestLog(questId, status, objectives = []) {
    const char = getCharacter();
    char.currentQuest = { id: questId, status, objectives };
    saveCharacter(char);
    
    const logEl = document.getElementById('quest-log');
    if (!logEl) return;
    
    logEl.innerHTML = `
        <div class="quest-log-header">◆ ACTIVE QUEST ◆</div>
        <div class="quest-log-title">${questId}</div>
        <div class="quest-log-status">${status}</div>
        <div class="quest-log-objectives">
            ${objectives.map(obj => 
                `<div class="quest-objective ${obj.complete ? 'complete' : ''}">
                    <span class="objective-check">${obj.complete ? '☑' : '☐'}</span>
                    ${obj.text}
                </div>`
            ).join('')}
        </div>
    `;
}

function completeQuest(questId) {
    const char = getCharacter();
    if (!char.questsCompleted.includes(questId)) {
        char.questsCompleted.push(questId);
        saveCharacter(char);
        showSystemMessage(`Quest Complete: ${questId}`, 'quest');
    }
}

// ============================================
// INTERACTIVE TERMINALS
// ============================================
function initTerminals() {
    document.querySelectorAll('.interactive-terminal').forEach(term => {
        const input = term.querySelector('.terminal-input');
        const output = term.querySelector('.terminal-output');
        const expected = term.dataset.expected;
        
        if (input) {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    const value = input.value.trim();
                    if (value === expected) {
                        output.innerHTML += `<div class="terminal-success">✓ Correct! Command executed.</div>`;
                        term.classList.add('completed');
                        if (term.dataset.skill) {
                            acquireSkill(term.dataset.skill, term.dataset.skillDesc || '');
                        }
                        if (term.dataset.xp) {
                            gainXP(parseInt(term.dataset.xp));
                        }
                    } else {
                        output.innerHTML += `<div class="terminal-error">✗ Invalid command. Try again.</div>`;
                    }
                    input.value = '';
                }
            });
        }
    });
}

// ============================================
// COLLAPSIBLE SECTIONS
// ============================================
function initCollapsibles() {
    document.querySelectorAll('.collapsible-trigger').forEach(trigger => {
        trigger.addEventListener('click', () => {
            const content = trigger.nextElementSibling;
            trigger.classList.toggle('open');
            content.classList.toggle('open');
        });
    });
}

// ============================================
// SCROLL REVEALS
// ============================================
function initScrollReveals() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                
                // Trigger any associated events
                if (entry.target.dataset.onReveal) {
                    eval(entry.target.dataset.onReveal);
                }
            }
        });
    }, { threshold: 0.3 });
    
    document.querySelectorAll('.scroll-reveal').forEach(el => observer.observe(el));
}

// ============================================
// CHARACTER CREATION
// ============================================
function showCharacterCreation() {
    return new Promise(resolve => {
        const modal = document.createElement('div');
        modal.className = 'character-creation-modal';
        modal.innerHTML = `
            <div class="cc-content">
                <h2>◆ IDENTITY INITIALIZATION ◆</h2>
                <p class="cc-subtitle">Before you jack in, the system requires identification.</p>
                
                <div class="cc-field">
                    <label>HANDLE (Alias)</label>
                    <input type="text" id="cc-name" placeholder="Enter your handle..." maxlength="20">
                </div>
                
                <div class="cc-stats">
                    <p>INITIAL NEURAL SCAN DETECTED:</p>
                    <div class="cc-stat-preview">
                        <span>INT: 8</span>
                        <span>FOCUS: 6</span>
                        <span>MEMORY: 7</span>
                        <span>STEALTH: 5</span>
                    </div>
                </div>
                
                <button id="cc-confirm" class="cyber-btn green">INITIALIZE IDENTITY</button>
            </div>
        `;
        document.body.appendChild(modal);
        setTimeout(() => modal.classList.add('visible'), 10);
        
        document.getElementById('cc-confirm').onclick = () => {
            const name = document.getElementById('cc-name').value.trim() || 'Ghost';
            const char = getCharacter();
            char.name = name;
            saveCharacter(char);
            
            modal.classList.remove('visible');
            setTimeout(() => {
                modal.remove();
                showSystemMessage(`Identity confirmed: ${name}`, 'info');
                resolve(name);
            }, 300);
        };
    });
}

// ============================================
// INITIALIZATION
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    initCollapsibles();
    initTerminals();
    initScrollReveals();
    updateStatusDisplay();
    
    // Show character creation if new player on index
    const char = getCharacter();
    if (char.name === 'Unknown' && document.getElementById('character-creation-trigger')) {
        showCharacterCreation();
    }
});

// Expose functions globally
window.NetRunner = {
    getCharacter,
    saveCharacter,
    resetCharacter,
    showSystemMessage,
    acquireSkill,
    gainXP,
    showDialogue,
    showChoice,
    updateQuestLog,
    completeQuest,
    showCharacterCreation,
    updateStatusDisplay
};

