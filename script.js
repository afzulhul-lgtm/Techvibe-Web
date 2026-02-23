// ===== UNIVERSAL AUTO SYSTEM (Optimized with Fast JSON Loading & VIP Features) =====

const config = {
    folderName: 'articles',      
    itemsPerPage: 15,            
    authorName: 'Sarah Mitchell',
    defaultAuthorImg: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-1.2.1&auto=format&fit=crop&w=150&q=80' 
};

let allArticles = [];
let currentPage = 1;
let currentFilter = 'all'; 

const isArticlePage = window.location.pathname.includes(`/${config.folderName}/`);
const basePath = isArticlePage ? '' : `${config.folderName}/`; 
const linkPrefix = isArticlePage ? '' : `${config.folderName}/`; 
const rootPrefix = isArticlePage ? '../' : ''; 

// CSS INJECTION
const style = document.createElement('style');
style.innerHTML = `
    .sidebar-card { display: flex; gap: 12px; align-items: start; margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px; }
    .sidebar-card:last-child { border-bottom: none; }
    .sidebar-img { width: 80px; height: 60px; flex-shrink: 0; border-radius: 4px; overflow: hidden; background: #ddd; }
    .sidebar-img img { width: 100%; height: 100%; object-fit: cover; transition: opacity 0.3s ease-in-out; }
    .sidebar-info { display: flex; flex-direction: column; }
    .sidebar-info a { color: #fff; font-size: 0.9rem; font-weight: 500; line-height: 1.4; margin-bottom: 5px; text-decoration: none; }
    .sidebar-info a:hover { text-decoration: underline; color: #0066cc; }
    .sidebar-date { font-size: 0.75rem; color: rgba(255,255,255,0.7); }
    .mini-avatar { width: 24px; height: 24px; border-radius: 50%; object-fit: cover; vertical-align: middle; margin-right: 6px; border: 1px solid #ddd; }
    .author-link { cursor: pointer; transition: color 0.2s; text-decoration: none; color: inherit; font-weight:600; }
    .author-link:hover { color: #0066cc; }
    .verified-tick { color: #1da1f2; margin-left: 4px; font-size: 0.8em; }
    .card-author-img { width: 28px; height: 28px; border-radius: 50%; object-fit: cover; margin-right: 8px; border: 1px solid #ddd; }
    .news-meta { display: flex; align-items: center; flex-wrap: wrap; gap: 5px; margin-top:10px; }
    .pagination-controls { grid-column: 1 / -1; display: flex; justify-content: center; gap: 10px; margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; }
    .page-btn { padding: 8px 16px; border: 1px solid #ddd; background: white; cursor: pointer; border-radius: 4px; font-weight: 500; transition: all 0.3s ease; }
    .page-btn:hover { background: #f0f0f0; }
    .page-btn.active { background: #0066cc; color: white; border-color: #0066cc; }
    .notify-popup-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 9999; display: flex; justify-content: center; align-items: center; }
    .notify-popup { background: #fff; padding: 30px; border-radius: 12px; text-align: center; max-width: 400px; width: 90%; }
    .notify-icon { width: 60px; height: 60px; background: #e8f4ff; color: #0066cc; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; margin: 0 auto 15px; }
    .btn-allow { background: #0066cc; color: #fff; border: none; padding: 10px 25px; border-radius: 6px; cursor: pointer; font-weight: 600; }
    .btn-deny { background: #f1f1f1; color: #555; border: none; padding: 10px 25px; border-radius: 6px; cursor: pointer; font-weight: 600; }
    #search-full-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.8); backdrop-filter: blur(10px); z-index: 20000; display: none; justify-content: center; align-items: flex-start; padding-top: 80px; }
    .search-modal { width: 90%; max-width: 650px; background: #fff; border-radius: 15px; overflow: hidden; }
    .search-header { display: flex; align-items: center; padding: 15px 20px; border-bottom: 2px solid #f0f0f0; }
    .search-header input { flex: 1; border: none; outline: none; font-size: 1.2rem; padding: 10px; background:transparent; }
    .close-search-btn { font-size: 1.5rem; color: #999; cursor: pointer; padding: 5px; }
    #search-results-list { max-height: 450px; overflow-y: auto; padding: 10px; }
    .search-result-item { display: flex; gap: 15px; padding: 12px; border-radius: 8px; cursor: pointer; border-bottom: 1px solid #f9f9f9; }
    .search-result-item img { width: 60px; height: 45px; object-fit: cover; border-radius: 4px; }
    .search-result-info h4 { margin: 0; font-size: 1rem; color: #222; }
    .search-result-info p { margin: 4px 0 0; font-size: 0.8rem; color: #0066cc; font-weight: 600; }
`;
document.head.appendChild(style);

// MAIN INIT
document.addEventListener('DOMContentLoaded', async function() {
    highlightActiveMenu();
    updateInnerArticleDate();
    
    await loadArticlesFast(); // Extremely Fast JSON Fetch
    
    const homeContainer = document.getElementById('articles-container');
    if (homeContainer) { currentFilter = 'all'; renderArticles(homeContainer, 'all'); }
    const techContainer = document.getElementById('tech-page-container');
    if (techContainer) { currentFilter = 'Tech'; renderArticles(techContainer, 'Tech'); }
    const latestContainer = document.getElementById('latest-page-container');
    if (latestContainer) { currentFilter = 'all'; renderArticles(latestContainer, 'all'); }

    const sidebar = document.getElementById('sidebar-articles');
    if (sidebar) updateSidebar(sidebar);
    
    updateAlsoRead();
    injectHeaderAuthorPic(); 
    initCommentSystem();
    injectNotificationBell();
    setupCopyLinkButtons();
    initLiveSearchSystem(); 
    initTopBarFeatures(); // <--- NAYA VIP FEATURE
    
    setTimeout(initNotificationPopup, 3000);
});

// VIP TOP BAR FEATURES (Date, Hot News, Dark Mode, Random Article)
function initTopBarFeatures() {
    const dateDisplay = document.getElementById('current-date-display');
    if(dateDisplay) {
        const options = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' };
        dateDisplay.innerHTML = `<i class="far fa-calendar-alt"></i> ${new Date().toLocaleDateString('en-US', options)}`;
    }

    const tickerContainer = document.getElementById('hot-news-ticker');
    if(tickerContainer && allArticles.length > 0) {
        const latestNews = allArticles.slice(0, 5);
        tickerContainer.innerHTML = latestNews.map(art => `<a href="${linkPrefix}${art.filename}"><i class="fas fa-bolt" style="color:#ffcc00; margin-right:5px;"></i>${art.title}</a>`).join('');
    }

    const randomBtn = document.getElementById('random-article-btn');
    if(randomBtn) {
        randomBtn.addEventListener('click', () => {
            if(allArticles.length > 0) {
                const randomArt = allArticles[Math.floor(Math.random() * allArticles.length)];
                window.location.href = `${linkPrefix}${randomArt.filename}`;
            }
        });
    }

    const darkBtn = document.getElementById('dark-mode-toggle');
    if(darkBtn) {
        if(localStorage.getItem('theme') === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
            darkBtn.innerHTML = '<i class="fas fa-sun" style="color:#ffcc00;"></i>';
        }
        darkBtn.addEventListener('click', () => {
            if(document.documentElement.getAttribute('data-theme') === 'dark') {
                document.documentElement.removeAttribute('data-theme');
                localStorage.setItem('theme', 'light');
                darkBtn.innerHTML = '<i class="fas fa-moon"></i>';
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                darkBtn.innerHTML = '<i class="fas fa-sun" style="color:#ffcc00;"></i>';
            }
        });
    }
}

function getTodayDate() {
    const d = new Date();
    return `${d.getDate()} ${d.toLocaleString('default', { month: 'short' })}, ${d.getFullYear()}`;
}

function updateInnerArticleDate() {
    if (isArticlePage) {
        const dateElement = document.querySelector('.publish-date .date');
        if (dateElement) dateElement.innerText = getTodayDate();
    }
}

// OPTIMIZED FAST FETCH
async function loadArticlesFast() {
    try {
        const response = await fetch(basePath + 'data.json');
        if (response.ok) {
            allArticles = await response.json();
            allArticles.sort((a, b) => b.id - a.id); 
        }
    } catch (e) {
        console.error("Error loading articles:", e);
    }
}

function renderArticles(container, filter) {
    container.innerHTML = '';
    let displayList = allArticles;
    if (filter !== 'all') displayList = allArticles.filter(art => art.category.includes(filter));
    
    const totalItems = displayList.length;
    const totalPages = Math.ceil(totalItems / config.itemsPerPage);
    if (currentPage > totalPages) currentPage = 1;

    const start = (currentPage - 1) * config.itemsPerPage;
    const end = start + config.itemsPerPage;
    const paginatedItems = displayList.slice(start, end);

    if (paginatedItems.length === 0) { 
        container.innerHTML = '<div style="padding:40px; text-align:center; grid-column:1/-1;"><h3>No articles found</h3></div>'; return; 
    }

    const articlesHTML = paginatedItems.map(art => {
        let imgSrc = art.image.startsWith('http') ? art.image : `${linkPrefix}${art.image}`;
        return `
            <article class="news-card">
                <div class="article-image" onclick="window.location.href='${linkPrefix}${art.filename}'" style="cursor:pointer">
                    <img src="${imgSrc}" alt="${art.title}" loading="lazy" decoding="async">
                </div>
                <div class="news-content">
                    <h3 class="news-title" onclick="window.location.href='${linkPrefix}${art.filename}'" style="cursor:pointer">${art.title}</h3>
                    <div class="news-meta">
                        <img src="${art.authorImg}" class="card-author-img" alt="author" loading="lazy">
                        <span class="author-link">${art.author} <i class="fas fa-check-circle verified-tick"></i></span>
                        <span class="separator">|</span>
                        <span class="date">${art.date}</span>
                    </div>
                </div>
            </article>`;
    }).join('');

    container.innerHTML = articlesHTML;
    if (totalPages > 1) renderPaginationControls(container, totalPages);
}

function renderPaginationControls(container, totalPages) {
    const paginationDiv = document.createElement('div');
    paginationDiv.className = 'pagination-controls';
    if (currentPage > 1) paginationDiv.appendChild(createPageBtn('< Prev', () => changePage(currentPage - 1, container)));
    for (let i = 1; i <= totalPages; i++) {
        const btn = createPageBtn(i, () => changePage(i, container));
        if (i === currentPage) btn.classList.add('active');
        paginationDiv.appendChild(btn);
    }
    if (currentPage < totalPages) paginationDiv.appendChild(createPageBtn('Next >', () => changePage(currentPage + 1, container)));
    container.appendChild(paginationDiv);
}

function createPageBtn(text, onClick) {
    const btn = document.createElement('button');
    btn.className = 'page-btn';
    btn.innerText = text;
    btn.onclick = onClick;
    return btn;
}

function changePage(newPage, container) {
    currentPage = newPage;
    renderArticles(container, currentFilter);
    const yOffset = -100; 
    const y = container.getBoundingClientRect().top + window.pageYOffset + yOffset;
    window.scrollTo({top: y, behavior: 'smooth'});
}

function initLiveSearchSystem() {
    const overlay = document.createElement('div');
    overlay.id = 'search-full-overlay';
    overlay.innerHTML = `
        <div class="search-modal">
            <div class="search-header">
                <i class="fas fa-search" style="color:#0066cc"></i>
                <input type="text" id="main-search-input" placeholder="Type to search articles...">
                <i class="fas fa-times close-search-btn"></i>
            </div>
            <div id="search-results-list"></div>
        </div>`;
    document.body.appendChild(overlay);

    const searchTrigger = document.querySelector('.search-icon') || document.querySelector('.fa-search');
    const searchInput = document.getElementById('main-search-input');
    const resultsList = document.getElementById('search-results-list');
    const closeBtn = document.querySelector('.close-search-btn');

    if(searchTrigger) {
        searchTrigger.addEventListener('click', (e) => { e.preventDefault(); overlay.style.display = 'flex'; searchInput.focus(); });
    }

    const closeAction = () => { overlay.style.display = 'none'; searchInput.value = ''; resultsList.innerHTML = ''; };
    closeBtn.onclick = closeAction;
    overlay.onclick = (e) => { if(e.target === overlay) closeAction(); };

    searchInput.addEventListener('input', function() {
        const val = this.value.toLowerCase();
        resultsList.innerHTML = '';
        if(val.length < 1) return;

        const filtered = allArticles.filter(a => a.title.toLowerCase().includes(val) || a.category.toLowerCase().includes(val));
        if(filtered.length === 0) { resultsList.innerHTML = '<p style="text-align:center; padding:20px; color:#666;">No results found.</p>'; return; }

        resultsList.innerHTML = filtered.map(art => {
            let imgSrc = art.image.startsWith('http') ? art.image : `${linkPrefix}${art.image}`;
            return `
            <div class="search-result-item" onclick="window.location.href='${linkPrefix}${art.filename}'">
                <img src="${imgSrc}" loading="lazy">
                <div class="search-result-info">
                    <h4>${art.title}</h4>
                    <p>${art.category} • ${art.date}</p>
                </div>
            </div>`
        }).join('');
    });
}

function updateSidebar(sidebar) {
    sidebar.innerHTML = '';
    const currentFile = window.location.pathname.split('/').pop();
    const recent = allArticles.filter(art => art.filename !== currentFile).slice(0, 5);
    
    if (recent.length === 0) { sidebar.innerHTML = '<p style="color:rgba(255,255,255,0.7); padding:10px;">More articles coming soon.</p>'; return; }
    
    sidebar.innerHTML = recent.map(art => {
        let imgSrc = art.image.startsWith('http') ? art.image : `${linkPrefix}${art.image}`;
        return `
        <div class="sidebar-card">
            <div class="sidebar-img"><img src="${imgSrc}" loading="lazy"></div>
            <div class="sidebar-info">
                <a href="${linkPrefix}${art.filename}">${art.title}</a>
                <span class="sidebar-date"><i class="far fa-clock"></i> ${art.date}</span>
            </div>
        </div>`
    }).join('');
}

function initNotificationPopup() {
    if (localStorage.getItem('notify_status')) return;
    const overlay = document.createElement('div');
    overlay.className = 'notify-popup-overlay';
    overlay.innerHTML = `
        <div class="notify-popup">
            <div class="notify-icon"><i class="fas fa-bell"></i></div>
            <h3>Get Daily Updates</h3>
            <p>Never miss a tech update! Allow notifications.</p>
            <div class="notify-btns">
                <button class="btn-deny">Not Now</button>
                <button class="btn-allow">Allow</button>
            </div>
        </div>`;
    document.body.appendChild(overlay);
    overlay.querySelector('.btn-deny').onclick = () => { localStorage.setItem('notify_status', 'denied'); overlay.remove(); };
    overlay.querySelector('.btn-allow').onclick = () => {
        localStorage.setItem('notify_status', 'allowed');
        localStorage.setItem('site_subscribed', 'true');
        overlay.remove();
        alert("Thanks for subscribing!");
    };
}

function injectNotificationBell() {
    const isSubscribed = localStorage.getItem('site_subscribed');
    const bell = document.createElement('div');
    bell.className = 'notification-bell';
    bell.innerHTML = '<i class="fas fa-bell"></i>' + (!isSubscribed ? '<div class="badge" style="position:absolute; top:0; right:0; width:10px; height:10px; background:red; border-radius:50%;"></div>' : '');
    const toast = document.createElement('div'); toast.className = 'sub-toast';
    document.body.append(toast, bell);

    bell.addEventListener('click', () => {
        if(!localStorage.getItem('site_subscribed')) {
            localStorage.setItem('site_subscribed', 'true');
            localStorage.setItem('notify_status', 'allowed');
            bell.querySelector('.badge')?.remove();
            toast.innerText = "Notifications turned on! 🔔";
        } else {
            toast.innerText = "Already subscribed! ✅";
        }
        toast.style.display = 'block';
        setTimeout(() => toast.style.display = 'none', 3000);
    });
}

function setupCopyLinkButtons() {
    document.body.addEventListener('click', function(e) {
        if (e.target.closest('.btn-copy')) {
            e.preventDefault();
            navigator.clipboard.writeText(window.location.href);
            alert("Link Copied!");
        }
    });
}

function injectHeaderAuthorPic() {
    if (!isArticlePage) return;
    const headerImg = document.getElementById('header-author-img');
    const headerName = document.getElementById('header-author-name');
    if (headerImg) headerImg.src = config.defaultAuthorImg;
    if (headerName) headerName.innerHTML = `${config.authorName} <i class="fas fa-check-circle verified-tick"></i>`;
}

function updateAlsoRead() {
    const boxes = document.querySelectorAll('.also-read');
    if (boxes.length === 0) return;
    const currentFile = window.location.pathname.split('/').pop();
    const recommendations = allArticles.filter(a => a.filename !== currentFile);
    boxes.forEach((box, index) => {
        if (index < recommendations.length) {
            const art = recommendations[index];
            box.innerHTML = `<h3><i class="fas fa-book-reader"></i> Also Read</h3><a href="${linkPrefix}${art.filename}">${art.title}</a>`;
        }
    });
}

function highlightActiveMenu() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.main-nav a').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').split('/').pop() === currentPage) link.classList.add('active');
    });
}

function initCommentSystem() {
    const commentForm = document.getElementById('comment-form');
    if (!commentForm) return;
    loadComments();
    commentForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const name = document.getElementById('comment-name').value;
        const msg = document.getElementById('comment-msg').value;
        const newComment = { name, date: getTodayDate(), text: msg };
        const articleKey = 'comments_' + window.location.pathname.split('/').pop();
        let savedComments = JSON.parse(localStorage.getItem(articleKey)) || [];
        savedComments.push(newComment);
        localStorage.setItem(articleKey, JSON.stringify(savedComments));
        renderSingleComment(newComment);
        commentForm.reset();
    });
}

function loadComments() {
    const articleKey = 'comments_' + window.location.pathname.split('/').pop();
    const savedComments = JSON.parse(localStorage.getItem(articleKey)) || [];
    savedComments.forEach(comment => renderSingleComment(comment));
}

function renderSingleComment(comment) {
    const displayArea = document.getElementById('comments-display-area');
    if(!displayArea) return;
    const html = `<div class="single-comment" style="display:flex; gap:15px; margin-bottom:20px; background:#f9f9f9; padding:15px; border-radius:8px;">
        <div style="width:40px; height:40px; background:#ddd; border-radius:50%; display:flex; align-items:center; justify-content:center;"><i class="fas fa-user"></i></div>
        <div>
            <div style="font-weight:bold;">${comment.name} <span style="font-size:0.8rem; color:#888; font-weight:normal; margin-left:10px;">${comment.date}</span></div>
            <p style="margin-top:5px; font-size:0.95rem;">${comment.text}</p>
        </div>
    </div>`;
    displayArea.insertAdjacentHTML('beforeend', html);
}