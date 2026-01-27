<template>
  <div class="references-page">
    <header>
      <div class="container nav">
        <router-link to="/" class="brand">
          <svg viewBox="0 0 64 64" aria-hidden="true">
            <defs>
              <linearGradient id="ref-g" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0" stop-color="#2563eb" />
                <stop offset="1" stop-color="#14b8a6" />
              </linearGradient>
            </defs>
            <circle cx="28" cy="28" r="18" fill="url(#ref-g)" opacity="0.08" />
            <circle cx="28" cy="28" r="12" fill="none" stroke="url(#ref-g)" stroke-width="3" />
            <path d="M36 36 L46 46" stroke="url(#ref-g)" stroke-width="3.2" stroke-linecap="round" />
            <path d="M44 16 L44 20 M42 18 L46 18" stroke="url(#ref-g)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            <circle cx="44" cy="18" r="1.5" fill="url(#ref-g)" />
          </svg>
          Opportunity Hub
        </router-link>

        <nav class="navlinks desktop-nav">
          <router-link to="/">Home</router-link>
          <router-link to="/about">About Us</router-link>
          <router-link to="/references">References</router-link>
          <router-link class="btn btn-primary" to="/signup">Sign up</router-link>
          <router-link class="btn btn-outline" to="/login">Log in</router-link>
        </nav>

        <button
          class="hamburger"
          :class="{ active: isMenuOpen }"
          @click="toggleMenu"
          aria-label="Toggle menu"
        >
          <span class="bar"></span>
          <span class="bar"></span>
          <span class="bar"></span>
        </button>
      </div>

      <nav class="mobile-nav" :class="{ active: isMenuOpen }">
        <router-link to="/" @click="closeMenu">Home</router-link>
        <router-link to="/about" @click="closeMenu">About Us</router-link>
        <router-link to="/references" @click="closeMenu">References</router-link>
        <div class="mobile-nav-buttons">
          <router-link class="btn btn-primary" to="/signup" @click="closeMenu">Sign up</router-link>
          <router-link class="btn btn-outline" to="/login" @click="closeMenu">Log in</router-link>
        </div>
      </nav>
    </header>

    <main class="main">
      <div class="container">
        <section class="hero-section">
          <h1 class="page-title">References & Resources</h1>
          <p class="page-subtitle">
            Technologies, frameworks, and resources used to build Opportunity Hub
          </p>
        </section>

        <!-- Technologies Section -->
        <section class="ref-section">
          <h2 class="section-title">
            <span class="section-icon">🛠️</span>
            Technologies & Frameworks
          </h2>
          
          <div class="ref-grid">
            <!-- Frontend -->
            <div class="ref-category">
              <h3 class="category-title">Frontend</h3>
              <div class="ref-list">
                <a href="https://vuejs.org/" target="_blank" rel="noopener" class="ref-card">
                  <div class="ref-icon vue-icon">
                    <svg viewBox="0 0 128 128"><path fill="#42b883" d="M78.8,10L64,35.4L49.2,10H0l64,110l64-110C128,10,78.8,10,78.8,10z"/><path fill="#35495e" d="M78.8,10L64,35.4L49.2,10H25.6L64,76l38.4-66H78.8z"/></svg>
                  </div>
                  <div class="ref-info">
                    <h4>Vue.js 3</h4>
                    <p>Progressive JavaScript framework for building user interfaces</p>
                  </div>
                  <span class="ref-arrow">→</span>
                </a>

                <a href="https://router.vuejs.org/" target="_blank" rel="noopener" class="ref-card">
                  <div class="ref-icon vue-icon">
                    <svg viewBox="0 0 128 128"><path fill="#42b883" d="M78.8,10L64,35.4L49.2,10H0l64,110l64-110C128,10,78.8,10,78.8,10z"/><path fill="#35495e" d="M78.8,10L64,35.4L49.2,10H25.6L64,76l38.4-66H78.8z"/></svg>
                  </div>
                  <div class="ref-info">
                    <h4>Vue Router</h4>
                    <p>Official router for Vue.js applications</p>
                  </div>
                  <span class="ref-arrow">→</span>
                </a>

                <a href="https://vitejs.dev/" target="_blank" rel="noopener" class="ref-card">
                  <div class="ref-icon vite-icon">⚡</div>
                  <div class="ref-info">
                    <h4>Vite</h4>
                    <p>Next generation frontend build tool</p>
                  </div>
                  <span class="ref-arrow">→</span>
                </a>

                <a href="https://axios-http.com/" target="_blank" rel="noopener" class="ref-card">
                  <div class="ref-icon axios-icon">📡</div>
                  <div class="ref-info">
                    <h4>Axios</h4>
                    <p>Promise-based HTTP client for the browser</p>
                  </div>
                  <span class="ref-arrow">→</span>
                </a>
              </div>
            </div>

            <!-- Backend -->
            <div class="ref-category">
              <h3 class="category-title">Backend</h3>
              <div class="ref-list">
                <a href="https://fastapi.tiangolo.com/" target="_blank" rel="noopener" class="ref-card">
                  <div class="ref-icon fastapi-icon">🚀</div>
                  <div class="ref-info">
                    <h4>FastAPI</h4>
                    <p>Modern, fast web framework for building APIs with Python</p>
                  </div>
                  <span class="ref-arrow">→</span>
                </a>

                <a href="https://www.python.org/" target="_blank" rel="noopener" class="ref-card">
                  <div class="ref-icon python-icon">🐍</div>
                  <div class="ref-info">
                    <h4>Python 3</h4>
                    <p>High-level programming language for backend development</p>
                  </div>
                  <span class="ref-arrow">→</span>
                </a>

                <a href="https://www.sqlalchemy.org/" target="_blank" rel="noopener" class="ref-card">
                  <div class="ref-icon db-icon">🗄️</div>
                  <div class="ref-info">
                    <h4>SQLAlchemy</h4>
                    <p>Python SQL toolkit and Object-Relational Mapping</p>
                  </div>
                  <span class="ref-arrow">→</span>
                </a>

                <a href="https://www.postgresql.org/" target="_blank" rel="noopener" class="ref-card">
                  <div class="ref-icon db-icon">🐘</div>
                  <div class="ref-info">
                    <h4>PostgreSQL</h4>
                    <p>Advanced open-source relational database</p>
                  </div>
                  <span class="ref-arrow">→</span>
                </a>

                <a href="https://resend.com/" target="_blank" rel="noopener" class="ref-card">
                  <div class="ref-icon email-icon">📧</div>
                  <div class="ref-info">
                    <h4>Resend</h4>
                    <p>Email API for sending transactional emails</p>
                  </div>
                  <span class="ref-arrow">→</span>
                </a>

                <a href="https://docs.pydantic.dev/" target="_blank" rel="noopener" class="ref-card">
                  <div class="ref-icon pydantic-icon">✅</div>
                  <div class="ref-info">
                    <h4>Pydantic</h4>
                    <p>Data validation using Python type annotations</p>
                  </div>
                  <span class="ref-arrow">→</span>
                </a>
              </div>
            </div>

            <!-- Styling -->
            <div class="ref-category">
              <h3 class="category-title">Styling & Design</h3>
              <div class="ref-list">
                <a href="https://developer.mozilla.org/en-US/docs/Web/HTML" target="_blank" rel="noopener" class="ref-card">
                  <div class="ref-icon html-icon">📄</div>
                  <div class="ref-info">
                    <h4>HTML5</h4>
                    <p>Standard markup language for web pages</p>
                  </div>
                  <span class="ref-arrow">→</span>
                </a>

                <a href="https://developer.mozilla.org/en-US/docs/Web/CSS" target="_blank" rel="noopener" class="ref-card">
                  <div class="ref-icon css-icon">🎨</div>
                  <div class="ref-info">
                    <h4>CSS3</h4>
                    <p>Stylesheet language for presentation and layout</p>
                  </div>
                  <span class="ref-arrow">→</span>
                </a>

                <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank" rel="noopener" class="ref-card">
                  <div class="ref-icon js-icon">⚙️</div>
                  <div class="ref-info">
                    <h4>JavaScript (ES6+)</h4>
                    <p>Programming language for interactive web functionality</p>
                  </div>
                  <span class="ref-arrow">→</span>
                </a>
              </div>
            </div>

            <!-- Security & Auth -->
            <div class="ref-category">
              <h3 class="category-title">Security & Authentication</h3>
              <div class="ref-list">
                <a href="https://jwt.io/" target="_blank" rel="noopener" class="ref-card">
                  <div class="ref-icon jwt-icon">🔐</div>
                  <div class="ref-info">
                    <h4>JWT (JSON Web Tokens)</h4>
                    <p>Secure token-based authentication</p>
                  </div>
                  <span class="ref-arrow">→</span>
                </a>

                <a href="https://passlib.readthedocs.io/" target="_blank" rel="noopener" class="ref-card">
                  <div class="ref-icon security-icon">🛡️</div>
                  <div class="ref-info">
                    <h4>Passlib + Bcrypt</h4>
                    <p>Password hashing library for secure storage</p>
                  </div>
                  <span class="ref-arrow">→</span>
                </a>
              </div>
            </div>
          </div>
        </section>

        <!-- Learning Resources Section -->
        <section class="ref-section">
          <h2 class="section-title">
            <span class="section-icon">📚</span>
            Learning Resources
          </h2>
          
          <div class="resources-grid">
            <a href="https://developer.mozilla.org/" target="_blank" rel="noopener" class="resource-card mdn">
              <div class="resource-logo">MDN</div>
              <h4>MDN Web Docs</h4>
              <p>Comprehensive documentation for HTML, CSS, and JavaScript</p>
            </a>

            <a href="https://www.w3schools.com/" target="_blank" rel="noopener" class="resource-card w3">
              <div class="resource-logo">W3</div>
              <h4>W3Schools</h4>
              <p>Web development tutorials and references</p>
            </a>

            <a href="https://stackoverflow.com/" target="_blank" rel="noopener" class="resource-card so">
              <div class="resource-logo">SO</div>
              <h4>Stack Overflow</h4>
              <p>Community Q&A for programming questions</p>
            </a>

            <a href="https://github.com/" target="_blank" rel="noopener" class="resource-card gh">
              <div class="resource-logo">GH</div>
              <h4>GitHub</h4>
              <p>Version control and code collaboration</p>
            </a>

            <a href="https://www.youtube.com/" target="_blank" rel="noopener" class="resource-card yt">
              <div class="resource-logo">YT</div>
              <h4>YouTube</h4>
              <p>Video tutorials for web development</p>
            </a>


          </div>
        </section>

        <!-- Documentation Links -->
        <section class="ref-section">
          <h2 class="section-title">
            <span class="section-icon">📖</span>
            Official Documentation
          </h2>
          
          <div class="docs-list">
            <a href="https://vuejs.org/guide/introduction.html" target="_blank" rel="noopener" class="doc-link">
              <span class="doc-name">Vue.js Documentation</span>
              <span class="doc-url">vuejs.org/guide</span>
            </a>
            <a href="https://fastapi.tiangolo.com/tutorial/" target="_blank" rel="noopener" class="doc-link">
              <span class="doc-name">FastAPI Tutorial</span>
              <span class="doc-url">fastapi.tiangolo.com/tutorial</span>
            </a>
            <a href="https://docs.sqlalchemy.org/en/20/" target="_blank" rel="noopener" class="doc-link">
              <span class="doc-name">SQLAlchemy 2.0 Documentation</span>
              <span class="doc-url">docs.sqlalchemy.org</span>
            </a>
            <a href="https://docs.python.org/3/" target="_blank" rel="noopener" class="doc-link">
              <span class="doc-name">Python 3 Documentation</span>
              <span class="doc-url">docs.python.org</span>
            </a>
            <a href="https://developer.mozilla.org/en-US/docs/Learn" target="_blank" rel="noopener" class="doc-link">
              <span class="doc-name">MDN Learn Web Development</span>
              <span class="doc-url">developer.mozilla.org/learn</span>
            </a>
            <a href="https://css-tricks.com/" target="_blank" rel="noopener" class="doc-link">
              <span class="doc-name">CSS-Tricks</span>
              <span class="doc-url">css-tricks.com</span>
            </a>
          </div>
        </section>

        <!-- Tools Section -->
        <section class="ref-section">
          <h2 class="section-title">
            <span class="section-icon">🔧</span>
            Development Tools
          </h2>
          
          <div class="tools-grid">
            <div class="tool-card">
              <span class="tool-icon">💻</span>
              <h4>VS Code / Cursor</h4>
              <p>Code editor for coding</p>
            </div>
            <div class="tool-card">
              <span class="tool-icon">🔄</span>
              <h4>Git</h4>
              <p>Version control system</p>
            </div>
            <div class="tool-card">
              <span class="tool-icon">📦</span>
              <h4>npm</h4>
              <p>Node.js package manager</p>
            </div>
            <div class="tool-card">
              <span class="tool-icon">🐍</span>
              <h4>pip</h4>
              <p>Python package installer</p>
            </div>
            <div class="tool-card">
              <span class="tool-icon">🌐</span>
              <h4>Chrome DevTools</h4>
              <p>Browser debugging tools</p>
            </div>
            <div class="tool-card">
              <span class="tool-icon">📬</span>
              <h4>Postman</h4>
              <p>API testing and development</p>
            </div>
          </div>
        </section>
      </div>
    </main>

    <footer>
      <div class="container footer-inner">
        <p class="muted small-text">© {{ year }} Opportunity Hub · TSA Webmaster {{ year }}</p>
        <div class="footer-links">
          <router-link to="/about">About Us</router-link>
          <router-link to="/references">References</router-link>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const year = new Date().getFullYear()

const isMenuOpen = ref(false)
function toggleMenu() { isMenuOpen.value = !isMenuOpen.value }
function closeMenu() { isMenuOpen.value = false }
</script>

<style scoped>
*{ box-sizing:border-box; margin:0; padding:0; }

:root{
  --bg:#f3f4ff;
  --bg-soft:#eef2ff;
  --panel:#ffffff;
  --panel-elevated:#ffffff;
  --muted:#000000;
  --text:#0f172a;
  --accent:#2563eb;
  --accent-2:#14b8a6;
  --ring:rgba(37,99,235,.25);
  --card:#ffffff;
  --card-2:#f9fafb;
  --success:#22c55e;
  --warning:#eab308;
}

.references-page{
  min-height:100vh;
  display:flex;
  flex-direction:column;
  background:
    radial-gradient(900px 500px at 10% -10%, rgba(59,130,246,.20), transparent 60%),
    radial-gradient(900px 600px at 90% 110%, rgba(45,212,191,.18), transparent 60%),
    var(--bg);
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, "Helvetica Neue", Arial;
  color:var(--text);
}

a{color:inherit;text-decoration:none}

.container{
  max-width:1200px;
  margin:0 auto;
  padding:24px 24px 32px;
}

/* Header */
header{
  position:sticky;
  top:0;
  z-index:20;
  background:rgba(248,250,252,.86);
  backdrop-filter: blur(12px);
}

.nav{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:16px;
}

.brand{
  display:flex;
  align-items:center;
  gap:10px;
  font-weight:800;
  letter-spacing:.04em;
  font-size:18px;
}

.brand svg{
  width:30px;
  height:30px;
}

.navlinks{
  display:flex;
  gap:14px;
  align-items:center;
  flex-wrap:wrap;
  font-size:14px;
}

.navlinks a{
  color:var(--muted);
}

.navlinks a:hover{
  color:var(--text);
}

.navlinks a.btn-primary{
  color:#fff;
}

.btn{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  gap:8px;
  padding:10px 16px;
  border-radius:999px;
  border:1px solid rgba(148,163,184,.4);
  background:linear-gradient(180deg, #ffffff, #eef2ff);
  color:var(--text);
  font-size:14px;
  cursor:pointer;
  transition:transform .12s ease, box-shadow .12s ease, background .12s ease, border-color .12s ease;
  box-shadow:0 0 0 rgba(0,0,0,0);
}

.btn:hover{
  transform:translateY(-1px);
  box-shadow:0 10px 24px rgba(15,23,42,.12);
  border-color:rgba(148,163,184,.9);
}

.btn-primary{
  background:linear-gradient(90deg, var(--accent), var(--accent-2));
  color:#fff;
  font-weight:700;
  border:none;
}

.btn-primary:hover{
  box-shadow:0 14px 28px rgba(37,99,235,.28);
}

.btn-outline{
  background:#ffffff;
}

.desktop-nav{ display:flex; }

/* Hamburger */
.hamburger{
  display:none;
  flex-direction:column;
  background:transparent;
  border:none;
  cursor:pointer;
  padding:8px;
  gap:5px;
  z-index:101;
}

.bar{
  display:block;
  width:25px;
  height:3px;
  background-color:var(--text);
  border-radius:2px;
  transition:all 0.3s ease-in-out;
  margin:0;
}

.hamburger.active .bar:nth-child(1){
  transform: translateY(8px) rotate(45deg);
}

.hamburger.active .bar:nth-child(2){
  opacity: 0;
}

.hamburger.active .bar:nth-child(3){
  transform: translateY(-8px) rotate(-45deg);
}

/* Mobile Navigation */
.mobile-nav{
  display:none;
  flex-direction:column;
  gap:0;
  background:rgba(248,250,252,.95);
  backdrop-filter: blur(12px);
  border-top:1px solid rgba(148,163,184,.25);
  padding:0 24px;
  max-height:0;
  overflow:hidden;
  transition:max-height 0.3s ease-in-out, padding 0.3s ease-in-out;
}

.mobile-nav.active{
  max-height:500px;
  padding:16px 24px;
}

.mobile-nav a{
  color:var(--muted);
  padding:12px 0;
  font-size:14px;
  border-bottom:1px solid rgba(148,163,184,.15);
  transition:color 0.2s ease;
}

.mobile-nav a:last-child{
  border-bottom:none;
}

.mobile-nav a:hover{
  color:var(--text);
}

.mobile-nav-buttons{
  margin-top:16px;
  padding-top:16px;
  border-top:1px solid rgba(148,163,184,.25);
  display:flex;
  flex-direction:column;
  gap:10px;
}

.mobile-nav-buttons .btn{
  width:100%;
  text-align:center;
  justify-content:center;
}

/* Main */
.main{
  flex:1;
  padding:40px 0 60px;
}

.hero-section{
  text-align:center;
  margin-bottom:48px;
}

.page-title{
  font-size:clamp(28px, 5vw, 42px);
  font-weight:800;
  background:linear-gradient(135deg, var(--accent), var(--accent-2));
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  margin-bottom:12px;
}

.page-subtitle{
  font-size:16px;
  color:var(--muted);
  max-width:500px;
  margin:0 auto;
}

/* Sections */
.ref-section{
  margin-bottom:48px;
}

.section-title{
  display:flex;
  align-items:center;
  gap:12px;
  font-size:20px;
  font-weight:700;
  margin-bottom:24px;
  color:var(--text);
}

.section-icon{
  font-size:24px;
}

/* Reference Grid */
.ref-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit, minmax(280px, 1fr));
  gap:24px;
}

.ref-category{
  background:var(--card);
  border-radius:16px;
  padding:24px;
  border:1px solid rgba(148,163,184,.15);
}

.category-title{
  font-size:14px;
  font-weight:700;
  color:var(--muted);
  text-transform:uppercase;
  letter-spacing:.05em;
  margin-bottom:16px;
  padding-bottom:12px;
  border-bottom:1px solid rgba(148,163,184,.15);
}

.ref-list{
  display:flex;
  flex-direction:column;
  gap:8px;
}

.ref-card{
  display:flex;
  align-items:center;
  gap:12px;
  padding:12px;
  border-radius:12px;
  text-decoration:none;
  color:var(--text);
  transition:all 0.2s ease;
  border:1px solid transparent;
}

.ref-card:hover{
  background:rgba(37,99,235,.04);
  border-color:rgba(37,99,235,.15);
}

.ref-icon{
  width:40px;
  height:40px;
  border-radius:10px;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:20px;
  background:linear-gradient(135deg, rgba(37,99,235,.1), rgba(20,184,166,.1));
  flex-shrink:0;
}

.ref-icon svg{
  width:24px;
  height:24px;
}

.ref-info{
  flex:1;
  min-width:0;
}

.ref-info h4{
  font-size:14px;
  font-weight:600;
  margin-bottom:2px;
}

.ref-info p{
  font-size:12px;
  color:var(--muted);
  line-height:1.4;
}

.ref-arrow{
  color:var(--accent);
  font-size:14px;
  opacity:0;
  transition:opacity 0.2s, transform 0.2s;
}

.ref-card:hover .ref-arrow{
  opacity:1;
  transform:translateX(4px);
}

/* Resources Grid */
.resources-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit, minmax(180px, 1fr));
  gap:16px;
}

.resource-card{
  display:flex;
  flex-direction:column;
  align-items:center;
  text-align:center;
  padding:24px 16px;
  background:var(--card);
  border-radius:16px;
  border:1px solid rgba(148,163,184,.15);
  text-decoration:none;
  color:var(--text);
  transition:all 0.2s ease;
}

.resource-card:hover{
  transform:translateY(-4px);
  box-shadow:0 12px 32px rgba(15,23,42,.1);
}

.resource-logo{
  width:56px;
  height:56px;
  border-radius:14px;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:18px;
  font-weight:900;
  margin-bottom:12px;
  color:#fff;
}

.resource-card.mdn .resource-logo{ background:linear-gradient(135deg, #000, #333); }
.resource-card.w3 .resource-logo{ background:linear-gradient(135deg, #04aa6d, #087f5b); }
.resource-card.so .resource-logo{ background:linear-gradient(135deg, #f48024, #bc5d00); }
.resource-card.gh .resource-logo{ background:linear-gradient(135deg, #24292e, #0d1117); }
.resource-card.yt .resource-logo{ background:linear-gradient(135deg, #ff0000, #cc0000); }

.resource-card h4{
  font-size:14px;
  font-weight:700;
  margin-bottom:4px;
}

.resource-card p{
  font-size:12px;
  color:var(--muted);
  line-height:1.4;
}

/* Docs List */
.docs-list{
  display:flex;
  flex-direction:column;
  gap:8px;
  background:var(--card);
  border-radius:16px;
  padding:8px;
  border:1px solid rgba(148,163,184,.15);
}

.doc-link{
  display:flex;
  justify-content:space-between;
  align-items:center;
  padding:14px 16px;
  border-radius:10px;
  text-decoration:none;
  color:var(--text);
  transition:background 0.15s;
}

.doc-link:hover{
  background:rgba(37,99,235,.04);
}

.doc-name{
  font-size:14px;
  font-weight:600;
}

.doc-url{
  font-size:12px;
  color:var(--accent);
}

/* Tools Grid */
.tools-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit, minmax(160px, 1fr));
  gap:12px;
}

.tool-card{
  display:flex;
  flex-direction:column;
  align-items:center;
  text-align:center;
  padding:20px 12px;
  background:var(--card);
  border-radius:12px;
  border:1px solid rgba(148,163,184,.15);
}

.tool-icon{
  font-size:28px;
  margin-bottom:8px;
}

.tool-card h4{
  font-size:13px;
  font-weight:700;
  margin-bottom:4px;
}

.tool-card p{
  font-size:11px;
  color:var(--muted);
}

/* Footer */
footer{
  padding:20px 0;
  border-top:1px solid rgba(148,163,184,.2);
  background:#fff;
}

.footer-inner{
  display:flex;
  justify-content:space-between;
  align-items:center;
  flex-wrap:wrap;
  gap:12px;
}

.footer-links{
  display:flex;
  gap:20px;
}

.footer-links a{
  color:var(--muted);
  text-decoration:none;
  font-size:13px;
}

.footer-links a:hover{
  color:var(--accent);
}

.muted{ color:var(--muted); }
.small-text{ font-size:13px; }

/* Responsive */
@media (max-width: 640px){
  .container{
    padding:18px 16px 28px;
  }

  .desktop-nav{
    display:none;
  }

  .hamburger{
    display:flex;
  }

  .mobile-nav{
    display:flex;
  }
  
  .main{ padding:24px 0 40px; }
  
  .ref-grid{ grid-template-columns:1fr; }
  .resources-grid{ grid-template-columns:repeat(2, 1fr); }
  .tools-grid{ grid-template-columns:repeat(2, 1fr); }
  
  .doc-link{
    flex-direction:column;
    align-items:flex-start;
    gap:4px;
  }
  
  .footer-inner{
    flex-direction:column;
    text-align:center;
  }
}

@media (max-width: 480px){
  .resources-grid{ grid-template-columns:1fr; }
  .tools-grid{ grid-template-columns:1fr; }
}
</style>
