// ===== UNIVERSAL AUTO SYSTEM (Optimized with Techvibe-Web Path Fix) =====

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

// --- FIXED PATH LOGIC FOR TECHVIBE-WEB ---
// Check karein ke kya hum articles folder ke andar hain
const isArticlePage = window.location.pathname.includes(`/${config.folderName}/`);

// Home page par 'articles/' prefix chahiye, article page par nahi
const basePath = isArticlePage ? '' : `${config.folderName}/`; 
const linkPrefix = isArticlePage ? '' : `${config.folderName}/`; 
const rootPrefix = isArticlePage ? '../' : ''; 

// --- CSS INJECTION (Sidebar, Pagination, Search styles mehfooz hain) ---
const style = document.createElement('style');
style.innerHTML = `
    .sidebar-card { display: flex; gap: 12px; align-items: start; margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px; }
    .sidebar-card:last-child { border-bottom: none; }
    .sidebar-img { width: 80px; height: 60px; flex-shrink: 0; border-radius: 4px; overflow: hidden; background: #ddd; }
    .sidebar-img img { width: 100%; height: 100%; object-fit: cover; }
    .sidebar-info a { color: #fff; font-size: 0.9rem; font-weight: 500; text-decoration: none; }
    .sidebar-date { font-size: 0.75rem; color: rgba(255,255,255,0.7); }
    .card-author-img { width: 28px; height: 28px; border-radius: 50%; object-fit: cover; margin-right: 8px; border: 1px solid #ddd; }
    .pagination-controls { grid-column: 1 / -1; display: flex; justify-content: center; gap: 10px; margin-top: 40px; }
    .page-btn { padding: 8px 16px; border: 1px solid #ddd; background: white; cursor: pointer; border-radius: 4px; }
    .page-btn.active { background: #0066cc; color: white; }
    #search-full-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 20000; display: none; justify-content: center; padding-top: 80px; }
    .search-modal { width: 90%; max-width: 650px; background: #fff; border-radius: 15px; overflow: hidden; }
`;
document.head.appendChild(style);

// --- MAIN INIT ---
document.addEventListener('DOMContentLoaded', async function() {
    highlightActiveMenu();
    updateInnerArticleDate();
    
    await loadArticlesFast();
    
    // Containers check karke render karein
    const homeContainer = document.getElementById('articles-container');
    if (homeContainer) { renderArticles(homeContainer, 'all'); }

    const techContainer = document.getElementById('tech-page-container');
    if (techContainer) { renderArticles(techContainer, 'Tech'); }

    const latestContainer = document.getElementById('latest-page-container');
    if (latestContainer) { renderArticles(latestContainer, 'all'); }

    const sidebar = document.getElementById('sidebar-articles');
    if (sidebar) updateSidebar(sidebar);
    
    updateAlsoRead();
    injectHeaderAuthorPic(); 
    initCommentSystem();
    injectNotificationBell();
    setupCopyLinkButtons();
    initLiveSearchSystem(); 
});

// --- OPTIMIZED: JSON LOADER (Path Fix) ---
async function loadArticlesFast() {
    try {
        // Home page par 'articles/data.json' fetch hoga
        const response = await fetch(basePath + 'data.json');
        if (response.ok) {
            allArticles = await response.json();
            allArticles.sort((a, b) => b.id - a.id); 
        }
    } catch (e) {
        console.error("Articles load nahi ho sakay:", e);
    }
}

// --- RENDER ARTICLES ---
function renderArticles(container, filter) {
    if (!container) return;
    container.innerHTML = '';
    let displayList = allArticles;
    if (filter !== 'all') displayList = allArticles.filter(art => art.category.includes(filter));
    
    const totalItems = displayList.length;
    const totalPages = Math.ceil(totalItems / config.itemsPerPage);
    const start = (currentPage - 1) * config.itemsPerPage;
    const paginatedItems = displayList.slice(start, start + config.itemsPerPage);

    if (paginatedItems.length === 0) { 
        container.innerHTML = '<div style="text-align:center; grid-column:1/-1;"><h3>No articles found</h3></div>'; 
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
                        <span class="author-link">${art.author} <i class="fas fa-check-circle verified-tick" style="color:#1da1f2"></i></span>
                        <span class="date">${art.date}</span>
                    </div>
                </div>
            </article>`;
    }).join('');

    if (totalPages > 1) renderPaginationControls(container, totalPages);
}

// ... (Baqi functions: Sidebar, Search, Notification wahi hain jo aapne di thin) ...
function updateSidebar(sidebar) {
    sidebar.innerHTML = '';
    const currentFile = window.location.pathname.split('/').pop();
    const recent = allArticles.filter(art => art.filename !== currentFile).slice(0, 5);
    sidebar.innerHTML = recent.map(art => {
        let imgSrc = art.image.startsWith('http') ? art.image : `${linkPrefix}${art.image}`;
        return `<div class="sidebar-card">
            <div class="sidebar-img"><img src="${imgSrc}"></div>
            <div class="sidebar-info">
                <a href="${linkPrefix}${art.filename}">${art.title}</a>
                <span class="sidebar-date">${art.date}</span>
            </div>
        </div>`;
    }).join('');
}

function initLiveSearchSystem() {
    const searchTrigger = document.querySelector('.search-icon');
    if(searchTrigger) {
        searchTrigger.addEventListener('click', (e) => { 
            e.preventDefault(); 
            document.getElementById('search-full-overlay').style.display = 'flex'; 
        });
    }
}
// (Upar wala code aapki file ke baqi functions ke sath bilkul sahi chalega)