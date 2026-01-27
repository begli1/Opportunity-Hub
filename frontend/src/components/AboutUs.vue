<template>
  <div class="about-page">
    <header>
      <div class="container">
        <nav class="nav">
          <router-link to="/" class="brand">
            <svg viewBox="0 0 64 64" aria-hidden="true">
              <defs>
                <linearGradient id="about-g" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0" stop-color="#2563eb" />
                  <stop offset="1" stop-color="#14b8a6" />
                </linearGradient>
              </defs>
              <circle cx="28" cy="28" r="18" fill="url(#about-g)" opacity="0.08" />
              <circle cx="28" cy="28" r="12" fill="none" stroke="url(#about-g)" stroke-width="3" />
              <path d="M36 36 L46 46" stroke="url(#about-g)" stroke-width="3.2" stroke-linecap="round" />
            </svg>
            Opportunity Hub
          </router-link>

          <div class="desktop-nav">
            <div class="navlinks">
              <router-link to="/">Home</router-link>
              <router-link to="/about">About Us</router-link>
              <router-link to="/references">References</router-link>
            </div>
            <router-link to="/signup" class="btn btn-primary">Sign up</router-link>
            <router-link to="/login" class="btn btn-outline">Log in</router-link>
          </div>

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
        </nav>
      </div>

      <nav class="mobile-nav" :class="{ active: isMenuOpen }">
        <router-link to="/" @click="closeMenu">Home</router-link>
        <router-link to="/about" @click="closeMenu">About Us</router-link>
        <router-link to="/references" @click="closeMenu">References</router-link>
        <div class="mobile-nav-buttons">
          <router-link to="/signup" class="btn btn-primary" @click="closeMenu">Sign up</router-link>
          <router-link to="/login" class="btn btn-outline" @click="closeMenu">Log in</router-link>
        </div>
      </nav>
    </header>

    <main class="main">
      <div class="container">
        <!-- Hero Section -->
        <section class="hero-section">
          <div class="hero-badge">TSA Webmaster {{ year }}</div>
          <h1 class="hero-title">About Opportunity Hub</h1>
          <p class="hero-subtitle">
            Connecting students with the opportunities that shape their future
          </p>
        </section>

        <!-- Mission Section -->
        <section class="mission-section">
          <div class="mission-card">
            <div class="mission-icon">🎯</div>
            <h2>Our Mission</h2>
            <p class="mission-text">
              Opportunity Hub was created to solve a common problem students face: 
              <strong>finding the right opportunities shouldn't require visiting dozens of different websites.</strong>
            </p>
            <p class="mission-text">
              We believe every student deserves easy access to clubs, internships, volunteering positions, 
              and tutoring opportunities—all in one place. Our platform serves as a centralized hub where 
              students can discover, explore, and apply to opportunities that match their interests and goals.
            </p>
          </div>
        </section>

        <!-- Problem & Solution -->
        <section class="problem-section">
          <div class="problem-grid">
            <div class="problem-card">
              <div class="card-header problem">
                <span class="card-icon">😫</span>
                <h3>The Problem</h3>
              </div>
              <ul class="problem-list">
                <li>Students struggle to find relevant opportunities</li>
                <li>Information is scattered across multiple websites</li>
                <li>School clubs are often poorly advertised</li>
                <li>No centralized system for internships and volunteering</li>
                <li>Missed deadlines due to lack of awareness</li>
              </ul>
            </div>

            <div class="problem-card">
              <div class="card-header solution">
                <span class="card-icon">💡</span>
                <h3>Our Solution</h3>
              </div>
              <ul class="solution-list">
                <li>One platform for all student opportunities</li>
                <li>Easy search and filter by type, location, tags</li>
                <li>Direct in-app applications</li>
                <li>Save and track opportunities you're interested in</li>
                <li>AI-powered content moderation for safety</li>
              </ul>
            </div>
          </div>
        </section>

        <!-- Vision Section -->
        <section class="vision-section">
          <h2 class="section-title">
            <span class="section-icon">🚀</span>
            The Vision
          </h2>
          <div class="vision-content">
            <p>
              <strong>Opportunity Hub is a blueprint for what student platforms could be.</strong> 
              Imagine a world where:
            </p>
            <div class="vision-grid">
              <div class="vision-item">
                <span class="vision-emoji">🏫</span>
                <p>Every school has a dedicated hub for their clubs, making it easy for students to discover what's available</p>
              </div>
              <div class="vision-item">
                <span class="vision-emoji">🌍</span>
                <p>Local internships and volunteering opportunities are easily discoverable by nearby students</p>
              </div>
              <div class="vision-item">
                <span class="vision-emoji">📚</span>
                <p>Tutoring connections happen seamlessly, helping students help each other</p>
              </div>
              <div class="vision-item">
                <span class="vision-emoji">🤝</span>
                <p>Organizations can reach motivated students directly, without expensive advertising</p>
              </div>
            </div>
            <p class="vision-closing">
              This project demonstrates what's possible when we put student needs first. 
              It's not just a website—it's a proof of concept for better educational tools.
            </p>
          </div>
        </section>

        <!-- Team Section -->
        <section class="team-section">
          <h2 class="section-title">
            <span class="section-icon">👥</span>
            Meet Our Team
          </h2>
          <p class="team-intro">
            The talented individuals who brought Opportunity Hub to life
          </p>

          <div class="team-grid">
            <!-- Team Leader -->
            <div class="team-card leader">
              <div class="member-avatar leader-avatar">BP</div>
              <div class="member-badge leader-badge">Team Leader</div>
              <h3 class="member-name">Begli Pirmuhammedov</h3>
              <p class="member-role">Main Programmer · Full Stack Developer</p>
              <p class="member-desc">
                Led the development of both frontend and backend systems, 
                architecting the entire application structure.
              </p>
              <div class="member-skills">
                <span class="skill-tag">FastAPI</span>
                <span class="skill-tag">Vue.js</span>
                <span class="skill-tag">HTML</span>
                <span class="skill-tag">CSS</span>
                <span class="skill-tag">Pydantic</span>
                <span class="skill-tag">SQLAlchemy</span>
                <span class="skill-tag">Python</span>
                <span class="skill-tag">JavaScript</span>
              </div>
            </div>

            <!-- Frontend Developers -->
            <div class="team-card">
              <div class="member-avatar frontend-avatar">JM</div>
              <div class="member-badge frontend-badge">Frontend</div>
              <h3 class="member-name">Jabari Myers</h3>
              <p class="member-role">Frontend Developer</p>
              <p class="member-desc">
                Contributed to the user interface design and frontend functionality.
              </p>
              <div class="member-skills">
                <span class="skill-tag">Vue.js</span>
                <span class="skill-tag">HTML</span>
                <span class="skill-tag">CSS</span>
              </div>
            </div>

            <div class="team-card">
              <div class="member-avatar frontend-avatar">BP</div>
              <div class="member-badge frontend-badge">Frontend</div>
              <h3 class="member-name">Benjamin Popma</h3>
              <p class="member-role">Frontend Developer</p>
              <p class="member-desc">
                Worked on responsive design and interactive components.
              </p>
              <div class="member-skills">
                <span class="skill-tag">Vue.js</span>
                <span class="skill-tag">HTML</span>
                <span class="skill-tag">CSS</span>
              </div>
            </div>

            <!-- Backend Developers -->
            <div class="team-card">
              <div class="member-avatar backend-avatar">KM</div>
              <div class="member-badge backend-badge">Backend</div>
              <h3 class="member-name">Kanishaka Madan</h3>
              <p class="member-role">Backend Developer</p>
              <p class="member-desc">
                Developed API endpoints and database functionality.
              </p>
              <div class="member-skills">
                <span class="skill-tag">FastAPI</span>
                <span class="skill-tag">Python</span>
              </div>
            </div>

            <div class="team-card">
              <div class="member-avatar backend-avatar">NN</div>
              <div class="member-badge backend-badge">Backend</div>
              <h3 class="member-name">Nicolai Nunez</h3>
              <p class="member-role">Backend Developer</p>
              <p class="member-desc">
                Contributed to server-side logic and data management.
              </p>
              <div class="member-skills">
                <span class="skill-tag">FastAPI</span>
                <span class="skill-tag">Python</span>
              </div>
            </div>
          </div>
        </section>

        <!-- Features Highlight -->
        <section class="features-section">
          <h2 class="section-title">
            <span class="section-icon">✨</span>
            Key Features
          </h2>
          <div class="features-grid">
            <div class="feature-card">
              <span class="feature-icon">🔍</span>
              <h4>Smart Search</h4>
              <p>Find opportunities by type, location, or keywords</p>
            </div>
            <div class="feature-card">
              <span class="feature-icon">📝</span>
              <h4>Easy Applications</h4>
              <p>Apply directly through the platform</p>
            </div>
            <div class="feature-card">
              <span class="feature-icon">💾</span>
              <h4>Save & Track</h4>
              <p>Bookmark opportunities for later</p>
            </div>
            <div class="feature-card">
              <span class="feature-icon">🛡️</span>
              <h4>AI Moderation</h4>
              <p>Safe content through smart filtering</p>
            </div>
            <div class="feature-card">
              <span class="feature-icon">📱</span>
              <h4>Mobile Ready</h4>
              <p>Works great on any device</p>
            </div>
            <div class="feature-card">
              <span class="feature-icon">⚡</span>
              <h4>Fast & Modern</h4>
              <p>Built with cutting-edge tech</p>
            </div>
            <div class="feature-card">
              <span class="feature-icon">👤</span>
              <h4>User Accounts</h4>
              <p>Create posts and manage applications</p>
            </div>
            <div class="feature-card">
              <span class="feature-icon">🎯</span>
              <h4>Advanced Filters</h4>
              <p>Filter by type, grade, and time commitment</p>
            </div>
            <div class="feature-card">
              <span class="feature-icon">📊</span>
              <h4>Application Dashboard</h4>
              <p>Track and manage all your applications</p>
            </div>
            <div class="feature-card">
              <span class="feature-icon">🔗</span>
              <h4>External Links</h4>
              <p>Apply through external websites when available</p>
            </div>
            <div class="feature-card">
              <span class="feature-icon">⚖️</span>
              <h4>Appeal System</h4>
              <p>Fair review process for moderated content</p>
            </div>
            <div class="feature-card">
              <span class="feature-icon">🚨</span>
              <h4>Report Content</h4>
              <p>Help keep the platform safe and reliable</p>
            </div>
            <div class="feature-card">
              <span class="feature-icon">📧</span>
              <h4>Email Support</h4>
              <p>Contact us directly through the platform</p>
            </div>
            <div class="feature-card">
              <span class="feature-icon">🔐</span>
              <h4>Secure Authentication</h4>
              <p>Safe login with encrypted passwords</p>
            </div>
            <div class="feature-card">
              <span class="feature-icon">👥</span>
              <h4>User Profiles</h4>
              <p>Personalized profiles and activity tracking</p>
            </div>
            <div class="feature-card">
              <span class="feature-icon">🔄</span>
              <h4>Real-time Updates</h4>
              <p>Get instant notifications and updates</p>
            </div>
            <div class="feature-card">
              <span class="feature-icon">🎨</span>
              <h4>Responsive Design</h4>
              <p>Beautiful interface that works everywhere</p>
            </div>
            <div class="feature-card">
              <span class="feature-icon">📈</span>
              <h4>Analytics Dashboard</h4>
              <p>Track your posts and application statistics</p>
            </div>
          </div>
        </section>

        <!-- Call to Action -->
        <section class="cta-section">
          <div class="cta-card">
            <h2>Ready to explore opportunities?</h2>
            <p>Join Opportunity Hub and discover what's waiting for you.</p>
            <div class="cta-buttons">
              <router-link to="/signup" class="btn btn-cta-primary">Get Started</router-link>
              <router-link to="/login" class="btn btn-cta-secondary">Sign In</router-link>
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

.about-page{
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

.desktop-nav{ display:flex; align-items:center; gap:14px; }

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

/* Hero Section */
.hero-section{
  text-align:center;
  margin-bottom:48px;
}

.hero-badge{
  display:inline-block;
  padding:6px 16px;
  border-radius:999px;
  background:linear-gradient(135deg, rgba(37,99,235,.1), rgba(20,184,166,.1));
  color:var(--accent);
  font-size:13px;
  font-weight:700;
  margin-bottom:16px;
}

.hero-title{
  font-size:clamp(32px, 6vw, 48px);
  font-weight:800;
  background:linear-gradient(135deg, var(--accent), var(--accent-2));
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  margin-bottom:12px;
}

.hero-subtitle{
  font-size:18px;
  color:#64748b;
  max-width:500px;
  margin:0 auto;
}

/* Mission Section */
.mission-section{
  margin-bottom:48px;
}

.mission-card{
  background:linear-gradient(135deg, rgba(37,99,235,.04), rgba(20,184,166,.04));
  border:1px solid rgba(37,99,235,.15);
  border-radius:24px;
  padding:40px;
  text-align:center;
}

.mission-icon{
  font-size:48px;
  margin-bottom:16px;
}

.mission-card h2{
  font-size:24px;
  font-weight:800;
  margin-bottom:20px;
  color:var(--text);
}

.mission-text{
  font-size:16px;
  line-height:1.7;
  color:#64748b;
  max-width:700px;
  margin:0 auto 16px;
}

.mission-text strong{
  color:var(--text);
}

/* Problem Section */
.problem-section{
  margin-bottom:48px;
}

.problem-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit, minmax(280px, 1fr));
  gap:24px;
}

.problem-card{
  background:var(--card);
  border-radius:20px;
  padding:28px;
  border:1px solid rgba(148,163,184,.15);
}

.card-header{
  display:flex;
  align-items:center;
  gap:12px;
  margin-bottom:20px;
  padding-bottom:16px;
  border-bottom:1px solid rgba(148,163,184,.15);
}

.card-header.problem{ border-color:rgba(239,68,68,.2); }
.card-header.solution{ border-color:rgba(34,197,94,.2); }

.card-icon{
  font-size:28px;
}

.card-header h3{
  font-size:18px;
  font-weight:700;
}

.problem-list,
.solution-list{
  list-style:none;
  display:flex;
  flex-direction:column;
  gap:12px;
}

.problem-list li,
.solution-list li{
  display:flex;
  align-items:flex-start;
  gap:10px;
  font-size:14px;
  color:#64748b;
  line-height:1.5;
}

.problem-list li::before{
  content:'✗';
  color:#ef4444;
  font-weight:700;
  flex-shrink:0;
}

.solution-list li::before{
  content:'✓';
  color:#22c55e;
  font-weight:700;
  flex-shrink:0;
}

/* Vision Section */
.vision-section{
  margin-bottom:48px;
}

.section-title{
  display:flex;
  align-items:center;
  gap:12px;
  font-size:22px;
  font-weight:700;
  margin-bottom:24px;
}

.section-icon{
  font-size:28px;
}

.vision-content{
  background:var(--card);
  border-radius:20px;
  padding:32px;
  border:1px solid rgba(148,163,184,.15);
}

.vision-content > p{
  font-size:16px;
  line-height:1.7;
  color:#64748b;
  margin-bottom:24px;
}

.vision-content > p strong{
  color:var(--text);
}

.vision-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit, minmax(220px, 1fr));
  gap:16px;
  margin-bottom:24px;
}

.vision-item{
  display:flex;
  align-items:flex-start;
  gap:12px;
  padding:16px;
  background:rgba(37,99,235,.03);
  border-radius:12px;
}

.vision-emoji{
  font-size:24px;
  flex-shrink:0;
}

.vision-item p{
  font-size:13px;
  color:#64748b;
  line-height:1.5;
}

.vision-closing{
  font-style:italic;
  text-align:center;
  padding-top:16px;
  border-top:1px solid rgba(148,163,184,.15);
  color:#64748b;
}

/* Team Section */
.team-section{
  margin-bottom:48px;
}

.team-intro{
  color:#64748b;
  margin-bottom:32px;
  font-size:16px;
}

.team-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit, minmax(240px, 1fr));
  gap:20px;
}

.team-card{
  background:var(--card);
  border-radius:20px;
  padding:28px;
  text-align:center;
  border:1px solid rgba(148,163,184,.15);
  transition:transform 0.2s, box-shadow 0.2s;
}

.team-card:hover{
  transform:translateY(-4px);
  box-shadow:0 16px 40px rgba(15,23,42,.08);
}

.team-card.leader{
  grid-column:1 / -1;
  background:linear-gradient(135deg, rgba(37,99,235,.03), rgba(20,184,166,.03));
  border-color:rgba(37,99,235,.2);
}

@media (min-width: 768px){
  .team-card.leader{
    grid-column:span 1;
  }
}

.member-avatar{
  width:72px;
  height:72px;
  border-radius:999px;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:24px;
  font-weight:800;
  color:#fff;
  margin:0 auto 12px;
}

.leader-avatar{
  background:linear-gradient(135deg, var(--accent), var(--accent-2));
  width:84px;
  height:84px;
  font-size:28px;
}

.frontend-avatar{
  background:linear-gradient(135deg, #8b5cf6, #a855f7);
}

.backend-avatar{
  background:linear-gradient(135deg, #f59e0b, #ea580c);
}

.member-badge{
  display:inline-block;
  padding:4px 12px;
  border-radius:999px;
  font-size:11px;
  font-weight:700;
  text-transform:uppercase;
  letter-spacing:.03em;
  margin-bottom:12px;
}

.leader-badge{
  background:linear-gradient(90deg, var(--accent), var(--accent-2));
  color:#fff;
}

.frontend-badge{
  background:rgba(139,92,246,.15);
  color:#7c3aed;
}

.backend-badge{
  background:rgba(245,158,11,.15);
  color:#d97706;
}

.member-name{
  font-size:18px;
  font-weight:700;
  margin-bottom:4px;
}

.member-role{
  font-size:13px;
  color:var(--accent);
  font-weight:600;
  margin-bottom:12px;
}

.member-desc{
  font-size:13px;
  color:#64748b;
  line-height:1.5;
  margin-bottom:16px;
}

.member-skills{
  display:flex;
  flex-wrap:wrap;
  justify-content:center;
  gap:6px;
}

.skill-tag{
  padding:4px 10px;
  border-radius:6px;
  background:rgba(148,163,184,.1);
  font-size:11px;
  font-weight:600;
  color:#64748b;
}

/* Features Section */
.features-section{
  margin-bottom:48px;
}

.features-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit, minmax(160px, 1fr));
  gap:16px;
}

.feature-card{
  background:var(--card);
  border-radius:16px;
  padding:24px 16px;
  text-align:center;
  border:1px solid rgba(148,163,184,.15);
}

.feature-icon{
  font-size:32px;
  margin-bottom:12px;
  display:block;
}

.feature-card h4{
  font-size:14px;
  font-weight:700;
  margin-bottom:6px;
}

.feature-card p{
  font-size:12px;
  color:#64748b;
  line-height:1.4;
}

/* CTA Section */
.cta-section{
  margin-bottom:24px;
}

.cta-card{
  background:linear-gradient(135deg, var(--accent), var(--accent-2));
  border-radius:24px;
  padding:48px 32px;
  text-align:center;
  color:#fff;
}

.cta-card h2{
  font-size:clamp(22px, 4vw, 28px);
  font-weight:800;
  margin-bottom:12px;
}

.cta-card p{
  font-size:16px;
  opacity:0.9;
  margin-bottom:24px;
}

.cta-buttons{
  display:flex;
  justify-content:center;
  gap:12px;
  flex-wrap:wrap;
}

.btn-cta-primary{
  padding:12px 28px;
  border-radius:12px;
  font-size:14px;
  font-weight:700;
  text-decoration:none;
  transition:all 0.2s ease;
  cursor:pointer;
  border:none;
  background:#fff;
  color:var(--accent);
}

.btn-cta-primary:hover{
  transform:translateY(-2px);
  box-shadow:0 8px 20px rgba(0,0,0,.2);
}

.btn-cta-secondary{
  padding:12px 28px;
  border-radius:12px;
  font-size:14px;
  font-weight:700;
  text-decoration:none;
  transition:all 0.2s ease;
  cursor:pointer;
  background:rgba(255,255,255,.15);
  color:#fff;
  border:1px solid rgba(255,255,255,.3);
}

.btn-cta-secondary:hover{
  background:rgba(255,255,255,.25);
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
  color:#64748b;
  text-decoration:none;
  font-size:13px;
}

.footer-links a:hover{
  color:var(--accent);
}

.muted{ color:#64748b; }
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
  
  .mission-card{ padding:28px 20px; }
  .problem-grid{ grid-template-columns:1fr; }
  .vision-grid{ grid-template-columns:1fr; }
  .team-grid{ grid-template-columns:1fr; }
  .features-grid{ grid-template-columns:repeat(2, 1fr); }
  
  .footer-inner{
    flex-direction:column;
    text-align:center;
  }
}

@media (max-width: 480px){
  .features-grid{ grid-template-columns:1fr; }
  .cta-buttons{ flex-direction:column; }
  .btn-cta-primary, .btn-cta-secondary{ width:100%; text-align:center; }
}
</style>
