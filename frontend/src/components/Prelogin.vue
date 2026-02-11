<template>
  <div class="prelog">
    <header>
      <div class="container nav">
        <a class="brand" href="#">
          <!-- New logo: simple "hub" network icon -->
          <svg viewBox="0 0 64 64" aria-hidden="true">
            <defs>
              <!-- Gradient for strokes/fills -->
              <linearGradient id="oh-search-g" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0" stop-color="#2563eb" />
                <stop offset="1" stop-color="#14b8a6" />
              </linearGradient>
            </defs>

            <!-- Soft background glow -->
            <circle
              cx="28"
              cy="28"
              r="18"
              fill="url(#oh-search-g)"
              opacity="0.08"
            />

            <!-- Magnifying glass circle -->
            <circle
              cx="28"
              cy="28"
              r="12"
              fill="none"
              stroke="url(#oh-search-g)"
              stroke-width="3"
            />

            <!-- Magnifying glass handle -->
            <path
              d="M36 36 L46 46"
              stroke="url(#oh-search-g)"
              stroke-width="3.2"
              stroke-linecap="round"
            />

            <!-- Spark: small star near top-right -->
            <path
              d="M44 16 L44 20 M42 18 L46 18"
              stroke="url(#oh-search-g)"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
            <circle
              cx="44"
              cy="18"
              r="1.5"
              fill="url(#oh-search-g)"
            />
          </svg>

          Opportunity Hub
        </a>
        

        <!-- header buttons -->
        <nav class="navlinks desktop-nav">
          <a href="#about" @click.prevent="scrollToSection('about')">About</a>
          <a href="#areas" @click.prevent="scrollToSection('areas')">Areas</a>
          <a href="#how" @click.prevent="scrollToSection('how')">How it works</a>
          <a href="#faq" @click.prevent="scrollToSection('faq')">FAQ</a>
          <RouterLink to="/about">About Us</RouterLink>
          <RouterLink to="/references">References</RouterLink>
          <RouterLink class="btn btn-primary" to="/signup">Sign up</RouterLink>
          <RouterLink class="btn btn-outline" to="/login">Log in</RouterLink>
        </nav>

    
          <!-- Hamburger button -->
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

        <!-- Mobile menu -->
              
        <nav class="mobile-nav" :class="{ active: isMenuOpen }">
          <a href="#about" @click="closeMenu">About</a>
          <a href="#areas" @click="closeMenu">Areas</a>
          <a href="#community-orgs" @click="closeMenu">Community</a>
          <a href="#how" @click="closeMenu">How it works</a>
          <a href="#faq" @click="closeMenu">FAQ</a>
          <RouterLink to="/about" @click="closeMenu">About Us</RouterLink>
          <RouterLink to="/references" @click="closeMenu">References</RouterLink>
          <div class="mobile-nav-buttons">
            <RouterLink class="btn btn-primary" to="/signup" @click="closeMenu">Sign up</RouterLink>
            <RouterLink class="btn btn-outline" to="/login" @click="closeMenu">Log in</RouterLink>
          </div>
        </nav>
      </header>


    <main class="container">
      <!-- HERO -->
      <section class="hero">
        <div class="hero-copy">
          <span class="badge">Student Community Resource Hub</span>
          <h1>All your internships, clubs, and tutoring in one place.</h1>
          <p>
            Opportunity Hub is a community resource hub designed for students—a vital subgroup of the local community—providing centralized access to educational, career, and service-oriented resources.
          </p>
          <p>
            Search real community resources filtered by grade, interest, and time
            commitment. Built by students, for students.
          </p>

          <ul class="hero-points">
            <li>Verified community resources only</li>
            <li>Smart filters and saved favorites</li>
            <li>Free accounts for students and educators</li>
          </ul>

          <div class="hero-ctas">
            <RouterLink class="btn btn-primary" to="/signup">
              Create a free account
            </RouterLink>
            <a class="btn btn-ghost" href="#areas" @click.prevent="scrollToSection('areas')">
              Preview areas
            </a>
          </div>

          <p class="muted hero-subnote">
            No credit card. No spam. Log in any time to see full community resources.
          </p>
        </div>

        <div class="panel hero-panel">
          <div class="hero-panel-header">
            <span class="kicker">Live preview</span>
            <span class="hero-panel-tag">Signed out view</span>
          </div>

          <div
            class="search"
            role="search"
            aria-labelledby="search-label"
          >
            <label
              id="search-label"
              class="sr-only"
              for="demo-search"
            >
              Search example cards
            </label>
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
              <path d="M13.5 13.5l4 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
              <circle cx="9" cy="9" r="6" stroke="currentColor" stroke-width="2" />
            </svg>
            <input
              id="demo-search"
              v-model="query"
              placeholder="Try: ‘summer internship’ or ‘math tutoring’"
              aria-describedby="search-help"
              autocomplete="off"
            />
          </div>
          <p id="search-help" class="muted search-help">
            Typing filters the sample cards in real time.
          </p>

          <div class="taglist taglist-chips">
            <button
              v-for="cat in categories"
              :key="cat.key"
              class="pill"
              :data-filter="cat.key"
              :data-active="activeFilter === cat.key"
              :aria-pressed="String(activeFilter === cat.key)"
              @click="setFilter(cat.key)"
              type="button"
            >
              {{ cat.label }}
            </button>
          </div>

          <div id="demo-results" class="cards cards-2" aria-live="polite">
            <article
              v-for="card in filteredCards"
              :key="card.id"
              class="card"
              :class="card.category"
            >
              <h3>{{ card.title }}</h3>
              <p>{{ card.desc }}</p>
            </article>

            <article v-if="filteredCards.length === 0" class="card">
              <h3>No results</h3>
              <p class="muted">Try a different term or category.</p>
            </article>
          </div>

          <p class="muted hero-panel-footer">
            Log in to see full community resources, deadlines, and application links.
          </p>
        </div>
      </section>

      <!-- STATS STRIP -->
      <section class="stats">
        <div class="stat">
          <div class="stat-label">Community Resources in the hub</div>
          <div class="stat-value">{{ opportunityCount != null ? opportunityCount + '+' : '—' }}</div>
        </div>
        <div class="stat">
          <div class="stat-label">Resource Categories</div>
          <div class="stat-value">4</div>
        </div>
        <div class="stat">
          <div class="stat-label">Built for</div>
          <div class="stat-value">High-school students</div>
        </div>
      </section>

      <!-- ABOUT / WHO -->
      <section id="about" class="grid-2 section-gap">
        <div class="panel align-left">
          <span class="kicker">What is this?</span>
          <h2>A focused hub for real student opportunities</h2>
          <p class="muted">
            Instead of digging through random flyers and dozens of sites,
            Opportunity Hub pulls trusted internships, tutoring, community
            service, and clubs into one searchable place.
          </p>
          <ul class="muted feature-list">
            <li>✅ Always free to browse and apply</li>
            <li>✅ Filter by interest, grade, and time commitment</li>
            <li>✅ Save favorites and get reminders after login</li>
          </ul>
        </div>

        <div class="panel">
          <span class="kicker">Who is it for?</span>
          <h2>Students, mentors, and educators</h2>
          <p class="muted">
            Whether you want to build a resume, find help in a class,
            or fill a club with engaged members, the Hub makes it fast.
          </p>
          <div class="persona-chips">
            <span class="pill">High-schoolers</span>
            <span class="pill">Mentors</span>
            <span class="pill">Club leaders</span>
            <span class="pill">Counselors</span>
          </div>
        </div>
      </section>

      <!-- AREAS -->
      <section id="areas" class="panel section-gap" aria-labelledby="areas-title">
        <div class="section-header">
          <div>
            <span class="kicker">Community Resources</span>
            <h2 id="areas-title">Community Programs for Students</h2>
            <p class="muted">
              These are the main sections you’ll find once you log in.
            </p>
          </div>
          <div class="taglist">
            <span class="pill">STEM</span>
            <span class="pill">Arts</span>
            <span class="pill">Civic</span>
            <span class="pill">Business</span>
            <span class="pill">Sports</span>
          </div>
        </div>

        <div class="cards cards-4">
          <article class="card">
            <h3>Internships</h3>
            <p>Local and remote, paid or for credit. Learn by doing.</p>
          </article>
          <article class="card">
            <h3>Tutoring</h3>
            <p>Get help or give help with verified peer and adult tutors.</p>
          </article>
          <article class="card">
            <h3>Community Service</h3>
            <p>Earn hours with meaningful, vetted projects.</p>
          </article>
          <article class="card">
            <h3>Clubs</h3>
            <p>Find clubs at your school or citywide and see meeting times.</p>
          </article>
        </div>
      </section>

      <!-- HOW IT WORKS -->
      <section id="how" class="panel section-gap">
        <span class="kicker">How it works</span>
        <h2>Three simple steps</h2>
        <div class="steps">
          <div class="step">
            <div class="num">1</div>
            <h3>Create your account</h3>
            <p class="muted">
              Use your school email or any email. No payment needed.
            </p>
          </div>
          <div class="step">
            <div class="num">2</div>
            <h3>Browse and save</h3>
            <p class="muted">
              Filter by interest, grade, schedule, or location. Save favorites.
            </p>
          </div>
          <div class="step">
            <div class="num">3</div>
            <h3>Apply or join</h3>
            <p class="muted">
              In one click, go to the official application, sign-up form,
              or club info.
            </p>
          </div>
        </div>
      </section>

      <!-- CTA + QUESTIONS -->
      <section id="cta" class="grid-2 section-gap">
        <div class="panel">
          <h2>Ready to explore?</h2>
          <p class="muted">
            Create a free account to unlock the full directory, application links,
            favorites, reminders, and more.
          </p>
          <div class="hero-ctas">
            <RouterLink class="btn btn-primary" to="/signup">
              Sign up — it’s free
            </RouterLink>
            <RouterLink class="btn btn-ghost" to="/login">
              Log in
            </RouterLink>
          </div>
          <p class="muted tiny">
            Perfect for school projects, competitions, or a real deployment.
          </p>
        </div>

        <div class="panel align-left">
          <h3>Questions before you join?</h3>
          <details class="faq-item">
            <summary class="muted">
              <strong>What can I do here before logging in?</strong>
            </summary>
            <p class="muted">
              You can see how the Hub works and browse example cards.
              Full community resources and application links appear after you create a free account.
            </p>
          </details>
          <details class="faq-item">
            <summary class="muted">
              <strong>Do I need an account to see community resources?</strong>
            </summary>
            <p class="muted">
              Yes. A free account lets you view the full directory, save favorites,
              and apply or join.
            </p>
          </details>
          <details class="faq-item">
            <summary class="muted">
              <strong>How much does it cost?</strong>
            </summary>
            <p class="muted">
              It is 100% free for students and educators. No hidden fees.
            </p>
          </details>
          <details class="faq-item">
            <summary class="muted">
              <strong>Who can use the Hub?</strong>
            </summary>
            <p class="muted">
              High-school students and educators. Some community resources may be regional
              or have age or grade requirements.
            </p>
          </details>
          <details class="faq-item">
            <summary class="muted">
              <strong>Where do community resources come from?</strong>
            </summary>
            <p class="muted">
              From verified organizations, schools, and club leaders.
              We review and update them regularly.
            </p>
          </details>
          <details class="faq-item">
            <summary class="muted">
              <strong>Can I add a community resource?</strong>
            </summary>
            <p class="muted">
              Yes. After creating an account, you will see a “Post a community resource” button
              with a short form.
            </p>
          </details>
        </div>
      </section>

      <!-- FAQ SHORT -->
      <section id="faq" class="faq panel section-gap-bottom">
        <span class="kicker">FAQ</span>
        <h2>Quick answers</h2>
        <details open>
          <summary><strong>Is my data safe?</strong></summary>
          <p class="muted">
            We collect the minimum needed to run your account and never sell your data.
            You can delete your account at any time.
          </p>
        </details>
        <details>
          <summary><strong>Accessibility</strong></summary>
          <p class="muted">
            We use semantic tags, solid contrast, keyboard focus, and aria labels.
            Please test with your standards and report issues.
          </p>
        </details>
      </section>
    </main>

    <footer>
      <div class="container">
        <div class="footer-inner">
          <p class="muted">
            © <span>{{ year }}</span> Opportunity Hub. Built by students, for students.
          </p>
          <div class="taglist">
            <RouterLink class="pill" to="/about">About Us</RouterLink>
            <RouterLink class="pill" to="/references">References</RouterLink>
            <button class="pill" type="button" @click="openPrivacy">Privacy</button>
            <button class="pill" type="button" @click="openContact">Contact</button>
          </div>
        </div>
      </div>
    </footer>

    <!-- Privacy Modal -->
    <div v-if="isPrivacyOpen" class="modal-backdrop" @click.self="isPrivacyOpen = false">
      <div class="modal">
        <h3>Privacy</h3>
        <p class="muted">
          Opportunity Hub stores your account info (username, email) and the posts you create.
          Applications you submit are visible to the creator of that post. Password encryption
          is implemented using hashing and salting techniques to ensure safety and security.
          We don't sell your data.
        </p>
        <div class="op-actions">
          <button class="btn btn-primary small-btn" type="button" @click="isPrivacyOpen = false">
            Done
          </button>
        </div>
      </div>
    </div>

    <!-- Contact Modal -->
    <div v-if="isContactOpen" class="modal-backdrop" @click.self="isContactOpen = false">
      <div class="modal">
        <h3>Contact</h3>
        <p class="muted small-text">Please sign in to send us a message.</p>
        <div class="op-actions">
          <button class="btn btn-ghost small-btn" type="button" @click="isContactOpen = false">
            Close
          </button>
          <RouterLink to="/login" class="btn btn-primary small-btn" @click="isContactOpen = false">
            Sign In
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

  
  <script setup>
  import { ref, computed, onMounted } from 'vue';
  import AxiosInstance from '@/apiClient';
  
  // Search + filtering state
  const query = ref('');
  const activeFilter = ref('all');
  const isMenuOpen = ref(false);

  function toggleMenu() {
    isMenuOpen.value = !isMenuOpen.value;
  }

  function closeMenu() {
    isMenuOpen.value = false;
  }
  
  const categories = [
    { key: 'all',         label: 'All' },
    { key: 'internships', label: 'Internships' },
    { key: 'tutoring',    label: 'Tutoring' },
    { key: 'service',     label: 'Community Service' },
    { key: 'clubs',       label: 'Clubs' }
  ];
  
  const cards = ref([
    { id: 1, category: 'internships', title: 'City Tech Summer Intern', desc: '8-week paid internship for HS students. Applications open in March.' },
    { id: 2, category: 'tutoring',    title: 'Peer Tutoring — Algebra II', desc: 'Request or offer tutoring sessions; match within your school network.' },
    { id: 3, category: 'service',     title: 'Park Clean-Up Saturdays', desc: 'Earn verified service hours at weekly neighborhood events.' },
    { id: 4, category: 'clubs',       title: 'Entrepreneurship Club', desc: 'Pitch nights, guest speakers, and micro-grants for student projects.' }
  ]);
  
  const filteredCards = computed(() => {
    const q = query.value.trim().toLowerCase();
    return cards.value.filter(c => {
      const matchesFilter = activeFilter.value === 'all' || c.category === activeFilter.value;
      const matchesQuery =
        !q ||
        c.title.toLowerCase().includes(q) ||
        c.desc.toLowerCase().includes(q);
      return matchesFilter && matchesQuery;
    });
  });
  
  function setFilter(key) {
    activeFilter.value = key;
  }

  function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
      // Update URL hash without creating history entry
      window.history.replaceState(null, '', `#${sectionId}`);
    }
  }
  
  // Footer year (simple const is fine in <script setup>)
  const year = new Date().getFullYear();

  // Opportunity count (fetched from API)
  const opportunityCount = ref(null);
  onMounted(async () => {
    try {
      const res = await AxiosInstance.get('/opportunities/count');
      const n = res.data?.count;
      opportunityCount.value = typeof n === 'number' ? n : null;
    } catch {
      opportunityCount.value = null;
    }
  });
  
  // Privacy modal
  const isPrivacyOpen = ref(false);
  
  function openPrivacy() {
    isPrivacyOpen.value = true;
    closeMenu();
  }
  
  // Contact modal
  const isContactOpen = ref(false);
  
  function openContact() {
    isContactOpen.value = true;
    closeMenu();
  }
  </script>
  
  <style scoped>

:global(:root){
  /* Light, friendly “education” theme */
  --bg:#f3f4ff;
  --bg-soft:#eef2ff;
  --panel:#ffffff;
  --panel-elevated:#ffffff;
  --muted:#000000;
  --text:#0f172a;
  --accent:#2563eb;   /* blue */
  --accent-2:#14b8a6; /* teal */
  --ring:rgba(37,99,235,.25);
  --card:#ffffff;
  --card-2:#f9fafb;
  --success:#22c55e;
  --warning:#eab308;
  --danger:#f97373;
  --radius:18px;
  --shadow:0 18px 40px rgba(15,23,42,.08);
  --border:1px solid rgba(15,23,42,.06);
}

/* Utility: visually hidden but accessible */
.sr-only{
  position:absolute!important;
  width:1px!important;height:1px!important;
  padding:0!important;margin:-1px!important;
  overflow:hidden!important;clip:rect(0,0,0,0)!important;
  white-space:nowrap!important;border:0!important;
}

*{box-sizing:border-box}

.prelog{
  min-height:100vh;
  background:
    radial-gradient(900px 500px at 10% -10%, rgba(59,130,246,.20), transparent 60%),
    radial-gradient(900px 600px at 90% 110%, rgba(45,212,191,.18), transparent 60%),
    var(--bg);
  color:var(--text);
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, "Helvetica Neue", Arial;
}

a{color:inherit;text-decoration:none}

.container{
  max-width:1200px;
  margin:0 auto;
  padding:24px 24px 32px;
}

header{
  position:sticky;
  top:0;
  z-index:20;
  background:rgba(248,250,252,.86);
  backdrop-filter: blur(12px);
  border-bottom:1px solid rgba(148,163,184,.25);
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

.btn-ghost{
  background:transparent;
  border:1px solid rgba(148,163,184,.5);
  color:var(--muted);
}

/* HERO */

.hero{
  display:grid;
  grid-template-columns:minmax(0,1.05fr) minmax(0,1.1fr);
  gap:32px;
  align-items:center;
  padding:48px 0 24px;
}

.hero-copy h1{
  font-size:40px;
  line-height:1.05;
  margin:12px 0 10px;
}

.hero-copy p{
  color:var(--muted);
  font-size:16px;
  max-width:46ch;
}

.badge{
  display:inline-flex;
  align-items:center;
  gap:6px;
  border-radius:999px;
  border:1px solid rgba(148,163,184,.5);
  padding:4px 10px;
  font-size:11px;
  color:var(--muted);
  background:rgba(255,255,255,.9);
}

.hero-points{
  margin:14px 0 14px;
  padding:0;
  list-style:none;
  color:var(--muted);
  font-size:14px;
  display:grid;
  gap:4px;
}

.hero-points li::before{
  content:"• ";
  color:var(--accent);
}

.hero-ctas{
  margin-top:10px;
  display:flex;
  flex-wrap:wrap;
  gap:10px;
}

.hero-subnote{
  margin-top:10px;
  font-size:13px;
}

/* HERO PANEL */

.hero-panel{
  background:
    radial-gradient(circle at top left, rgba(59,130,246,.16), transparent 60%),
    radial-gradient(circle at bottom right, rgba(45,212,191,.18), transparent 60%),
    var(--panel-elevated);
  border-radius:22px;
  padding:18px 18px 16px;
  border:var(--border);
  box-shadow:var(--shadow);
}

.hero-panel-header{
  display:flex;
  align-items:center;
  justify-content:space-between;
  margin-bottom:8px;
}

.hero-panel-tag{
  font-size:11px;
  padding:4px 8px;
  border-radius:999px;
  border:1px solid rgba(148,163,184,.6);
  color:var(--muted);
  background:rgba(255,255,255,.9);
}

.hero-panel-footer{
  margin-top:10px;
  font-size:12px;
  color:var(--muted);
}

/* SEARCH */

.search{
  display:flex;
  gap:10px;
  align-items:center;
  background:#f9fafb;
  border:1px solid rgba(148,163,184,.7);
  padding:10px 12px;
  border-radius:12px;
}

.search svg{
  color:var(--muted);
}

.search input{
  flex:1;
  background:transparent;
  border:0;
  outline:0;
  color:var(--text);
  font-size:14px;
}

.search input::placeholder{
  color:#9ca3af;
}

.search-help{
  margin:6px 2px 4px;
  font-size:11px;
}

/* TAGS & PILLS */

.taglist{
  display:flex;
  gap:8px;
  flex-wrap:wrap;
}

.taglist-chips{
  margin:10px 0 14px;
}

.pill{
  font-size:12px;
  border:1px solid rgba(148,163,184,.55);
  padding:6px 10px;
  border-radius:999px;
  color:var(--muted);
  background:#ffffff;
  white-space:nowrap;
}

.pill[data-active="true"]{
  background:linear-gradient(90deg, var(--accent), var(--accent-2));
  color:#fff;
  border:none;
}

.persona-chips{
  display:flex;
  gap:8px;
  flex-wrap:wrap;
  margin-top:10px;
}

/* PANELS & CARDS */

.panel{
  background:var(--panel);
  border:var(--border);
  border-radius:var(--radius);
  padding:20px 18px 18px;
  box-shadow:var(--shadow);
}

.cards{
  display:grid;
  gap:14px;
}

.cards-2{
  grid-template-columns:repeat(2,minmax(0,1fr));
}

.cards-4{
  grid-template-columns:repeat(4,minmax(0,1fr));
  margin-top:16px;
}

.card{
  background:linear-gradient(180deg,var(--card),var(--card-2));
  border-radius:14px;
  border:1px solid rgba(148,163,184,.35);
  padding:14px 14px 12px;
  box-shadow:0 10px 22px rgba(15,23,42,.08);
}

.card h3{
  margin:4px 0 6px;
  font-size:16px;
}

.card p{
  margin:0;
  color:var(--muted);
  font-size:13px;
}

/* STATS */

.stats{
  display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));
  gap:14px;
  margin:8px 0 24px;
}

.stat{
  background:linear-gradient(120deg,#ffffff,#e0f2fe);
  border-radius:14px;
  padding:12px 14px;
  border:1px solid rgba(148,163,184,.45);
  box-shadow:0 10px 22px rgba(15,23,42,.08);
}

.stat-label{
  font-size:11px;
  text-transform:uppercase;
  letter-spacing:.12em;
  color:var(--muted);
}

.stat-value{
  font-size:18px;
  font-weight:600;
  margin-top:4px;
}

/* SECTIONS */

.section-header{
  display:flex;
  align-items:flex-start;
  justify-content:space-between;
  gap:16px;
  flex-wrap:wrap;
}

.section-gap{
  margin:24px 0;
}

.section-gap-bottom{
  margin-bottom:24px;
}

.grid-2{
  display:grid;
  grid-template-columns:1.1fr 0.9fr;
  gap:18px;
}

.steps{
  display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));
  gap:14px;
  margin-top:10px;
}

.step{
  padding:14px 14px 12px;
  border-radius:14px;
  border:1px dashed rgba(148,163,184,.7);
  background:linear-gradient(180deg,#ffffff,#eff6ff);
}

.step .num{
  width:26px;
  height:26px;
  border-radius:999px;
  display:inline-flex;
  align-items:center;
  justify-content:center;
  background:#eff6ff;
  border:1px solid rgba(59,130,246,.7);
  margin-bottom:6px;
  font-size:13px;
  color:var(--accent);
}

/* FAQ */

.faq details{
  background:#ffffff;
  border:var(--border);
  padding:12px 12px;
  border-radius:12px;
}

.faq details+details{
  margin-top:8px;
}

.faq-item{
  margin-bottom:8px;
}

.muted{
  color:var(--muted);
}

.kicker{
  font-size:11px;
  letter-spacing:.14em;
  text-transform:uppercase;
  color:var(--muted);
}

.feature-list{
  margin-top:10px;
  padding-left:0;
  list-style:none;
}

.feature-list li{
  margin-bottom:4px;
}

.tiny{
  margin-top:10px;
  font-size:12px;
}

/* FOOTER */

footer{
  padding:16px 0 20px;
  border-top:1px solid rgba(148,163,184,.35);
  color:var(--muted);
  background:rgba(248,250,252,.9);
}

.footer-inner{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:12px;
  flex-wrap:wrap;
}

/* ALIGN UTIL */

.align-left,
.align-left *{
  text-align:left !important;
}

/* Hamburger */
/* Hamburger Menu */
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
}

/* RESPONSIVE */

@media (max-width: 900px){
  .hero{
    grid-template-columns:1fr;
    padding-top:32px;
  }

  .hero-copy h1{
    font-size:32px;
  }

  .cards-4{
    grid-template-columns:repeat(2,minmax(0,1fr));
  }

  .steps{
    grid-template-columns:1fr;
  }

  .grid-2{
    grid-template-columns:1fr;
  }

  .stats{
    grid-template-columns:repeat(3,minmax(0,1fr));
  }
}

@media (max-width: 640px){
  .container{
    padding:18px 16px 28px;
  }


    .navlinks a:not(:first-child) {display: none;};

    .navlinks a.icon {
    float: right;
    display: block;
    }

  .navlinks.responsive {position: relative;}
  .navlinks.responsive a.icon {
    position: absolute;
    right: 0;
    top: 0;
  }
  .topnav.responsive a {
    float: none;
    display: block;
    text-align: left;
  }


  .cards-4,
  .cards-2,
  .stats{
    grid-template-columns:1fr;
  }

  .hero-panel{
    padding:14px;
  }
}

/* Modal styling */
.modal-backdrop{
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.55);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal{
  background: #fff;
  border-radius: 14px;
  padding: 20px;
  width: 100%;
  max-width: 520px;
  max-height: 85vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.25);
  z-index: 1001;
}

.modal::-webkit-scrollbar{
  width: 8px;
}

.modal::-webkit-scrollbar-track{
  background: #f1f5f9;
  border-radius: 4px;
}

.modal::-webkit-scrollbar-thumb{
  background: #cbd5e1;
  border-radius: 4px;
}

.modal::-webkit-scrollbar-thumb:hover{
  background: #000000;
}

.modal h3{
  margin: 0 0 12px;
  font-size: 1.5rem;
  font-weight: 700;
}

.modal .muted{
  color: #000000;
  margin: 0 0 12px;
  line-height: 1.6;
}

.modal .small-text{
  font-size: 0.85rem;
}

.op-actions{
  margin-top: 20px;
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.small-btn{
  padding: 8px 12px;
  font-size: 12px;
}
</style>

  
