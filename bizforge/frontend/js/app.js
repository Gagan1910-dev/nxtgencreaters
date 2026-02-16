const API_URL = "http://localhost:8000/api/v1";

document.addEventListener("DOMContentLoaded", () => {
    const generateBtn = document.getElementById("generate-btn");
    const resetBtnHero = document.getElementById("reset-btn-hero");
    const resetBtnResults = document.getElementById("reset-btn-results");
    const businessIdeaInput = document.getElementById("business-idea");
    const industryInput = document.getElementById("industry");
    const toneSelect = document.getElementById("tone");

    // Sections
    const heroSection = document.getElementById("hero-section");
    const resultsSection = document.getElementById("results-section");

    // Results Containers
    // Results Containers
    const identityContainer = document.getElementById("identity-results");
    const socialContainer = document.getElementById("social-results");
    const logoContainer = document.getElementById("logo-result");
    const emailContainer = document.querySelector(".email-preview");
    const summaryContainer = document.getElementById("brand-summary");
    const sentimentContainer = document.getElementById("sentiment-result");
    const paletteContainer = document.getElementById("palette-result");

    // Palette Elements
    const previewThemeBtn = document.getElementById("preview-theme-btn");
    const resetThemeBtn = document.getElementById("reset-theme-btn");
    let currentPalette = []; // Store for preview

    // Chat Elements
    const chatInput = document.getElementById("chat-input");
    const chatSendBtn = document.getElementById("chat-send-btn");
    const chatWindow = document.getElementById("chat-window");

    // Logo Controls
    const regenerateLogoBtn = document.getElementById("regenerate-logo-btn");
    const downloadLogoBtn = document.getElementById("download-logo-btn");
    let currentLogoData = {}; // Store current logo state

    generateBtn.addEventListener("click", handleGeneration);

    // Attach event listeners to BOTH reset buttons
    if (resetBtnHero) resetBtnHero.addEventListener("click", resetApp);
    if (resetBtnResults) resetBtnResults.addEventListener("click", resetApp);

    chatSendBtn.addEventListener("click", handleChat);

    // Logo Controls
    if (regenerateLogoBtn) {
        regenerateLogoBtn.addEventListener("click", handleLogoRegeneration);
    }
    if (downloadLogoBtn) {
        downloadLogoBtn.addEventListener("click", downloadLogo);
    }

    // Theme Controls
    previewThemeBtn.addEventListener("click", () => applyTheme(currentPalette));
    resetThemeBtn.addEventListener("click", resetTheme);

    // Navbar Interactivity
    const navAboutBtn = document.getElementById("nav-about-btn");
    const navStartBtn = document.getElementById("nav-start-btn");
    const aboutModal = document.getElementById("about-modal");
    const closeModalBtn = document.getElementById("close-modal-btn");

    if (navStartBtn) {
        navStartBtn.addEventListener("click", (e) => {
            e.preventDefault();
            document.getElementById("business-idea").focus();
            document.getElementById("hero-section").scrollIntoView({ behavior: "smooth" });
        });
    }

    if (navAboutBtn && aboutModal && closeModalBtn) {
        navAboutBtn.addEventListener("click", () => {
            aboutModal.classList.remove("hidden");
        });

        closeModalBtn.addEventListener("click", () => {
            aboutModal.classList.add("hidden");
        });

        // Close on outside click
        aboutModal.addEventListener("click", (e) => {
            if (e.target === aboutModal) {
                aboutModal.classList.add("hidden");
            }
        });
    }

    async function handleGeneration() {
        const idea = businessIdeaInput.value;
        const industry = industryInput.value;
        const tone = toneSelect.value;

        if (!idea || !industry) {
            alert("Please enter both a business idea and industry.");
            return;
        }

        setLoading(true);

        try {
            const response = await fetch(`${API_URL}/generate`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ business_idea: idea, industry: industry, tone: tone })
            });

            if (!response.ok) throw new Error("Failed to generate brand kit");

            const data = await response.json();
            renderResults(data);

            heroSection.classList.add("hidden");
            resultsSection.classList.remove("hidden");

        } catch (error) {
            console.error(error);
            alert("Connection Error. Ensure Backend is running.");
        } finally {
            setLoading(false);
        }
    }

    function renderResults(data) {
        // 1. Identity
        identityContainer.innerHTML = "";
        data.identity.forEach(id => {
            const div = document.createElement("div");
            div.className = "identity-item";
            div.innerHTML = `
                <div class="identity-name">${id.name}</div>
                <div class="identity-tagline">${id.tagline}</div>
                <div style="font-size: 0.8rem; color: #aaa; margin-top: 5px;">Score: ${id.score}/100</div>
            `;
            identityContainer.appendChild(div);
        });

        // 2. Visuals
        logoContainer.innerHTML = `<img src="${data.logo_url}" alt="Generated Logo" />`;

        // Store for preview
        currentPalette = data.color_palette;
        resetThemeBtn.style.display = 'none'; // Hide reset on new generation
        previewThemeBtn.style.display = 'block';

        const roles = ["Primary", "Secondary", "Text/Dark", "Background", "Accent"];

        paletteContainer.innerHTML = data.color_palette.map((color, index) => {
            const role = roles[index] || "Support";
            return `
            <div class="color-card" onclick="previewSingleColor('${color}')" style="cursor: pointer;" title="Click to preview this color as Primary">
                <div class="color-preview-box" style="background-color: ${color};"></div>
                <div class="color-info">
                    <div class="color-role">${role}</div>
                    <span class="color-hex">${color}</span>
                    <button class="btn-copy" onclick="event.stopPropagation(); copyToClipboard('${color}', this)">
                        Copy HEX
                    </button>
                </div>
            </div>
            `;
        }).join("");

        // 3. Analysis
        summaryContainer.textContent = data.brand_summary;

        // Friendly Sentiment Message
        if (!data.sentiment_analysis || data.sentiment_analysis.toLowerCase().includes("inconclusive")) {
            sentimentContainer.innerHTML = `<span style="color: var(--text-muted)">More details will help us provide better brand insights. Try expanding your description!</span>`;
        } else {
            sentimentContainer.textContent = data.sentiment_analysis;
        }

        // 4. Social
        socialContainer.innerHTML = "";
        data.social_media.forEach(social => {
            const div = document.createElement("div");
            div.style.marginBottom = "1rem";
            div.style.borderBottom = "1px solid rgba(255,255,255,0.1)";
            div.style.paddingBottom = "1rem";
            div.innerHTML = `
                <strong style="color: var(--primary-color)">${social.platform}</strong>
                <p style="font-size: 0.9rem; margin: 0.5rem 0;">${social.content}</p>
                <div style="color: var(--accent-color); font-size: 0.8rem;">${social.hashtags.join(" ")}</div>
            `;
            socialContainer.appendChild(div);
        });

        // 5. Email
        if (emailContainer) emailContainer.textContent = data.email_copy;

        // 6. Store logo state and show controls
        currentLogoData = {
            name: data.identity[0].name,
            industry: businessIdeaInput.value.split(',')[0] || industryInput.value,
            tone: toneSelect.value,
            color_palette: data.color_palette,
            url: data.logo_url
        };

        // Show logo control buttons
        if (regenerateLogoBtn) regenerateLogoBtn.style.display = 'inline-block';
        if (downloadLogoBtn) downloadLogoBtn.style.display = 'inline-block';
    }

    async function handleChat() {
        const msg = chatInput.value;
        if (!msg) return;

        // Append User Message
        addChatMessage(msg, 'user');

        chatInput.value = "";

        // Show typing indicator (optional improvement)
        const loadingId = addChatMessage("Thinking...", 'ai', true);

        try {
            const response = await fetch(`${API_URL}/chat`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: msg, context: summaryContainer.textContent })
            });

            const data = await response.json();

            // Remove loading and show real response
            const loader = document.getElementById(loadingId);
            if (loader) loader.remove();

            addChatMessage(data.response, 'ai');

        } catch (error) {
            console.error(error);
            const loader = document.getElementById(loadingId);
            if (loader) loader.textContent = "Error: Could not reach assistant.";
        }
    }

    function addChatMessage(text, sender, isLoading = false) {
        const div = document.createElement("div");
        div.className = `chat-message ${sender}`;
        if (isLoading) div.id = `msg-${Date.now()}`;

        // Simple Markdown Parsing for Bold and Newlines
        // 1. Bold: **text** -> <strong>text</strong>
        let formatted = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        // 2. Newlines -> <br>
        formatted = formatted.replace(/\n/g, '<br>');
        // 3. Bullet points (• or - ) -> handled by CSS if structure is right, but let's simple fix
        // If the backend sends lines starting with -, wrap in list? 
        // For simplicity, just replacing "- " with "• " for visual consistency if needed

        div.innerHTML = formatted;

        chatWindow.appendChild(div);
        chatWindow.scrollTop = chatWindow.scrollHeight;
        return div.id;
    }

    function setLoading(isLoading) {
        const btnText = generateBtn.querySelector(".btn-text");
        const loader = generateBtn.querySelector(".btn-loader");

        if (isLoading) {
            btnText.style.display = "none";
            loader.classList.remove("hidden");
            loader.classList.add("loader");
            generateBtn.disabled = true;
        } else {
            btnText.style.display = "block";
            loader.classList.add("hidden");
            loader.classList.remove("loader");
            generateBtn.disabled = false;
        }
    }

    function resetApp() {
        businessIdeaInput.value = "";
        industryInput.value = "";
        resultsSection.classList.add("hidden");
        heroSection.classList.remove("hidden");
        // Clear results
        identityContainer.innerHTML = "";
        if (emailContainer) emailContainer.textContent = "";
        logoContainer.innerHTML = '<div class="placeholder-skeleton"></div>';
        chatWindow.innerHTML = '<div class="chat-message system">Hello! I am your AI Brand Strategist. Ask me anything about your new brand.</div>';
        resetTheme();
        // Hide logo controls
        if (regenerateLogoBtn) regenerateLogoBtn.style.display = 'none';
        if (downloadLogoBtn) downloadLogoBtn.style.display = 'none';
    }

    async function handleLogoRegeneration() {
        if (!currentLogoData.name) return;

        regenerateLogoBtn.disabled = true;
        regenerateLogoBtn.textContent = "Generating...";
        logoContainer.innerHTML = '<div class="placeholder-skeleton"></div>';

        try {
            const response = await fetch(`${API_URL}/regenerate-logo`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(currentLogoData)
            });

            if (!response.ok) throw new Error("Failed to regenerate logo");

            const data = await response.json();
            logoContainer.innerHTML = `<img src="${data.logo_url}" alt="Regenerated Logo" />`;
            currentLogoData.url = data.logo_url;

        } catch (error) {
            console.error(error);
            alert("Failed to regenerate logo. Please try again.");
        } finally {
            regenerateLogoBtn.disabled = false;
            regenerateLogoBtn.textContent = "↻ Regenerate Logo";
        }
    }

    function downloadLogo() {
        if (!currentLogoData.url) return;

        const link = document.createElement('a');
        link.href = currentLogoData.url;
        link.download = `${currentLogoData.name.replace(/\s+/g, '_')}_logo.png`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    // Design System Functions
    window.copyToClipboard = function (text, btnElement) {
        navigator.clipboard.writeText(text);
        const originalText = btnElement.textContent;
        btnElement.textContent = "Copied!";
        btnElement.style.borderColor = "var(--accent-color)";
        btnElement.style.color = "var(--accent-color)";

        setTimeout(() => {
            btnElement.textContent = originalText;
            btnElement.style.borderColor = "";
            btnElement.style.color = "";
        }, 2000);
    };

    // Expose to window for onclick events
    window.previewSingleColor = function (color) {
        document.documentElement.style.setProperty('--primary-color', color);
        resetThemeBtn.style.display = 'block';
    };

    window.fillInput = function (text) {
        businessIdeaInput.value = text;
        validateInput(); // Trigger validation UI clear
    };

    // Input Validation Logic
    businessIdeaInput.addEventListener("input", validateInput);

    function validateInput() {
        const hint = document.getElementById("input-hint");
        if (!hint) return;

        const words = businessIdeaInput.value.trim().split(/\s+/).filter(w => w.length > 0);

        if (words.length > 0 && words.length < 3) {
            hint.classList.remove("hidden");
        } else {
            hint.classList.add("hidden");
        }
    }

    function applyTheme(palette) {
        if (!palette || palette.length < 5) return;

        // Map palette to variables: 0:Primary, 4:Accent
        document.documentElement.style.setProperty('--primary-color', palette[0]);
        document.documentElement.style.setProperty('--accent-color', palette[4]);

        previewThemeBtn.style.display = 'none';
        resetThemeBtn.style.display = 'block';
    }

    function resetTheme() {
        document.documentElement.style.setProperty('--primary-color', '#6366f1');
        document.documentElement.style.setProperty('--accent-color', '#ec4899');

        if (previewThemeBtn) previewThemeBtn.style.display = 'block';
        if (resetThemeBtn) resetThemeBtn.style.display = 'none';
    }
});
