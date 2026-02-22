// ===== UNIVERSAL AUTO SYSTEM (Optimized with Fast JSON Loading) =====

const config = {
    folderName: 'articles',      
    itemsPerPage: 15,            
    authorName: 'Sarah Mitchell',
    defaultAuthorImg: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-1.2.1&auto=format&fit=crop&w=150&q=80' 
};

// State Variables
let allArticles = [];
let currentPage = 1;
let currentFilter = 'all'; 

// Location & Path Logic (FIXED FOR TECHVIBE-WEB)
const isArticlePage = window.location.pathname.includes(`/${config.folderName}/`);
const basePath = isArticlePage ? '../' : ''; // Home page par khali rahega, article page par ../ jayega
const linkPrefix = isArticlePage ? '' : `${config.folderName}/`; 
const rootPrefix = isArticlePage ? '../' : ''; 

// --- CSS INJECTION (Sidebar, Pagination, Notifications, Author, Search) ---
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

    .notification-bell { z-index: 10001 !important; cursor: pointer; touch-action: manipulation; }
    .sub-toast { position: fixed; bottom: 80px; left: 50%; transform: translateX(-50%); background: #333; color: #fff; padding: 10px 20px; border-radius: 20px; z-index: 10002; display: none; }
`;
document.head.appendChild(style);

// --- MAIN INIT ---
document.addEventListener('DOMContentLoaded', async function() {
    highlightActiveMenu();
    updateInnerArticleDate();
    
    await loadArticlesFast(); // Sab se pehle data load hoga
    
    // Home Page Grid
    const homeContainer = document.getElementById('articles-container');
    if (homeContainer) { renderArticles(homeContainer, 'all'); }

    // Tech Page Grid
    const techContainer = document.getElementById('tech-page-container');
    if (techContainer) { renderArticles(techContainer, 'Tech'); }

    // Sidebar Update
    const sidebar = document.getElementById('sidebar-articles');
    if (sidebar) updateSidebar(sidebar);
    
    updateAlsoRead();
    injectHeaderAuthorPic(); 
    initCommentSystem();
    injectNotificationBell();
    setupCopyLinkButtons();
    initLiveSearchSystem(); 
    
    setTimeout(initNotificationPopup, 3000);
});

// --- OPTIMIZED: JSON LOADER ---
async function loadArticlesFast() {
    try {
        // FIXED PATH: Hum articles folder ke andar data.json dhoond rahe hain
        const jsonPath = isArticlePage ? 'data.json' : 'articles/data.json';
        const response = await fetch(jsonPath);
        if (response.ok) {
            allArticles = await response.json();
            allArticles.sort((a, b) => b.id - a.id); // Latest articles top par
        }
    } catch (e) {
        console.error("Error loading articles:", e);
    }
}

// --- RENDER ARTICLES ---
function renderArticles(container, filter) {
    if (!container) return;
    container.innerHTML = '';
    
    let displayList = allArticles;
    if (filter !== 'all') displayList = allArticles.filter(art => art.category === filter);
    
    const totalItems = displayList.length;
    const totalPages = Math.ceil(totalItems / config.itemsPerPage);
    
    const start = (currentPage - 1) * config.itemsPerPage;
    const end = start + config.itemsPerPage;
    const paginatedItems = displayList.slice(start, end);

    if (paginatedItems.length === 0) { 
        container.innerHTML = '<div style="padding:40px; text-align:center; grid-column:1/-1;"><h3>Articles loading...</h3></div>'; 
        return; 
    }

    container.innerHTML = paginatedItems.map(art => {
        let imgSrc = art.image.startsWith('http') ? art.image : `${linkPrefix}${art.image}`;
        return `
            <article class="news-card">
                <div class="article-image" onclick="window.location.href='${linkPrefix}${art.filename}'" style="cursor:pointer">
                    <img src="${imgSrc}" alt="${art.title}" loading="lazy">
                </div>
                <div class="news-content">
                    <h3 class="news-title" onclick="window.location.href='${linkPrefix}${art.filename}'" style="cursor:pointer">${art.title}</h3>
                    <div class="news-meta">
                        <img src="${art.authorImg}" class="card-author-img" alt="author">
                        <span class="author-link">${art.author} <i class="fas fa-check-circle verified-tick"></i></span>
                        <span class="date">${art.date}</span>
                    </div>
                </div>
            </article>`;
    }).join('');

    if (totalPages > 1) renderPaginationControls(container, totalPages);
}

// ... (Baqi saari purani functions: pagination, search, notification wahi rahegi jo aapne di thi) ...