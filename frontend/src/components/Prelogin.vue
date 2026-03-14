<template>
  <div class="prelog">
    <header>
      <div class="container nav">
        <a class="brand" href="#" @click.prevent="scrollToTop">
          <svg viewBox="0 0 64 64" aria-hidden="true">
            <defs>
              <linearGradient id="oh-brand-gradient" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0" stop-color="#1d4ed8" />
                <stop offset="1" stop-color="#0f9d8a" />
              </linearGradient>
            </defs>
            <circle cx="28" cy="28" r="18" fill="url(#oh-brand-gradient)" opacity="0.1" />
            <circle cx="28" cy="28" r="12" fill="none" stroke="url(#oh-brand-gradient)" stroke-width="3" />
            <path d="M36 36 L46 46" stroke="url(#oh-brand-gradient)" stroke-width="3.2" stroke-linecap="round" />
            <path d="M44 16 L44 20 M42 18 L46 18" stroke="url(#oh-brand-gradient)" stroke-width="2" stroke-linecap="round" />
            <circle cx="44" cy="18" r="1.5" fill="url(#oh-brand-gradient)" />
          </svg>
          Opportunity Hub
        </a>

        <nav class="navlinks desktop-nav" aria-label="Primary">
          <RouterLink to="/about">About Us</RouterLink>
          <RouterLink to="/references">References</RouterLink>
          <RouterLink class="btn btn-primary" to="/signup">Sign up</RouterLink>
          <RouterLink class="btn btn-outline" to="/login">Log in</RouterLink>
        </nav>

        <button
          class="hamburger"
          :class="{ active: isMenuOpen }"
          @click="toggleMenu"
          aria-label="Toggle menu"
          :aria-expanded="isMenuOpen ? 'true' : 'false'"
        >
          <span class="bar"></span>
          <span class="bar"></span>
          <span class="bar"></span>
        </button>
      </div>

      <nav class="mobile-nav" :class="{ active: isMenuOpen }" aria-label="Mobile">
        <RouterLink to="/about" @click="closeMenu">About Us</RouterLink>
        <RouterLink to="/references" @click="closeMenu">References</RouterLink>
        <div class="mobile-nav-buttons">
          <RouterLink class="btn btn-primary" to="/signup" @click="closeMenu">Sign up</RouterLink>
          <RouterLink class="btn btn-outline" to="/login" @click="closeMenu">Log in</RouterLink>
        </div>
      </nav>
    </header>

    <main class="container">
      <section class="hero">
        <div class="hero-copy">
          <span class="eyebrow">Student community resource hub</span>
          <h1>Find student opportunities without chasing ten different websites.</h1>
          <p class="hero-intro">
            Opportunity Hub helps students discover internships, volunteering, clubs,
            tutoring, leadership programs, and community events in one centralized platform.
          </p>
          <p class="hero-support">
            Built to make real opportunities easier to find, easier to trust, and easier
            to act on for students, schools, and local organizations.
          </p>

          <div class="hero-ctas">
            <RouterLink class="btn btn-primary" to="/signup">Get Started</RouterLink>
            <button class="btn btn-ghost" type="button" @click="scrollToSection('categories')">
              Browse Opportunities
            </button>
          </div>

          <div class="hero-meta">
            <div class="meta-chip">
              <span class="meta-dot"></span>
              Centralized opportunities
            </div>
            <div class="meta-chip">
              <span class="meta-dot"></span>
              Student-friendly dashboard
            </div>
            <div class="meta-chip">
              <span class="meta-dot"></span>
              Community-focused design
            </div>
          </div>
        </div>

        <div class="hero-visual">
          <div class="hero-dashboard">
            <div class="hero-dashboard-top">
              <div>
                <p class="panel-label">Preview</p>
                <h2>Opportunity dashboard</h2>
              </div>
              <span class="status-pill">Signed out view</span>
            </div>

            <div class="preview-search" role="search" aria-labelledby="demo-search-label">
              <label id="demo-search-label" class="sr-only" for="demo-search">
                Search the example opportunity feed
              </label>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path d="M21 21l-4.2-4.2" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
                <circle cx="11" cy="11" r="6.5" stroke="currentColor" stroke-width="1.8" />
              </svg>
              <input
                id="demo-search"
                v-model="query"
                type="text"
                placeholder="Search internships, tutoring, or volunteering"
                autocomplete="off"
              />
            </div>

            <div class="preview-summary">
              <div class="summary-card">
                <span class="summary-label">Saved</span>
                <strong>12</strong>
              </div>
              <div class="summary-card">
                <span class="summary-label">In progress</span>
                <strong>4</strong>
              </div>
              <div class="summary-card">
                <span class="summary-label">New this week</span>
                <strong>8</strong>
              </div>
            </div>

            <div class="filter-row">
              <button
                v-for="filter in previewFilters"
                :key="filter.key"
                class="filter-pill"
                :class="{ active: activeFilter === filter.key }"
                type="button"
                :aria-pressed="String(activeFilter === filter.key)"
                @click="setFilter(filter.key)"
              >
                {{ filter.label }}
              </button>
            </div>

            <div class="preview-cards" aria-live="polite">
              <article v-for="card in filteredCards" :key="card.id" class="preview-card">
                <div class="preview-card-top">
                  <span class="preview-tag">{{ card.organization }}</span>
                  <span class="preview-type">{{ card.label }}</span>
                </div>
                <h3>{{ card.title }}</h3>
                <p>{{ card.desc }}</p>
                <div class="preview-card-meta">
                  <span>{{ card.meta }}</span>
                  <span>{{ card.location }}</span>
                </div>
              </article>

              <article v-if="filteredCards.length === 0" class="preview-card preview-card-empty">
                <h3>No matching preview results</h3>
                <p>Try a different term or switch categories to see more example opportunities.</p>
              </article>
            </div>
          </div>

          <div class="floating-note note-top">
            <strong>Trusted sources</strong>
            <span>Schools, clubs, and community organizations can share opportunities in one place.</span>
          </div>

          <div class="floating-note note-bottom">
            <strong>Built for action</strong>
            <span>Save opportunities, track applications, and return to your dashboard later.</span>
          </div>
        </div>
      </section>

      <section class="impact-strip" aria-label="Platform highlights">
        <article v-for="stat in impactStats" :key="stat.label" class="impact-card">
          <span class="impact-label">{{ stat.label }}</span>
          <strong>{{ stat.value }}</strong>
          <p>{{ stat.description }}</p>
        </article>
      </section>

      <section id="purpose" class="section-shell two-up">
        <div class="section-copy">
          <span class="section-kicker">Why Opportunity Hub matters</span>
          <h2>Students lose opportunities when information is scattered and inconsistent.</h2>
          <p>
            Internships might live on a district page, volunteer events might be buried in a
            flyer, and tutoring or club updates often stay locked inside separate systems.
            That fragmentation makes students miss chances they would have used.
          </p>
        </div>

        <div class="problem-solution">
          <article class="split-card split-card-problem">
            <span class="split-label">The problem</span>
            <h3>Too many disconnected sources</h3>
            <p>
              Students are expected to monitor multiple websites, forms, and announcements just
              to stay informed.
            </p>
          </article>
          <article class="split-card split-card-solution">
            <span class="split-label">The solution</span>
            <h3>One centralized, trusted student hub</h3>
            <p>
              Opportunity Hub brings together community resources into a single system that is
              searchable, organized, and easier to use.
            </p>
          </article>
        </div>
      </section>

      <section id="categories" class="section-shell">
        <div class="section-heading">
          <div>
            <span class="section-kicker">Categories and resources</span>
            <h2>Main opportunity paths students can explore</h2>
            <p>
              The platform is organized around the kinds of opportunities students actually look
              for, with clear categories and simple browsing.
            </p>
          </div>
        </div>

        <div class="resource-grid">
          <article v-for="category in resourceCategories" :key="category.title" class="resource-card">
            <div class="resource-icon" :style="{ '--icon-color': category.color }">
              <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path
                  :d="category.icon"
                  stroke="currentColor"
                  stroke-width="1.8"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </div>
            <h3>{{ category.title }}</h3>
            <p>{{ category.desc }}</p>
          </article>
        </div>
      </section>

      <section id="workflow" class="section-shell">
        <div class="section-heading">
          <div>
            <span class="section-kicker">How it works</span>
            <h2>A clear student workflow from discovery to follow-through</h2>
            <p>
              The landing page should communicate that Opportunity Hub is a real platform, not
              just a static directory. The workflow is built around what students actually do.
            </p>
          </div>
        </div>

        <div class="workflow-grid">
          <article v-for="step in workflowSteps" :key="step.number" class="workflow-card">
            <div class="workflow-number">{{ step.number }}</div>
            <h3>{{ step.title }}</h3>
            <p>{{ step.desc }}</p>
          </article>
        </div>
      </section>

      <section class="section-shell feature-showcase">
        <div class="section-heading">
          <div>
            <span class="section-kicker">Features preview</span>
            <h2>Tools that make the hub feel useful, organized, and real</h2>
            <p>
              These previews highlight the system behind the platform: a student dashboard,
              saved opportunities, tracking, posting, and moderation support.
            </p>
          </div>
        </div>

        <div class="feature-layout">
          <div class="feature-dashboard">
            <div class="feature-dashboard-header">
              <div>
                <p class="panel-label">Student dashboard</p>
                <h3>One place to manage opportunities</h3>
              </div>
              <span class="status-pill status-pill-soft">Active workspace</span>
            </div>

            <div class="dashboard-panels">
              <div class="dashboard-panel dashboard-panel-primary">
                <span class="dashboard-label">Application tracker</span>
                <strong>Track deadlines and progress</strong>
                <p>See what is saved, submitted, and still in progress without losing details.</p>
              </div>
              <div class="dashboard-panel">
                <span class="dashboard-label">Saved opportunities</span>
                <strong>Keep important listings close</strong>
                <p>Bookmark internships, clubs, tutoring, and service options for later review.</p>
              </div>
              <div class="dashboard-panel">
                <span class="dashboard-label">Organization posts</span>
                <strong>Promote opportunities clearly</strong>
                <p>Schools and local groups can publish openings with better visibility for students.</p>
              </div>
              <div class="dashboard-panel">
                <span class="dashboard-label">Moderation and reporting</span>
                <strong>Support trust and quality</strong>
                <p>Reporting and moderation help keep listings accurate, helpful, and appropriate.</p>
              </div>
            </div>
          </div>

          <div class="feature-card-stack">
            <article v-for="feature in featureCards" :key="feature.title" class="feature-card">
              <span class="feature-pill">{{ feature.tag }}</span>
              <h3>{{ feature.title }}</h3>
              <p>{{ feature.desc }}</p>
            </article>
          </div>
        </div>
      </section>

      <section class="section-shell community-section">
        <div class="section-heading">
          <div>
            <span class="section-kicker">Community focused</span>
            <h2>Designed for the people who actually make student opportunities happen</h2>
            <p>
              Opportunity Hub is meant to improve visibility and access for students while also
              giving schools, clubs, and community organizations a clearer way to share resources.
            </p>
          </div>
        </div>

        <div class="community-grid">
          <article v-for="group in communityGroups" :key="group.title" class="community-card">
            <h3>{{ group.title }}</h3>
            <p>{{ group.desc }}</p>
          </article>
        </div>
      </section>

      <section class="cta-shell">
        <div class="cta-panel">
          <div>
            <span class="section-kicker">Start exploring</span>
            <h2>Give students one polished place to discover what is next.</h2>
            <p>
              Create an account to unlock the full opportunity hub, or browse the landing page to
              see how the platform organizes real community resources.
            </p>
          </div>
          <div class="cta-actions">
            <RouterLink class="btn btn-primary" to="/signup">Sign up free</RouterLink>
            <RouterLink class="btn btn-outline" to="/login">Log in</RouterLink>
          </div>
        </div>
      </section>
    </main>

    <footer>
      <div class="container">
        <div class="footer-inner">
          <p class="footer-copy">
            Copyright {{ year }} Opportunity Hub. Built by students, for students.
          </p>
          <div class="footer-links">
            <RouterLink class="footer-pill" to="/about">About Us</RouterLink>
            <RouterLink class="footer-pill" to="/references">References</RouterLink>
            <button class="footer-pill" type="button" @click="openPrivacy">Privacy</button>
            <button class="footer-pill" type="button" @click="openContact">Contact</button>
          </div>
        </div>
      </div>
    </footer>

    <div v-if="isPrivacyOpen" class="modal-backdrop" @click.self="isPrivacyOpen = false">
      <div class="modal">
        <h3>Privacy</h3>
        <p class="modal-copy">
          Opportunity Hub stores your account information and the posts you create. Applications
          you submit are visible to the creator of that post. Password protection is handled with
          hashing and salting techniques, and your data is not sold.
        </p>
        <div class="op-actions">
          <button class="btn btn-primary small-btn" type="button" @click="isPrivacyOpen = false">
            Done
          </button>
        </div>
      </div>
    </div>

    <div v-if="isContactOpen" class="modal-backdrop" @click.self="isContactOpen = false">
      <div class="modal">
        <h3>Contact</h3>
        <p class="modal-copy modal-copy-small">Please sign in to send us a message.</p>
        <div class="op-actions">
          <button class="btn btn-ghost small-btn" type="button" @click="isContactOpen = false">
            Close
          </button>
          <RouterLink class="btn btn-primary small-btn" to="/login" @click="isContactOpen = false">
            Sign In
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import AxiosInstance from '@/apiClient';

const query = ref('');
const activeFilter = ref('all');
const isMenuOpen = ref(false);

const previewFilters = [
  { key: 'all', label: 'All' },
  { key: 'internships', label: 'Internships' },
  { key: 'volunteering', label: 'Volunteering' },
  { key: 'clubs', label: 'Clubs' },
  { key: 'tutoring', label: 'Tutoring' },
  { key: 'leadership', label: 'Leadership' }
];

const cards = ref([
  {
    id: 1,
    category: 'internships',
    label: 'Internship',
    organization: 'City Innovation Lab',
    title: 'Summer design and tech internship',
    desc: 'A student-friendly internship focused on digital projects, collaboration, and portfolio growth.',
    meta: 'Application closes April 12',
    location: 'Hybrid'
  },
  {
    id: 2,
    category: 'volunteering',
    label: 'Volunteer',
    organization: 'Community Food Network',
    title: 'Weekend service hours program',
    desc: 'Join local food distribution events and earn verified volunteer hours through supervised shifts.',
    meta: 'Flexible scheduling',
    location: 'On site'
  },
  {
    id: 3,
    category: 'clubs',
    label: 'Club',
    organization: 'Student Leadership Council',
    title: 'Campus leadership and service club',
    desc: 'Plan school initiatives, coordinate events, and build leadership experience with peers.',
    meta: 'Meets every Tuesday',
    location: 'School based'
  },
  {
    id: 4,
    category: 'tutoring',
    label: 'Tutoring',
    organization: 'Academic Support Center',
    title: 'Peer tutoring for math and science',
    desc: 'Students can request help or sign up to tutor classmates in core subjects after school.',
    meta: 'Open weekly',
    location: 'In person'
  },
  {
    id: 5,
    category: 'leadership',
    label: 'Leadership',
    organization: 'Youth Advisory Board',
    title: 'Youth advisory board applications',
    desc: 'Contribute ideas, represent student voices, and work with community partners on local initiatives.',
    meta: 'Interview required',
    location: 'District wide'
  }
]);

const resourceCategories = [
  {
    title: 'Internships',
    desc: 'Career-building experiences that help students explore real industries and build stronger resumes.',
    color: '#1d4ed8',
    icon: 'M4.5 8.5h15v9.75A1.75 1.75 0 0 1 17.75 20H6.25A1.75 1.75 0 0 1 4.5 18.25V8.5Zm4-3h7A1.5 1.5 0 0 1 17 7v1.5H7V7a1.5 1.5 0 0 1 1.5-1.5ZM4.5 12h15M10 12v2m4-2v2'
  },
  {
    title: 'Volunteering',
    desc: 'Community service opportunities that support local organizations while helping students earn verified hours.',
    color: '#0f9d8a',
    icon: 'M12 20s-6.5-4.35-8.2-7.3A4.9 4.9 0 0 1 12 5.1a4.9 4.9 0 0 1 8.2 7.6C18.5 15.65 12 20 12 20Z'
  },
  {
    title: 'Clubs',
    desc: 'School and community groups that help students connect around shared interests and ongoing activities.',
    color: '#7c3aed',
    icon: 'M12 4.5 14 8.5l4.5.75-3.25 3.1.8 4.65L12 14.8 7.95 17l.8-4.65L5.5 9.25 10 8.5 12 4.5Z'
  },
  {
    title: 'Tutoring',
    desc: 'Academic support resources for students who need help or want to mentor others in core subjects.',
    color: '#ea580c',
    icon: 'M5 6.75A2.75 2.75 0 0 1 7.75 4h8.5A2.75 2.75 0 0 1 19 6.75v10.5A1.75 1.75 0 0 1 17.25 19H8.1a2.6 2.6 0 0 0-2.6 2.6V6.75Zm0 0A2.75 2.75 0 0 0 2.25 9.5v9.75A1.75 1.75 0 0 0 4 21h13'
  },
  {
    title: 'Community events',
    desc: 'Programs, workshops, and events that connect students with local initiatives and seasonal opportunities.',
    color: '#0284c7',
    icon: 'M7 3.75v2.5M17 3.75v2.5M4 8.25h16M6.25 5.25h11.5A1.75 1.75 0 0 1 19.5 7v11A1.75 1.75 0 0 1 17.75 19.75H6.25A1.75 1.75 0 0 1 4.5 18V7a1.75 1.75 0 0 1 1.75-1.75Z'
  },
  {
    title: 'Leadership',
    desc: 'Opportunities that help students build confidence, guide projects, and contribute to their communities.',
    color: '#b45309',
    icon: 'M12 3.75 18.25 6.5v5.15c0 3.45-2.2 6.6-6.25 8.6-4.05-2-6.25-5.15-6.25-8.6V6.5L12 3.75Zm0 4.25v7.5m-3-4 3-3 3 3'
  }
];

const workflowSteps = [
  {
    number: '01',
    title: 'Discover opportunities',
    desc: 'Browse a centralized feed of internships, service, clubs, tutoring, and events.'
  },
  {
    number: '02',
    title: 'Save or apply',
    desc: 'Bookmark opportunities, compare options, and move forward when you are ready.'
  },
  {
    number: '03',
    title: 'Track your progress',
    desc: 'Use the dashboard to keep track of deadlines, saved items, and application activity.'
  },
  {
    number: '04',
    title: 'Connect with organizations',
    desc: 'Return to trusted postings from schools, clubs, and community partners in one place.'
  }
];

const featureCards = [
  {
    tag: 'Dashboard',
    title: 'A clearer student home base',
    desc: 'Students do not need to restart their search every time they log in.'
  },
  {
    tag: 'Discovery',
    title: 'Organized browsing experience',
    desc: 'Cards, categories, and filters keep the platform easy to scan on desktop and mobile.'
  },
  {
    tag: 'Trust',
    title: 'Moderated community content',
    desc: 'Posting and reporting tools support a safer, more useful community resource hub.'
  }
];

const communityGroups = [
  {
    title: 'Students',
    desc: 'Find meaningful opportunities faster and keep important information in one dashboard.'
  },
  {
    title: 'Schools and clubs',
    desc: 'Improve visibility for programs, teams, tutoring, and events that students should actually see.'
  },
  {
    title: 'Community organizations',
    desc: 'Reach student audiences more clearly through a platform built around accessibility and discovery.'
  }
];

const opportunityCount = ref(null);

const impactStats = computed(() => [
  {
    label: 'Opportunities centralized',
    value: opportunityCount.value != null ? `${opportunityCount.value}+` : 'Growing',
    description: 'A shared hub for student opportunities instead of scattered posts and links.'
  },
  {
    label: 'Core categories',
    value: '6',
    description: 'Internships, volunteering, clubs, tutoring, events, and leadership pathways.'
  },
  {
    label: 'Workflow stages',
    value: '4',
    description: 'A clear flow from discovery to tracking and community connection.'
  },
  {
    label: 'Groups served',
    value: '3',
    description: 'Students, schools, and community organizations all benefit from one platform.'
  }
]);

const filteredCards = computed(() => {
  const q = query.value.trim().toLowerCase();

  return cards.value.filter((card) => {
    const matchesFilter = activeFilter.value === 'all' || card.category === activeFilter.value;
    const matchesQuery =
      !q ||
      card.title.toLowerCase().includes(q) ||
      card.desc.toLowerCase().includes(q) ||
      card.organization.toLowerCase().includes(q) ||
      card.label.toLowerCase().includes(q);

    return matchesFilter && matchesQuery;
  });
});

function toggleMenu() {
  isMenuOpen.value = !isMenuOpen.value;
}

function closeMenu() {
  isMenuOpen.value = false;
}

function setFilter(key) {
  activeFilter.value = key;
}

function scrollToSection(sectionId) {
  const element = document.getElementById(sectionId);

  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    window.history.replaceState(null, '', `#${sectionId}`);
  }

  closeMenu();
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
  window.history.replaceState(null, '', window.location.pathname);
  closeMenu();
}

const year = new Date().getFullYear();

onMounted(async () => {
  try {
    const response = await AxiosInstance.get('/opportunities/count');
    const count = response.data?.count;
    opportunityCount.value = typeof count === 'number' ? count : null;
  } catch {
    opportunityCount.value = null;
  }
});

const isPrivacyOpen = ref(false);
const isContactOpen = ref(false);

function openPrivacy() {
  isPrivacyOpen.value = true;
  closeMenu();
}

function openContact() {
  isContactOpen.value = true;
  closeMenu();
}
</script>

<style scoped>
:global(:root) {
  --prelog-bg: #f4f7fb;
  --prelog-text: #0f172a;
  --prelog-muted: #475569;
  --prelog-blue: #1d4ed8;
  --prelog-teal: #0f9d8a;
  --prelog-gold: #c58c29;
  --prelog-shadow: 0 20px 50px rgba(15, 23, 42, 0.08);
  --prelog-shadow-soft: 0 14px 30px rgba(15, 23, 42, 0.06);
  --prelog-radius-lg: 28px;
  --prelog-radius-md: 20px;
}

.sr-only {
  position: absolute !important;
  width: 1px !important;
  height: 1px !important;
  padding: 0 !important;
  margin: -1px !important;
  overflow: hidden !important;
  clip: rect(0, 0, 0, 0) !important;
  white-space: nowrap !important;
  border: 0 !important;
}

* {
  box-sizing: border-box;
}

.prelog {
  min-height: 100vh;
  color: var(--prelog-text);
  font-family: "Segoe UI", "Trebuchet MS", sans-serif;
  background:
    radial-gradient(circle at top left, rgba(29, 78, 216, 0.13), transparent 34%),
    radial-gradient(circle at 85% 18%, rgba(15, 157, 138, 0.1), transparent 28%),
    linear-gradient(180deg, #f9fbfe 0%, var(--prelog-bg) 55%, #eef4f9 100%);
}

a {
  color: inherit;
  text-decoration: none;
}

button,
input {
  font: inherit;
}

.container {
  width: min(1220px, calc(100% - 40px));
  margin: 0 auto;
}

header {
  position: sticky;
  top: 0;
  z-index: 30;
  background: rgba(248, 251, 255, 0.85);
  border-bottom: 1px solid rgba(148, 163, 184, 0.2);
  backdrop-filter: blur(16px);
}

.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  padding: 18px 0;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  font-size: 1.05rem;
  font-weight: 700;
  letter-spacing: 0.01em;
}

.brand svg {
  width: 34px;
  height: 34px;
  flex: 0 0 auto;
}

.navlinks {
  display: flex;
  align-items: center;
  gap: 14px;
}

.navlinks a:not(.btn) {
  color: var(--prelog-muted);
  font-size: 0.95rem;
  transition: color 0.2s ease;
}

.navlinks a:not(.btn):hover,
.mobile-nav a:hover {
  color: var(--prelog-text);
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 44px;
  padding: 0 18px;
  border: 1px solid rgba(148, 163, 184, 0.35);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.78);
  color: var(--prelog-text);
  box-shadow: 0 1px 0 rgba(255, 255, 255, 0.55) inset;
  cursor: pointer;
  transition:
    transform 0.18s ease,
    box-shadow 0.18s ease,
    border-color 0.18s ease,
    background 0.18s ease;
}

.btn:hover {
  transform: translateY(-1px);
  box-shadow: var(--prelog-shadow-soft);
  border-color: rgba(15, 23, 42, 0.14);
}

.btn:focus-visible,
.filter-pill:focus-visible,
.footer-pill:focus-visible,
.hamburger:focus-visible {
  outline: 3px solid rgba(29, 78, 216, 0.22);
  outline-offset: 2px;
}

.btn-primary {
  border: none;
  color: #ffffff;
  font-weight: 700;
  background: linear-gradient(135deg, var(--prelog-blue), var(--prelog-teal));
}

.btn-primary:hover {
  box-shadow: 0 18px 32px rgba(29, 78, 216, 0.24);
}

.btn-outline {
  background: rgba(255, 255, 255, 0.92);
}

.btn-ghost {
  background: rgba(255, 255, 255, 0.52);
}

.hamburger {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  width: 44px;
  height: 44px;
  padding: 0;
  border: 1px solid rgba(148, 163, 184, 0.35);
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.75);
  cursor: pointer;
}

.bar {
  width: 20px;
  height: 2px;
  margin: 0 auto;
  border-radius: 999px;
  background: var(--prelog-text);
  transition: transform 0.28s ease, opacity 0.28s ease;
}

.hamburger.active .bar:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
}

.hamburger.active .bar:nth-child(2) {
  opacity: 0;
}

.hamburger.active .bar:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
}

.mobile-nav {
  display: none;
  flex-direction: column;
  gap: 0;
  padding: 0 20px;
  max-height: 0;
  overflow: hidden;
  background: rgba(248, 251, 255, 0.96);
  border-top: 1px solid rgba(148, 163, 184, 0.16);
  transition: max-height 0.3s ease, padding 0.3s ease;
}

.mobile-nav.active {
  max-height: 320px;
  padding: 12px 20px 18px;
}

.mobile-nav a {
  padding: 12px 0;
  color: var(--prelog-muted);
  border-bottom: 1px solid rgba(148, 163, 184, 0.12);
}

.mobile-nav-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding-top: 14px;
}

.mobile-nav-buttons .btn {
  width: 100%;
}

main.container {
  padding: 34px 0 48px;
}

.hero {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1.05fr);
  gap: 34px;
  align-items: center;
  padding: 18px 0 22px;
}

.eyebrow,
.section-kicker,
.panel-label,
.split-label,
.impact-label,
.dashboard-label {
  display: inline-block;
  font-size: 0.76rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.eyebrow,
.section-kicker,
.panel-label,
.impact-label,
.dashboard-label {
  color: var(--prelog-blue);
}

.hero-copy h1 {
  margin: 12px 0 18px;
  font-size: clamp(2.7rem, 5vw, 4.45rem);
  line-height: 0.98;
  max-width: 11.5ch;
}

.hero-intro,
.hero-support,
.section-heading p,
.section-copy p,
.split-card p,
.workflow-card p,
.resource-card p,
.feature-card p,
.community-card p,
.cta-panel p,
.impact-card p,
.preview-card p,
.dashboard-panel p {
  margin: 0;
  color: var(--prelog-muted);
  line-height: 1.7;
}

.hero-intro {
  max-width: 56ch;
  font-size: 1.08rem;
}

.hero-support {
  max-width: 56ch;
  margin-top: 12px;
}

.hero-ctas {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 24px;
}

.hero-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 22px;
}

.meta-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border: 1px solid rgba(148, 163, 184, 0.22);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.72);
  color: var(--prelog-muted);
  box-shadow: 0 12px 24px rgba(15, 23, 42, 0.04);
}

.meta-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--prelog-blue), var(--prelog-teal));
}

.hero-visual {
  position: relative;
  padding: 20px 0;
}

.hero-dashboard,
.section-shell,
.cta-panel {
  position: relative;
  overflow: hidden;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(248, 251, 255, 0.9));
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: var(--prelog-radius-lg);
  box-shadow: var(--prelog-shadow);
}

.hero-dashboard::before,
.section-shell::before,
.cta-panel::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at top right, rgba(29, 78, 216, 0.09), transparent 24%),
    radial-gradient(circle at bottom left, rgba(15, 157, 138, 0.08), transparent 28%);
  pointer-events: none;
}

.hero-dashboard {
  padding: 24px;
}

.hero-dashboard-top,
.feature-dashboard-header,
.section-heading,
.footer-inner {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 18px;
}

.hero-dashboard-top h2,
.section-heading h2,
.section-copy h2,
.cta-panel h2 {
  margin: 6px 0 0;
}

.hero-dashboard-top h2 {
  font-size: 1.55rem;
}

.status-pill,
.feature-pill,
.preview-tag,
.preview-type,
.footer-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  font-size: 0.78rem;
}

.status-pill {
  padding: 8px 12px;
  background: rgba(15, 23, 42, 0.04);
  color: var(--prelog-muted);
}

.status-pill-soft {
  background: rgba(29, 78, 216, 0.1);
  color: var(--prelog-blue);
}

.preview-search {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 20px;
  padding: 14px 16px;
  border: 1px solid rgba(148, 163, 184, 0.22);
  border-radius: 16px;
  background: rgba(247, 250, 252, 0.88);
  color: var(--prelog-muted);
}

.preview-search input {
  flex: 1 1 auto;
  border: none;
  outline: none;
  background: transparent;
  color: var(--prelog-text);
}

.preview-search input::placeholder {
  color: #94a3b8;
}

.preview-summary {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-top: 16px;
}

.summary-card {
  padding: 14px;
  border-radius: 18px;
  background: linear-gradient(180deg, #ffffff, #f5f8fd);
  border: 1px solid rgba(148, 163, 184, 0.16);
}

.summary-card strong {
  display: block;
  margin-top: 6px;
  font-size: 1.45rem;
}

.summary-label {
  color: var(--prelog-muted);
  font-size: 0.86rem;
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 18px;
}

.filter-pill {
  padding: 9px 14px;
  border: 1px solid rgba(148, 163, 184, 0.24);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.88);
  color: var(--prelog-muted);
  cursor: pointer;
  transition: background 0.18s ease, border-color 0.18s ease, color 0.18s ease, transform 0.18s ease;
}

.filter-pill:hover,
.filter-pill.active {
  transform: translateY(-1px);
}

.filter-pill.active {
  border-color: transparent;
  background: linear-gradient(135deg, var(--prelog-blue), var(--prelog-teal));
  color: #ffffff;
}

.preview-cards {
  display: grid;
  gap: 12px;
  margin-top: 18px;
}

.preview-card {
  padding: 16px;
  border-radius: 18px;
  background: linear-gradient(180deg, #ffffff, #f7fafc);
  border: 1px solid rgba(148, 163, 184, 0.16);
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}

.preview-card:hover,
.resource-card:hover,
.workflow-card:hover,
.feature-card:hover,
.community-card:hover,
.impact-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--prelog-shadow-soft);
  border-color: rgba(29, 78, 216, 0.16);
}

.preview-card-top,
.preview-card-meta,
.footer-links {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  flex-wrap: wrap;
}

.preview-tag,
.preview-type {
  padding: 6px 10px;
}

.preview-tag {
  background: rgba(29, 78, 216, 0.08);
  color: var(--prelog-blue);
}

.preview-type {
  background: rgba(15, 23, 42, 0.05);
  color: var(--prelog-muted);
}

.preview-card h3,
.resource-card h3,
.workflow-card h3,
.feature-card h3,
.community-card h3,
.split-card h3,
.dashboard-panel strong,
.cta-panel h2 {
  margin: 10px 0 8px;
}

.preview-card-meta {
  margin-top: 14px;
  color: var(--prelog-muted);
  font-size: 0.88rem;
}

.preview-card-empty p {
  margin-top: 8px;
}

.floating-note {
  position: absolute;
  max-width: 220px;
  padding: 14px 16px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.94);
  border: 1px solid rgba(148, 163, 184, 0.16);
  box-shadow: var(--prelog-shadow-soft);
}

.floating-note strong {
  display: block;
  margin-bottom: 6px;
  font-size: 0.95rem;
}

.floating-note span {
  color: var(--prelog-muted);
  line-height: 1.55;
  font-size: 0.9rem;
}

.note-top {
  top: -6px;
  right: -8px;
}

.note-bottom {
  bottom: -4px;
  left: -10px;
}

.impact-strip {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
  margin: 8px 0 30px;
}

.impact-card,
.resource-card,
.workflow-card,
.feature-card,
.community-card,
.split-card,
.dashboard-panel {
  position: relative;
  padding: 22px;
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(148, 163, 184, 0.16);
  border-radius: var(--prelog-radius-md);
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}

.impact-card strong {
  display: block;
  margin-top: 8px;
  font-size: 2rem;
  line-height: 1;
}

.impact-card p {
  margin-top: 12px;
}

.section-shell {
  padding: 30px;
  margin: 0 0 26px;
}

.two-up {
  display: grid;
  grid-template-columns: minmax(0, 0.95fr) minmax(0, 1.05fr);
  gap: 24px;
  align-items: start;
}

.section-copy h2,
.section-heading h2,
.cta-panel h2 {
  font-size: clamp(1.85rem, 2.8vw, 2.7rem);
  line-height: 1.08;
}

.section-copy p {
  margin-top: 16px;
  max-width: 60ch;
}

.problem-solution {
  display: grid;
  gap: 16px;
}

.split-card-problem {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.95), rgba(254, 242, 242, 0.95));
}

.split-card-solution {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.95), rgba(240, 253, 250, 0.98));
}

.split-label {
  color: var(--prelog-gold);
}

.resource-grid,
.workflow-grid,
.community-grid {
  display: grid;
  gap: 16px;
}

.resource-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
  margin-top: 22px;
}

.resource-card {
  min-height: 210px;
}

.resource-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 52px;
  height: 52px;
  border-radius: 16px;
  background: rgba(29, 78, 216, 0.1);
  color: var(--icon-color);
}

.resource-icon svg {
  width: 24px;
  height: 24px;
}

.workflow-grid {
  grid-template-columns: repeat(4, minmax(0, 1fr));
  margin-top: 22px;
}

.workflow-card {
  min-height: 210px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(244, 248, 253, 0.96));
}

.workflow-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 58px;
  height: 34px;
  padding: 0 12px;
  border-radius: 999px;
  background: rgba(29, 78, 216, 0.1);
  color: var(--prelog-blue);
  font-weight: 700;
  letter-spacing: 0.08em;
}

.feature-showcase {
  padding-bottom: 32px;
}

.feature-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(0, 0.85fr);
  gap: 18px;
  margin-top: 22px;
}

.feature-dashboard {
  position: relative;
  padding: 24px;
  border-radius: 24px;
  background: linear-gradient(180deg, rgba(245, 249, 255, 0.98), rgba(255, 255, 255, 0.96));
  border: 1px solid rgba(148, 163, 184, 0.16);
}

.feature-dashboard-header h3 {
  margin: 6px 0 0;
  font-size: 1.45rem;
}

.dashboard-panels {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
  margin-top: 20px;
}

.dashboard-panel {
  min-height: 170px;
  background: rgba(255, 255, 255, 0.9);
}

.dashboard-panel-primary {
  background: linear-gradient(145deg, rgba(29, 78, 216, 0.95), rgba(15, 157, 138, 0.94));
  color: #ffffff;
}

.dashboard-panel-primary .dashboard-label,
.dashboard-panel-primary p {
  color: rgba(255, 255, 255, 0.88);
}

.feature-card-stack {
  display: grid;
  gap: 14px;
}

.feature-card {
  min-height: 158px;
}

.feature-pill {
  padding: 7px 10px;
  background: rgba(15, 23, 42, 0.05);
  color: var(--prelog-muted);
}

.community-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
  margin-top: 22px;
}

.community-card {
  min-height: 180px;
}

.cta-shell {
  margin-top: 8px;
}

.cta-panel {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 30px;
}

.cta-panel p {
  margin-top: 14px;
  max-width: 58ch;
}

.cta-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

footer {
  border-top: 1px solid rgba(148, 163, 184, 0.18);
  background: rgba(248, 251, 255, 0.82);
}

.footer-inner {
  padding: 18px 0 24px;
}

.footer-copy {
  margin: 0;
  color: var(--prelog-muted);
}

.footer-links {
  justify-content: flex-end;
}

.footer-pill {
  padding: 9px 12px;
  border: 1px solid rgba(148, 163, 184, 0.2);
  background: rgba(255, 255, 255, 0.7);
  color: var(--prelog-muted);
  cursor: pointer;
}

.modal-backdrop {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: rgba(15, 23, 42, 0.46);
  backdrop-filter: blur(8px);
  z-index: 1000;
}

.modal {
  width: min(540px, 100%);
  max-height: 84vh;
  overflow-y: auto;
  padding: 24px;
  border-radius: 22px;
  background: #ffffff;
  box-shadow: 0 24px 50px rgba(15, 23, 42, 0.24);
}

.modal h3 {
  margin: 0 0 12px;
  font-size: 1.5rem;
}

.modal-copy {
  margin: 0;
  color: var(--prelog-muted);
  line-height: 1.7;
}

.modal-copy-small {
  font-size: 0.92rem;
}

.op-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.small-btn {
  min-height: 40px;
  padding: 0 14px;
}

@media (max-width: 1100px) {
  .hero,
  .feature-layout,
  .two-up {
    grid-template-columns: 1fr;
  }

  .hero {
    gap: 24px;
  }

  .hero-copy h1 {
    max-width: 12.5ch;
  }

  .note-top,
  .note-bottom {
    position: static;
    max-width: none;
    margin-top: 14px;
  }

  .workflow-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .impact-strip {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .resource-grid,
  .community-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .cta-panel {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (max-width: 780px) {
  .desktop-nav {
    display: none;
  }

  .hamburger,
  .mobile-nav {
    display: flex;
  }

  main.container {
    padding-top: 24px;
  }

  .hero-copy h1 {
    max-width: none;
    font-size: clamp(2.4rem, 12vw, 3.4rem);
  }

  .hero-dashboard,
  .section-shell,
  .cta-panel,
  .feature-dashboard {
    padding: 22px;
  }

  .preview-summary,
  .dashboard-panels,
  .community-grid,
  .resource-grid,
  .workflow-grid,
  .impact-strip {
    grid-template-columns: 1fr;
  }

  .feature-dashboard-header,
  .hero-dashboard-top,
  .section-heading,
  .footer-inner,
  .cta-panel {
    flex-direction: column;
  }

  .footer-links {
    justify-content: flex-start;
  }
}

@media (max-width: 560px) {
  .container {
    width: min(100% - 28px, 1220px);
  }

  .nav {
    padding: 14px 0;
  }

  .brand {
    font-size: 0.98rem;
  }

  .hero-meta,
  .hero-ctas,
  .cta-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .btn {
    width: 100%;
  }

  .hero-dashboard,
  .section-shell,
  .cta-panel,
  .feature-dashboard,
  .impact-card,
  .resource-card,
  .workflow-card,
  .feature-card,
  .community-card,
  .split-card,
  .dashboard-panel {
    padding: 18px;
  }
}
</style>
