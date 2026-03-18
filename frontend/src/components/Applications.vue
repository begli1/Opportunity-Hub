<template>
  <div class="Applications">
    <header>
      <div class="container nav">
        <router-link to="/dashboard">
          <a class="brand">
            <svg viewBox="0 0 64 64" aria-hidden="true">
              <defs>
                <linearGradient id="oh-search-g" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0" stop-color="#2563eb" />
                  <stop offset="1" stop-color="#14b8a6" />
                </linearGradient>
              </defs>
              <circle cx="28" cy="28" r="18" fill="url(#oh-search-g)" opacity="0.08" />
              <circle cx="28" cy="28" r="12" fill="none" stroke="url(#oh-search-g)" stroke-width="3" />
              <path d="M36 36 L46 46" stroke="url(#oh-search-g)" stroke-width="3.2" stroke-linecap="round" />
              <path
                d="M44 16 L44 20 M42 18 L46 18"
                stroke="url(#oh-search-g)"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
              <circle cx="44" cy="18" r="1.5" fill="url(#oh-search-g)" />
            </svg>
            Opportunity Hub
          </a>
        </router-link>

        <div class="nav-search">
          <input
            type="search"
            placeholder="Search your applications…"
            v-model="searchQuery"
          />
        </div>

        <nav class="navlinks desktop-nav">
          <router-link to="/dashboard">Dashboard</router-link>
          <router-link to="/my-posts">My posts</router-link>
          <router-link to="/applications">Applications</router-link>

          <!-- Profile dropdown -->
          <div class="profile-dropdown-wrapper">
            <button class="avatar-btn" @click="toggleProfileDropdown">
              <span class="avatar-circle">{{ userInitials }}</span>
            </button>
            <div v-if="isProfileOpen" class="profile-dropdown">
              <div class="profile-header">
                <span class="profile-avatar">{{ userInitials }}</span>
                <div class="profile-info">
                  <p class="profile-name">{{ userName }}</p>
                  <p class="profile-email">{{ userEmail }}</p>
                </div>
              </div>
              <div class="profile-divider"></div>
              <router-link to="/dashboard" class="profile-link" @click="closeProfileDropdown">
                <span class="profile-link-icon">🏠</span> Dashboard
              </router-link>
              <router-link to="/my-posts" class="profile-link" @click="closeProfileDropdown">
                <span class="profile-link-icon">📝</span> My Posts
              </router-link>
              <router-link to="/applications" class="profile-link" @click="closeProfileDropdown">
                <span class="profile-link-icon">📋</span> Applications
              </router-link>
              <div class="profile-divider"></div>
              <button class="profile-link profile-logout" @click="onLogout">
                <span class="profile-link-icon">🚪</span> Logout
              </button>
            </div>
          </div>
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
        <div class="mobile-profile-header">
          <span class="avatar-circle">{{ userInitials }}</span>
          <div class="mobile-profile-info">
            <p class="mobile-profile-name">{{ userName }}</p>
            <p class="mobile-profile-email">{{ userEmail }}</p>
          </div>
        </div>
        <div class="mobile-nav-divider"></div>
        
        <router-link to="/dashboard" @click="closeMenu">Dashboard</router-link>
        <router-link to="/my-posts" @click="closeMenu">My posts</router-link>
        <router-link to="/applications" @click="closeMenu">Applications</router-link>

        <div class="mobile-nav-divider"></div>
        <button class="btn-danger btn-danger-solid btn-post w-full" @click="onLogout">
          Logout
        </button>
      </nav>
    </header>

    <div v-if="pageError" class="error-popup">{{ pageError }}</div>

    <div class="section-header">
      <h2>My Applications</h2>
      <span class="muted small-text">Track decisions on community resources you applied to.</span>


      <div v-if="loading" class="muted small-text" style="padding: 0 20px;">
        Loading…
      </div>
      
      <div v-else-if="items.length === 0" class="muted small-text" style="padding: 0 20px;">
        You haven’t applied to anything yet.
      </div>

    </div>



    <div class="card-grid">
      <article v-for="row in filtered" :key="row.application.id" class="op-card">
        <div class="op-card-header">
          <span class="badge">{{ prettyType(row.opportunity.type) }}</span>
          <span class="status-pill" :data-status="row.application.status">
            {{ prettyStatus(row.application.status) }}
          </span>
        </div>

        <h3 class="op-title">{{ row.opportunity.title }}</h3>
        <p class="op-org">{{ row.opportunity.org }}</p>

        <div class="op-meta">
          <span>Applied: {{ formatDate(row.application.created_at) }}</span>
          <span>•</span>
          <span>Deadline: {{ formatDeadline(row.opportunity) }}</span>
        </div>

        <p
          v-if="row.application.status === 'rejected' && row.application.decision_reason"
          class="muted small-text"
        >
          Reason: {{ row.application.decision_reason }}
        </p>

        <!-- If you don't have a public opportunity page yet, remove this block -->
        <div class="op-actions" v-if="hasOpportunityRoute">
          <router-link class="btn btn-outline small-btn" :to="`/opportunities/${row.opportunity.id}`">
            View post
          </router-link>
        </div>
      </article>
    </div>

    <footer>
      <div class="container">
        <div class="footer-inner">
          <p class="muted">
            © <span>{{ year }}</span> Opportunity Hub. Built by students, for students.
          </p>
          <div class="footer-links">
            <router-link to="/about">About Us</router-link>
            <router-link to="/references">References</router-link>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import AxiosInstance from '@/apiClient'
import router from '@/router'
import { useAuth } from '@/lib/authStore'

const { clearToken, user, userInitials } = useAuth()
const year = new Date().getFullYear()

// User info from authStore
const userName = computed(() => user.value?.username || '...')
const userEmail = computed(() => user.value?.email || '')

// Nav toggle
const isMenuOpen = ref(false)
function toggleMenu() { isMenuOpen.value = !isMenuOpen.value }
function closeMenu() { isMenuOpen.value = false }

// Profile dropdown
const isProfileOpen = ref(false)
function toggleProfileDropdown() { isProfileOpen.value = !isProfileOpen.value }
function closeProfileDropdown() { isProfileOpen.value = false }
function handleClickOutside(e) {
  if (isProfileOpen.value && !e.target.closest('.profile-dropdown-wrapper')) {
    isProfileOpen.value = false
  }
}

function onLogout() {
  clearToken()
  router.push('/')
}

const pageError = ref('')
const loading = ref(false)
const items = ref([])

const searchQuery = ref('')

// Set this true only if you actually created a route like /opportunities/:id
const hasOpportunityRoute = false

function prettyType(t) {
  const s = String(t || '')
  return s ? s.charAt(0).toUpperCase() + s.slice(1) : ''
}

function prettyStatus(s) {
  const t = String(s || 'pending')
  return t.charAt(0).toUpperCase() + t.slice(1)
}

function formatDate(value) {
  if (!value) return '—'
  // Ensure UTC timezone is recognized - append Z if no timezone info
  let dateStr = String(value)
  if (!dateStr.includes('Z') && !dateStr.includes('+') && !dateStr.includes('-', 10)) {
    dateStr += 'Z'
  }
  return new Date(dateStr).toLocaleString()
}

function formatDeadline(op) {
  if (op?.deadline_text) return op.deadline_text
  if (op?.deadline_at) return new Date(op.deadline_at).toLocaleDateString()
  return '—'
}

async function loadMyApplications() {
  pageError.value = ''
  loading.value = true
  try {
    const res = await AxiosInstance.get('/users/me/applications')
    items.value = res.data || []
  } catch (e) {
    pageError.value =
      e?.response?.data?.detail?.message ||
      e?.response?.data?.detail ||
      e?.message ||
      'Could not load your applications'
  } finally {
    loading.value = false
  }
}

const filtered = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return items.value
  return items.value.filter((row) => {
    const title = String(row.opportunity?.title || '').toLowerCase()
    const org = String(row.opportunity?.org || '').toLowerCase()
    const status = String(row.application?.status || '').toLowerCase()
    return title.includes(q) || org.includes(q) || status.includes(q)
  })
})

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  loadMyApplications()
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

  
  <style scoped>
  /* Copy-paste of your MyPosts CSS, but renamed class + removed stuff you don’t need */
  
  :global(:root){
    --bg:#f3f4ff;
    --panel:#ffffff;
    --muted:#000000;
    --text:#0f172a;
    --accent:#2563eb;
    --accent-2:#14b8a6;
    --ring:rgba(37,99,235,.25);
    --card:#ffffff;
    --card-2:#f9fafb;
    --radius:18px;
    --shadow:0 18px 40px rgba(15,23,42,.08);
    --border:1px solid rgba(15,23,42,.06);
  }
  
  *{ box-sizing:border-box; }
  
  .Applications{
    min-height:100vh;
    background:
      radial-gradient(900px 500px at 10% -10%, rgba(59,130,246,.20), transparent 60%),
      radial-gradient(900px 600px at 90% 110%, rgba(45,212,191,.18), transparent 60%),
      var(--bg);
    color:var(--text);
    font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, "Helvetica Neue", Arial;
  }
  
  a{ color:inherit; text-decoration:none; }
  
  .container{
    max-width:1200px;
    margin:0 auto;
    padding:24px 24px 32px;
  }
  
  header{
    position:sticky;
    top:0;
    z-index:100;
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
  
  .nav-search{
    flex:1;
    max-width:360px;
    margin:0 12px;
  }
  
  .nav-search input{
    width:100%;
    padding:8px 12px;
    border-radius:999px;
    border:1px solid rgba(148,163,184,.7);
    font-size:13px;
    outline:none;
  }
  
  .nav-search input:focus{
    box-shadow:0 0 0 2px var(--ring);
    border-color:var(--accent);
  }
  
  .btn{
    display:inline-flex;
    align-items:center;
    justify-content:center;
    gap:8px;
    padding:10px 16px;
    border-radius:999px;
    border:1px solid rgba(148,163,184,.4);
    background:#ffffff;
    color:var(--text);
    font-size:14px;
    cursor:pointer;
    transition:transform .12s ease, box-shadow .12s ease;
  }
  
  .btn:hover{
    transform:translateY(-1px);
    box-shadow:0 10px 24px rgba(15,23,42,.12);
  }
  
  .btn-outline{
    background:#ffffff;
  }
  
  .btn-danger{
    display:inline-flex;
    align-items:center;
    justify-content:center;
    gap:8px;
    padding:10px 16px;
    border-radius:999px;
    border:1px solid rgba(239,68,68,.25);
    background:linear-gradient(180deg, #fffafa, #fee2e2);
    color:#b91c1c;
    font-size:14px;
    font-weight:600;
    cursor:pointer;
    transition:all .18s ease;
  }
  
  .btn-danger:hover{
    background:linear-gradient(180deg, #fee2e2, #fecaca);
    border-color:#ef4444;
    color:#991b1b;
    box-shadow:0 6px 14px rgba(239,68,68,.18);
    transform:translateY(-1px);
  }
  
  .btn-danger-solid{
    background:linear-gradient(90deg, #ef4444, #dc2626);
    color:#fff;
    border:none;
    font-weight:700;
  }
  
  .avatar-btn{
    background:transparent;
    border:none;
    cursor:pointer;
    padding:0;
  }
  
  .avatar-circle{
    width:30px;
    height:30px;
    border-radius:999px;
    display:inline-flex;
    align-items:center;
    justify-content:center;
    font-size:12px;
    font-weight:700;
    background:linear-gradient(135deg, var(--accent), var(--accent-2));
    color:#fff;
  }
  
  /* Profile Dropdown */
  .profile-dropdown-wrapper{ position:relative; }
  .profile-dropdown{
    position:absolute;
    top:calc(100% + 8px);
    right:0;
    width:280px;
    background:#fff;
    border-radius:16px;
    border:1px solid rgba(148,163,184,.25);
    box-shadow:0 20px 50px rgba(15,23,42,.15);
    z-index:1000;
    overflow:hidden;
    animation:dropdown-fade 0.15s ease;
  }
  @keyframes dropdown-fade{
    from{ opacity:0; transform:translateY(-8px); }
    to{ opacity:1; transform:translateY(0); }
  }
  .profile-header{
    display:flex;
    align-items:center;
    gap:12px;
    padding:16px;
    background:linear-gradient(135deg, rgba(37,99,235,.05), rgba(20,184,166,.05));
  }
  .profile-avatar{
    width:44px;
    height:44px;
    border-radius:999px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:16px;
    font-weight:800;
    background:linear-gradient(135deg, var(--accent), var(--accent-2));
    color:#fff;
    flex-shrink:0;
  }
  .profile-info{ flex:1; min-width:0; }
  .profile-name{
    margin:0;
    font-size:14px;
    font-weight:700;
    color:var(--text);
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
  }
  .profile-email{
    margin:2px 0 0;
    font-size:12px;
    color:rgba(15,23,42,.55);
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
  }
  .profile-divider{ height:1px; background:rgba(148,163,184,.2); margin:0; }
  .profile-link{
    display:flex;
    align-items:center;
    gap:10px;
    padding:12px 16px;
    font-size:14px;
    color:var(--text);
    text-decoration:none;
    transition:background 0.15s ease;
    border:none;
    background:transparent;
    width:100%;
    cursor:pointer;
    text-align:left;
  }
  .profile-link:hover{ background:rgba(148,163,184,.08); }
  .profile-link-icon{ font-size:16px; width:20px; text-align:center; }
  .profile-logout{ color:#dc2626; }
  .profile-logout:hover{ background:rgba(239,68,68,.08); }
  
  /* Mobile profile header */
  .mobile-profile-header{
    display:flex;
    align-items:center;
    gap:12px;
    padding:8px 0 12px;
  }
  .mobile-profile-info{ flex:1; min-width:0; }
  .mobile-profile-name{ margin:0; font-size:14px; font-weight:700; color:var(--text); }
  .mobile-profile-email{ margin:2px 0 0; font-size:12px; color:rgba(15,23,42,.55); }
  .mobile-nav-divider{ height:1px; background:rgba(148,163,184,.2); margin:8px 0; }
  
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
  }
  
  .hamburger.active .bar:nth-child(1){ transform: translateY(8px) rotate(45deg); }
  .hamburger.active .bar:nth-child(2){ opacity: 0; }
  .hamburger.active .bar:nth-child(3){ transform: translateY(-8px) rotate(-45deg); }
  
  /* Mobile nav */
  .mobile-nav{
    display:none;
    flex-direction:column;
    gap:5px;
    background:rgba(248,250,252,.95);
    backdrop-filter: blur(12px);
    border-top:1px solid rgba(148,163,184,.25);
    padding:0 24px;
    max-height:0;
    overflow:hidden;
    transition:max-height 0.3s ease-in-out, padding 0.3s ease-in-out;
  }
  
  .mobile-nav.active{ max-height:400px; padding:16px 24px; }
  
  .mobile-nav a{
    color:var(--muted);
    padding:12px 0;
    font-size:14px;
    border-bottom:1px solid rgba(148,163,184,.15);
    transition:color 0.2s ease;
  }
  
  .mobile-nav a:hover{ color:var(--text); }
  
  .w-full{ width:100%; }
  
  /* Page content */
  .section-header{
    max-width:1200px;
    margin:0 auto;
    padding:16px 24px 0;
    display:flex;
    flex-direction:column;
    gap:6px;
  }
  
  .section-header h2{
    margin:0;
    font-size:20px;
    font-weight:800;
    letter-spacing:.01em;
  }
  
  .small-text{ font-size:12px; }
  
  /* Card grid */
  .card-grid{
    max-width:1200px;
    margin:0 auto;
    padding:14px 24px 40px;
    display:grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap:16px;
  }
  
  .op-card{
    background:var(--card);
    border-radius:var(--radius);
    padding:14px 16px;
    box-shadow:var(--shadow);
    border:var(--border);
    display:flex;
    flex-direction:column;
    gap:10px;
    min-height: 200px;
  }
  
  .op-card-header{
    display:flex;
    justify-content:space-between;
    align-items:center;
  }
  
  .badge{
    font-size:11px;
    padding:4px 8px;
    border-radius:999px;
    background:rgba(37,99,235,.08);
    color:var(--accent);
    font-weight:700;
  }
  
  .count-pill{
    font-size:11px;
    padding:4px 8px;
    border-radius:999px;
    background:rgba(20,184,166,.10);
    color:rgba(15,23,42,.85);
    border:1px solid rgba(20,184,166,.25);
    font-weight:700;
  }
  
  .op-title{
    font-size:16px;
    font-weight:800;
    margin:0;
  }
  
  .op-org{
    margin:0;
    font-size:13px;
    color:rgba(15,23,42,.7);
    font-weight:600;
  }
  
  .op-meta{
    font-size:12px;
    color:rgba(15,23,42,.65);
    display:flex;
    gap:6px;
    align-items:center;
    flex-wrap:wrap;
  }
  
  .op-actions{
    margin-top:auto;
    display:flex;
    gap:8px;
  }
  
  .small-btn{
    padding:8px 12px;
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
.footer-links{
  display:flex;
  gap:20px;
}
.footer-links a{
  color:var(--muted);
  text-decoration:none;
  font-size:13px;
  transition:color 0.2s;
}
.footer-links a:hover{
  color:var(--accent);
}
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

/* ALIGN UTIL */

.align-left,
.align-left *{
  text-align:left !important;
}
  /* Error popup */
  .error-popup{
    position: fixed;
    bottom: 24px;
    right: 24px;
    max-width: 360px;
    padding: 14px 18px;
    background: #fee2e2;
    color: #991b1b;
    border: 1px solid #fecaca;
    border-radius: 12px;
    font-size: 14px;
    line-height: 1.4;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12);
    z-index: 9999;
    animation: slide-in 0.25s ease-out;
  }
  
  @keyframes slide-in{
    from{ transform: translateY(12px); opacity: 0; }
    to{ transform: translateY(0); opacity: 1; }
  }
  
  @media (max-width: 900px){
    .nav-search{ display:none; }
    .card-grid{ grid-template-columns: 1fr; }
  }
  
  @media (max-width: 640px){
    .container{ padding:18px 16px 20px; }
    .desktop-nav{ display:none; }
    .hamburger{ display:flex; }
    .mobile-nav{ display:flex; }
    .section-header{ padding:14px 16px 0; }
    .card-grid{ padding:12px 16px 32px; }
  }



.status-pill {
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 12px;
  border: 1px solid rgba(0,0,0,0.08);
  font-weight:700;
}
.status-pill[data-status="pending"] {
  color:#a16207;
  background:linear-gradient(180deg, #fffbeb, #fef3c7);
  border-color:rgba(234,179,8,.35);
}
.status-pill[data-status="accepted"] {
  color:#166534;
  background:linear-gradient(180deg, #f0fdf4, #dcfce7);
  border-color:rgba(34,197,94,.3);
}
.status-pill[data-status="rejected"] {
  color:#b91c1c;
  background:linear-gradient(180deg, #fef2f2, #fee2e2);
  border-color:rgba(239,68,68,.3);
}
  </style>
  
