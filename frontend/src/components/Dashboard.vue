<template>
  <div class="dashboard">
    <header>
      <div class="container nav">
        <a class="brand" href="#">
          <!-- New logo: simple "hub" network icon -->
          <svg viewBox="0 0 64 64" aria-hidden="true">
            <defs>
              <linearGradient id="oh-search-g" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0" stop-color="#2563eb" />
                <stop offset="1" stop-color="#14b8a6" />
              </linearGradient>
            </defs>

            <circle cx="28" cy="28" r="18" fill="url(#oh-search-g)" opacity="0.08" />

            <circle
              cx="28"
              cy="28"
              r="12"
              fill="none"
              stroke="url(#oh-search-g)"
              stroke-width="3"
            />

            <path
              d="M36 36 L46 46"
              stroke="url(#oh-search-g)"
              stroke-width="3.2"
              stroke-linecap="round"
            />

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

        <div class="nav-search">
          <input
            type="search"
            placeholder="Search for all posts"
            v-model="searchQuery"
            @input="onSearchInput"
          />
        </div>

        <!-- Desktop navigation -->
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

        <!-- Hamburger button (for mobile) -->
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
        <!-- Mobile profile header -->
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
        <button
          class="btn-danger btn-danger-solid btn-post w-full"
          @click="onLogout"
        >
          Logout
        </button>
      </nav>
    </header>

    <main class="main">
      <div class="container">
        <!-- Greeting row -->
        <section class="welcome-row">
          <div>
            <p class="welcome-eyebrow">Welcome back,</p>
            <h1 class="welcome-title">{{ userName }}</h1>
            <p class="welcome-sub">
              Here’s what’s happening in your community resource hub today.
            </p>
          </div>

          <div class="welcome-stats">
            <div class="stat-card">
              <p class="stat-label">New matches</p>
              <p class="stat-value">{{ stats.newMatches }}</p>
            </div>
            <div class="stat-card">
              <p class="stat-label">Saved</p>
              <p class="stat-value">{{ stats.saved }}</p>
            </div>
            <div class="stat-card">
              <p class="stat-label">Applications</p>
              <p class="stat-value">{{ stats.applications }}</p>
            </div>
          </div>
        </section>

        <!-- Filters + layout grid -->
        <section class="layout-grid">
          <div class="main-column">
            <!-- Filters -->
            <div class="filters-row">
              <div class="pill-row">
                <button
                  v-for="f in filters"
                  :key="f.id"
                  class="pill"
                  :data-active="f.id === activeFilter"
                  @click="setFilter(f.id)"
                  type="button"
                >
                  {{ f.label }}
                </button>
              </div>

              <button class="btn btn-outline small-btn" type="button" @click="openAdvanced">
                Advanced filters
              </button>
            </div>

            <!-- Trending -->
            <div class="section-header">
              <h2>Featured Community Resources</h2>
              <span class="muted small-text">
                Based on what students around you are viewing
              </span>
            </div>

            <div class="card-grid">
              <article v-for="op in visibleTrending" :key="op.id" class="op-card">
                <div class="op-card-header">
                  <span class="badge">{{ op.type }}</span>
                  <button
                    class="icon-btn"
                    :aria-label="op.saved ? 'Unsave' : 'Save for later'"
                    @click="toggleSave(op.id)"
                    type="button"
                  >
                    <span v-if="op.saved">♥</span>
                    <span v-else>♡</span>
                  </button>
                </div>

                <h3 class="op-title">{{ op.title }}</h3>
                <p class="op-org">{{ op.org }}</p>

                <p class="op-desc">
                  {{ op.description }}
                </p>
                <p class="op-desc">{{ op.contact_email }}</p>

                <div class="op-meta">
                  <span>{{ op.location }}</span>
                  <span>•</span>
                  <span>
                    Deadline:
                    <span v-if="op.deadline_at">{{ new Date(op.deadline_at).toLocaleDateString() }}</span>
                    <span v-else>{{ op.deadline_text || 'Rolling' }}</span>
                  </span>

                </div>

                <div class="op-tags">
                  <span v-for="tag in op.tags" :key="tag" class="chip">
                    {{ tag }}
                  </span>
                </div>

                <div class="op-actions">
                  <button class="btn btn-ghost small-btn" type="button" @click="openDetails(op)">
                    View details
                  </button>

                  <button
                    v-if="op.allow_apply"
                    class="btn btn-primary small-btn"
                    type="button"
                    @click="openApply(op)"
                  >
                    Apply
                  </button>

                  <a
                    v-if="op.allow_external_apply && op.external_apply_url && op.external_url_approved === true"
                    class="btn btn-outline small-btn"
                    :href="op.external_apply_url"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Apply externally
                  </a>
                  <button class="btn-danger1 btn-danger-solid1 small-btn" type="button" @click="openReport(op)">
                    Report
                  </button>
                </div>
              </article>
            </div>
          </div>

          <!-- Sidebar -->
          <aside class="sidebar">
            <section class="sidebar-section">
              <h3>Quick actions</h3>
              <div class="sidebar-actions">
                <button class="btn btn-primary w-full" type="button" @click="openPost">
                  + Add a community resource
                </button>

                <button class="btn btn-outline w-full" type="button" @click="quickFilter('tutor')">
                  Find a tutor
                </button>

                <button class="btn btn-outline w-full" type="button" @click="quickFilter('club')">
                  Browse clubs
                </button>
              </div>
            </section>

            <section class="sidebar-section">
              <h3>Saved for later</h3>
              <p v-if="saved.length === 0" class="muted small-text">
                You haven’t saved anything yet. Tap the ♥ on an opportunity to keep it here.
              </p>

              <ul v-else class="saved-list">
                <li v-for="item in saved" :key="item.id" class="saved-item">
                  <div>
                    <p class="saved-title">{{ item.title }}</p>
                    <p class="saved-meta">
                      {{ item.type }} • {{ item.org }}
                    </p>
                  </div>
                  <button class="icon-btn small-icon" type="button" @click="openDetails(item)">
                    →
                  </button>
                </li>
              </ul>
            </section>
          </aside>
        </section>
      </div>
    </main>

    <footer>
      <div class="container">
        <div class="footer-inner">
          <p class="muted">
            © <span>{{ year }}</span> Opportunity Hub. Built by students, for students.
          </p>
          <div class="taglist">
            <router-link to="/about" class="pill">About Us</router-link>
            <router-link to="/references" class="pill">References</router-link>
            <button class="pill" type="button" @click="openPrivacy">Privacy</button>
            <button class="pill" type="button" @click="openContact">Contact</button>
            <button class="pill" type="button" @click="openPost">Post a community resource</button>
          </div>
        </div>
      </div>
    </footer>
    <!-- Report Modal -->
<div v-if="isReportOpen" class="modal-backdrop" @click.self="closeReport">
  <div class="modal">
    <h3>Report: {{ reportTarget?.title }}</h3>
    <p class="muted small-text">
      Tell us what’s wrong. This will be reviewed by a moderator later.
    </p>

    <div class="form-row">
      <label>Reason</label>
      <select v-model="reportForm.reason">
        <option disabled value="">Select a reason</option>
        <option value="scam">Scam / fake opportunity</option>
        <option value="inappropriate">Inappropriate content</option>
        <option value="fake_org">Fake organization</option>
        <option value="spam">Spam</option>
        <option value="other">Other</option>
      </select>
    </div>

    <div class="form-row">
      <label>Details (optional)</label>
      <textarea
        v-model="reportForm.comment"
        placeholder="Explain briefly (links, what looks suspicious, etc.)"
      ></textarea>
    </div>

    <div class="op-actions">
      <button class="btn btn-ghost small-btn" type="button" @click="closeReport">
        Cancel
      </button>
      <button
        class="btn btn-primary small-btn"
        type="button"
        :disabled="isReporting || !reportForm.reason"
        @click="submitReport"
      >
        {{ isReporting ? 'Sending...' : 'Submit report' }}
      </button>
    </div>

    <p v-if="reportError" class="muted small-text">{{ reportError }}</p>
    <p v-if="reportSuccess" class="success-text">Report submitted</p>
  </div>
</div>

    <!-- Apply Modal -->
    <div v-if="isApplyOpen" class="modal-backdrop" @click.self="isApplyOpen = false">
      <div class="modal">
        <h3>Apply to {{ applyingTo?.title }}</h3>

        <div class="form-row">
          <label>Full name</label>
          <input v-model="applyForm.full_name" />
        </div>

        <div class="form-row">
          <label>Email</label>
          <input v-model="applyForm.email" />
        </div>

        <div class="form-row">
          <label>Message</label>
          <textarea v-model="applyForm.message"></textarea>
        </div>

        <div class="op-actions">
          <button class="btn btn-ghost small-btn" type="button" @click="isApplyOpen = false">
            Cancel
          </button>
          <button class="btn btn-primary small-btn" type="button" @click="submitApplication">
            Apply
          </button>
        </div>

        <p v-if="applyError" class="muted small-text">{{ applyError }}</p>
        <p v-if="applySuccess" class="success-text">Application sent</p>
      </div>
    </div>

    <!-- Post Modal -->
    <div v-if="isPostOpen" class="modal-backdrop" @click.self="closePost">
      <div class="modal">
        <h3>Add community resource</h3>

        <div class="form-row">
          <label>Type</label>
          <select v-model="postForm.type">
            <option value="internship">Internship</option>
            <option value="club">Club</option>
            <option value="volunteering">Volunteering</option>
            <option value="tutor">Tutor</option>
          </select>
        </div>

        <div class="form-row">
          <label>Title</label>
          <input v-model="postForm.title" />
        </div>

        <div class="form-row">
          <label>Organization</label>
          <input v-model="postForm.org" />
        </div>

        <div class="form-row">
          <label>Description</label>
          <textarea v-model="postForm.description"></textarea>
        </div>

        <div class="form-row">
          <label>Location</label>
          <input v-model="postForm.location" />
        </div>

        <div class="form-row">
          <label>Deadline date</label>
          <input type="date" v-model="postForm.deadline_date" />
          <p class="muted small-text">Leave empty for rolling deadlines.</p>
        </div>

        <div class="form-row">
          <label>Deadline note</label>
          <input v-model="postForm.deadline_text" placeholder="Rolling / Jan 15 / Until filled" />
        </div>



        <div class="form-row">
          <label>Tags (comma separated)</label>
          <input v-model="postTags" placeholder="Web Dev, Paid, Beginner friendly" />
        </div>

        <hr class="divider" />

        <div class="form-row">
          <label>Contact email</label>
          <input v-model="postForm.contact_email" placeholder="example@org.com" />
        </div>

        <div class="form-row">
          <label class="row-inline">
            <input type="checkbox" v-model="postForm.allow_apply" />
            Allow people to apply on Opportunity Hub
          </label>
        </div>

        <div class="form-row">
          <label class="row-inline">
            <input type="checkbox" v-model="postForm.allow_external_apply" />
            Also show an external apply link
          </label>
        </div>

        <div v-if="postForm.allow_external_apply" class="form-row">
          <label>External apply URL</label>
          <input v-model="postForm.external_apply_url" placeholder="https://..." />
          <p class="muted small-text">
            Only allow links you trust. You can leave this off to keep everything on-site.
          </p>
        </div>

        <!-- Honeypot field: hidden from humans, bots will fill it -->
        <input
          type="text"
          v-model="postForm.website"
          name="website"
          autocomplete="off"
          tabindex="-1"
          style="position: absolute; left: -9999px; opacity: 0; height: 0; width: 0;"
          aria-hidden="true"
        />

        <div class="op-actions">
          <button class="btn btn-ghost small-btn" type="button" @click="closePost">Cancel</button>
          <button
            class="btn btn-primary small-btn"
            type="button"
            @click="submitPost"
            :disabled="isPosting"
          >
            {{ isPosting ? 'Posting...' : 'Post' }}
          </button>
        </div>

        <p v-if="postError" class="muted small-text">{{ postError }}</p>
      </div>
    </div>

    <!-- Opportunity Details Modal (simple, optional but useful) -->
    <div v-if="isDetailsOpen" class="modal-backdrop" @click.self="closeDetails">
      <div class="modal">
        <h3>{{ detailsOp?.title }}</h3>
        <p class="muted">{{ detailsOp?.org }} • {{ detailsOp?.type }}</p>

        <div class="form-row">
          <label>Description</label>
          <p class="op-desc">{{ detailsOp?.description }}</p>
        </div>

        <div class="form-row">
          <label>Location</label>
          <p class="muted">{{ detailsOp?.location }}</p>
        </div>

        <div class="form-row">
          <label>Deadline</label>
          <p class="muted">{{ detailsOp?.deadline }}</p>
        </div>

        <div class="form-row">
          <label>Contact</label>
          <p class="muted">{{ detailsOp?.contact_email }}</p>
        </div>

        <div class="op-tags" v-if="detailsOp?.tags?.length">
          <span v-for="tag in detailsOp.tags" :key="tag" class="chip">{{ tag }}</span>
        </div>

        <div class="op-actions">
          <button class="btn btn-ghost small-btn" type="button" @click="closeDetails">
            Close
          </button>

          <button
            class="btn btn-outline small-btn"
            type="button"
            @click="toggleSave(detailsOp.id)"
          >
            {{ detailsOp?.saved ? 'Unsave' : 'Save' }}
          </button>

          <button
            v-if="detailsOp?.allow_apply"
            class="btn btn-primary small-btn"
            type="button"
            @click="openApply(detailsOp)"
          >
            Apply
          </button>

          <a
            v-if="detailsOp?.allow_external_apply && detailsOp?.external_apply_url && detailsOp?.external_url_approved === true"
            class="btn btn-outline small-btn"
            :href="detailsOp.external_apply_url"
            target="_blank"
            rel="noopener noreferrer"
          >
            External link
          </a>
        </div>
      </div>
    </div>

    <!-- Advanced Filters Modal -->
    <div v-if="isAdvancedOpen" class="modal-backdrop" @click.self="closeAdvanced">
      <div class="modal">
        <h3>Advanced filters</h3>

        <div class="form-row">
          <label>Location contains</label>
          <input v-model="advanced.location" placeholder="e.g. Fairfax, Remote" />
        </div>

        <div class="form-row">
          <label>Tags include (comma separated)</label>
          <input v-model="advanced.tags" placeholder="Paid, Beginner, Web" />
        </div>

        <div class="form-row">
          <label class="row-inline">
            <input type="checkbox" v-model="advanced.onlyInternalApply" />
            Only show opportunities with on-site apply
          </label>
        </div>

        <div class="form-row">
          <label class="row-inline">
            <input type="checkbox" v-model="advanced.onlyExternalApply" />
            Only show community resources with external apply link
          </label>
        </div>

        <div class="form-row">
          <label>Sort by</label>
          <select v-model="advanced.sort">
            <option value="newest">Newest</option>
            <option value="deadline">Deadline (best effort)</option>
            <option value="org">Organization (A→Z)</option>
          </select>
          <p class="muted small-text">
            Deadline sort is best-effort because deadlines are stored as text (e.g., “Jan 15 / Rolling”).
          </p>
        </div>

        <div class="op-actions">
          <button class="btn btn-ghost small-btn" type="button" @click="resetAdvanced">
            Reset
          </button>
          <button class="btn btn-outline small-btn" type="button" @click="closeAdvanced">
            Close
          </button>
          <button class="btn btn-primary small-btn" type="button" @click="applyAdvanced">
            Apply
          </button>
        </div>
      </div>
    </div>

    <!-- Privacy Modal -->
    <div v-if="isPrivacyOpen" class="modal-backdrop" @click.self="isPrivacyOpen = false">
      <div class="modal">
        <h3>Privacy</h3>
        <p class="muted">
          Opportunity Hub stores your account info (username, email) and the posts you create.
          Applications you submit are visible to the creator of that post. We don’t sell your data.
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

        <div class="form-row">
          <label>Message</label>
          <textarea
            v-model="contactMessage"
            placeholder="Tell us what’s broken or what you want next..."
          ></textarea>
        </div>

        <div v-if="contactError" class="error-popup" style="position: static; margin: 12px 0;">
          {{ contactError }}
        </div>
        <p v-if="contactSuccess" class="success-text">Message sent successfully!</p>

        <div class="op-actions">
          <button class="btn btn-ghost small-btn" type="button" @click="isContactOpen = false">
            Close
          </button>
          <button 
            class="btn btn-primary small-btn" 
            type="button" 
            @click="sendContact"
            :disabled="submittingContact || !contactMessage.trim() || contactMessage.trim().length < 10"
          >
            {{ submittingContact ? 'Sending...' : 'Send Message' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import AxiosInstance from '@/apiClient'
import router from '@/router'
import { useAuth } from '@/lib/authStore'

const { clearToken, setUser, user, userInitials } = useAuth()
const year = new Date().getFullYear()

// apply modal
const isApplyOpen = ref(false)
const applyingTo = ref(null)
const applyError = ref('')
const applySuccess = ref(false)


// report modal
const isReportOpen = ref(false)
const reportTarget = ref(null)
const isReporting = ref(false)
const reportError = ref('')
const reportSuccess = ref(false)

const reportForm = ref({
  reason: '',
  comment: '',
})

function openReport(op) {
  reportTarget.value = op
  reportError.value = ''
  reportSuccess.value = false
  reportForm.value = { reason: '', comment: '' }
  isReportOpen.value = true
}

function closeReport() {
  isReportOpen.value = false
  reportTarget.value = null
}

async function submitReport() {
  reportError.value = ''
  reportSuccess.value = false

  if (!reportTarget.value?.id) {
    reportError.value = 'No opportunity selected'
    return
  }
  if (!reportForm.value.reason) {
    reportError.value = 'Please select a reason'
    return
  }

  isReporting.value = true
  try {
    await AxiosInstance.post(`/opportunities/${reportTarget.value.id}/report`, {
      reason: reportForm.value.reason,
      comment: (reportForm.value.comment || '').trim(),
    })
    reportSuccess.value = true

    // auto close after a moment (optional)
    setTimeout(() => closeReport(), 700)
  } catch (e) {
    reportError.value =
      e?.response?.data?.detail?.message ||
      e?.response?.data?.detail ||
      'Could not submit report'
  } finally {
    isReporting.value = false
  }
}


const applyForm = ref({
  full_name: '',
  email: '',
  message: '',
})

// nav
const isMenuOpen = ref(false)
function toggleMenu() {
  isMenuOpen.value = !isMenuOpen.value
}
function closeMenu() {
  isMenuOpen.value = false
}

// logout
function onLogout() {
  clearToken()
  trending.value = []
  savedList.value = []
  userName.value = '...'
  router.push('/')
}

// post modal
const isPostOpen = ref(false)
const isPosting = ref(false)
const postError = ref('')

const postForm = ref({
  type: 'internship',
  title: '',
  org: '',
  description: '',
  location: '',

  deadline_date: '',
  deadline_text: '',

  contact_email: '',
  allow_apply: true,
  allow_external_apply: false,
  external_apply_url: '',

  // Honeypot field - hidden, should always be empty from real users
  website: '',
})

const postTags = ref('')

function openPost() {
  postError.value = ''
  isPostOpen.value = true
  closeMenu()
}
function closePost() {
  isPostOpen.value = false
}

// tags for posting
function parsePostTags(str) {
  return String(str || '')
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean)
}

// dashboard state
const userName = ref(user.value?.username || '...')
const userEmail = ref(user.value?.email || '')
const stats = ref({ newMatches: 0, saved: 0, applications: 0 })

// profile dropdown
const isProfileOpen = ref(false)
function toggleProfileDropdown() {
  isProfileOpen.value = !isProfileOpen.value
}
function closeProfileDropdown() {
  isProfileOpen.value = false
}
// Close dropdown when clicking outside
function handleClickOutside(e) {
  if (isProfileOpen.value && !e.target.closest('.profile-dropdown-wrapper')) {
    isProfileOpen.value = false
  }
}

const filters = [
  { id: 'all', label: 'All' },
  { id: 'internship', label: 'Internships' },
  { id: 'club', label: 'Clubs' },
  { id: 'volunteering', label: 'Volunteering' },
  { id: 'tutor', label: 'Tutors' },
]
const activeFilter = ref('all')

// search
const searchQuery = ref('')
let searchTimer = null

// data
const trending = ref([])
const savedList = ref([])

function prettyType(t) {
  if (!t) return ''
  const s = String(t)
  return s.charAt(0).toUpperCase() + s.slice(1)
}

const saved = computed(() => savedList.value)

// backend loads
async function loadDashboard() {
  const res = await AxiosInstance.get('/dashboard')
  const data = res.data

  userName.value = data.me.username
  userEmail.value = data.me.email
  stats.value = data.stats

  // Store user info in authStore for other components
  setUser({ id: data.me.id, username: data.me.username, email: data.me.email })

  trending.value = (data.trending || []).map((op) => ({
    ...op,
    type: prettyType(op.type),
  }))

  savedList.value = (data.saved || []).map((op) => ({
    ...op,
    type: prettyType(op.type),
  }))
}

async function loadOpportunities() {
  const params = {}

  if (activeFilter.value !== 'all') params.type = activeFilter.value
  if (searchQuery.value.trim()) params.q = searchQuery.value.trim()

  const res = await AxiosInstance.get('/opportunities', { params })
  const ops = res.data || []

  const savedIds = new Set(savedList.value.map((x) => x.id))

  trending.value = ops.map((op) => ({
    ...op,
    type: prettyType(op.type),
    saved: Boolean(op.saved ?? savedIds.has(op.id)),
  }))
}

// apply modal
function openApply(op) {
  applyingTo.value = op
  applyError.value = ''
  applySuccess.value = false
  applyForm.value = { full_name: '', email: '', message: '' }
  isApplyOpen.value = true
}

async function submitApplication() {
  applyError.value = ''
  try {
    await AxiosInstance.post(`/opportunities/${applyingTo.value.id}/apply`, applyForm.value)
    applySuccess.value = true
  } catch (e) {
    applyError.value = e?.response?.data?.detail?.message || 'Could not apply'
  }
}

// search debounce
function onSearchInput() {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(async () => {
    await loadOpportunities()
  }, 250)
}

// filter
async function setFilter(id) {
  activeFilter.value = id
  await loadOpportunities()
}

// quick filter actions
async function quickFilter(typeId) {
  activeFilter.value = typeId
  await loadOpportunities()
  closeMenu()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// save/unsave
async function toggleSave(id) {
  const idx = trending.value.findIndex((x) => x.id === id)
  if (idx === -1) return

  const op = trending.value[idx]

  if (op.saved) {
    await AxiosInstance.delete(`/opportunities/${id}/save`)

    trending.value[idx] = { ...op, saved: false }
    savedList.value = savedList.value.filter((x) => x.id !== id)
    stats.value.saved = Math.max(0, (stats.value.saved || 0) - 1)

    // keep details modal in sync if open
    if (detailsOp.value?.id === id) detailsOp.value = { ...detailsOp.value, saved: false }
  } else {
    await AxiosInstance.post(`/opportunities/${id}/save`)

    trending.value[idx] = { ...op, saved: true }
    savedList.value = [{ ...trending.value[idx] }, ...savedList.value]
    stats.value.saved = (stats.value.saved || 0) + 1

    // keep details modal in sync if open
    if (detailsOp.value?.id === id) detailsOp.value = { ...detailsOp.value, saved: true }
  }
}

// Turn API validation errors into user-friendly messages for the post form
function formatPostError(e) {
  const detail = e?.response?.data?.detail
  if (Array.isArray(detail) && detail.length > 0) {
    const first = detail[0]
    const loc = first.loc || []
    const msg = (first.msg || '').toLowerCase()
    const field = loc[loc.length - 1]
    if (field === 'contact_email' || msg.includes('email')) {
      return 'Please enter a valid email address for Contact email.'
    }
    if (field === 'title') return 'Please enter a title.'
    if (field === 'org') return 'Please enter an organization name.'
    if (field === 'description') return 'Please enter a description.'
    if (field === 'location') return 'Please enter a location.'
    if (first.msg) return first.msg
  }
  if (typeof detail === 'object' && detail?.message) return detail.message
  if (typeof detail === 'string') return detail
  return e?.message || 'Failed to post. Please check your entries and try again.'
}

// submit post
async function submitPost() {
  postError.value = ''
  isPosting.value = true
  try {
    // Convert <input type="date"> value ("YYYY-MM-DD") to ISO datetime
    const deadline_at = deadlineDateToISO(postForm.value.deadline_date)
    function deadlineDateToISO(dateStr) {
      if (!dateStr) return null

      // local end-of-day (23:59:59.999)
      const d = new Date(dateStr + 'T23:59:59.999')
      return d.toISOString() // convert to UTC ISO for backend
    }

    const payload = {
      type: postForm.value.type,
      title: postForm.value.title,
      org: postForm.value.org,
      description: postForm.value.description,
      location: postForm.value.location,

      // ✅ new fields (backend expects these after your change)
      deadline_at,
      deadline_text: (postForm.value.deadline_text || '').trim(),

      tags: parsePostTags(postTags.value),

      contact_email: postForm.value.contact_email,
      allow_apply: postForm.value.allow_apply,
      allow_external_apply: postForm.value.allow_external_apply,
      external_apply_url: postForm.value.external_apply_url || null,

      // Honeypot field - should always be empty from real users
      website: postForm.value.website || null,
    }

    await AxiosInstance.post('/opportunities', payload)

    // Close modal + reset form (keep your reset code)
    isPostOpen.value = false

    // Send them to My Posts so they see status (approved vs flagged)
    router.push('/my-posts')


    // reset
    isPostOpen.value = false
    postForm.value = {
      type: 'internship',
      title: '',
      org: '',
      description: '',
      location: '',

      deadline_date: '',
      deadline_text: '',

      contact_email: '',
      allow_apply: true,

      allow_external_apply: false,
      external_apply_url: '',

      website: '',  // honeypot reset
    }
    postTags.value = ''
  } catch (e) {
      const isTimeout =
        e?.code === 'ECONNABORTED' ||
        String(e?.message || '').toLowerCase().includes('timeout')

      if (isTimeout) {
        postError.value = 'Request timed out. Your post may still have been created. Checking...'
        try {
          const check = await AxiosInstance.get('/users/me/opportunities')
          const exists = (check.data || []).some(o =>
            (o.title || '').trim() === (postForm.value.title || '').trim() &&
            (o.org || '').trim() === (postForm.value.org || '').trim()
          )
          if (exists) {
            router.push('/my-posts')
            return
          }
        } catch {}
      }

      postError.value = formatPostError(e)

  } finally {
    isPosting.value = false
  }
}

/* ---------------------------
   Opportunity details modal
---------------------------- */
const isDetailsOpen = ref(false)
const detailsOp = ref(null)

function openDetails(op) {
  detailsOp.value = op
  isDetailsOpen.value = true
  closeMenu()
}
function closeDetails() {
  isDetailsOpen.value = false
  detailsOp.value = null
}

/* ---------------------------
   Advanced Filters
---------------------------- */
const isAdvancedOpen = ref(false)
const advanced = ref({
  location: '',
  tags: '',
  onlyInternalApply: false,
  onlyExternalApply: false,
  sort: 'newest',
})
const appliedAdvanced = ref({ ...advanced.value })

function openAdvanced() {
  isAdvancedOpen.value = true
  closeMenu()
}
function closeAdvanced() {
  isAdvancedOpen.value = false
}
function resetAdvanced() {
  advanced.value = {
    location: '',
    tags: '',
    onlyInternalApply: false,
    onlyExternalApply: false,
    sort: 'newest',
  }
}
function applyAdvanced() {
  appliedAdvanced.value = { ...advanced.value }
  isAdvancedOpen.value = false
}

function parseTagsInput(str) {
  return String(str || '')
    .split(',')
    .map((s) => s.trim().toLowerCase())
    .filter(Boolean)
}

function normalizeTags(arr) {
  return (arr || [])
    .map((t) => String(t).trim().toLowerCase())
    .filter(Boolean)
}

function tryParseDeadline(s) {
  if (!s) return null
  const raw = String(s).split('/')[0].trim()
  const d = new Date(raw)
  if (!isNaN(d.getTime())) return d
  return null
}

const visibleTrending = computed(() => {
  let list = [...trending.value]
  const a = appliedAdvanced.value

  // location filter
  const locQ = String(a.location || '').trim().toLowerCase()
  if (locQ) {
    list = list.filter((op) => String(op.location || '').toLowerCase().includes(locQ))
  }

  // tags filter
  const wantTags = parseTagsInput(a.tags)
  if (wantTags.length) {
    list = list.filter((op) => {
      const have = new Set(normalizeTags(op.tags))
      return wantTags.every((t) => have.has(t))
    })
  }

  // apply method filters
  if (a.onlyInternalApply) list = list.filter((op) => Boolean(op.allow_apply))
  if (a.onlyExternalApply) {
    list = list.filter((op) => Boolean(op.allow_external_apply && op.external_apply_url && op.external_url_approved === true))
  }

  // sorting
  if (a.sort === 'org') {
    list.sort((x, y) => String(x.org || '').localeCompare(String(y.org || '')))
  } else if (a.sort === 'deadline') {
    list.sort((x, y) => {
      const dx = x.deadline_at ? new Date(x.deadline_at).getTime() : Infinity
      const dy = y.deadline_at ? new Date(y.deadline_at).getTime() : Infinity
      return dx - dy
    })
  } else {
    // newest: backend already returns newest first, keep order
  }

  return list
})

/* ---------------------------
   Footer modals
---------------------------- */
const isPrivacyOpen = ref(false)
const isContactOpen = ref(false)
const contactMessage = ref('')
const contactSuccess = ref(false)
const contactError = ref('')
const submittingContact = ref(false)

function openPrivacy() {
  isPrivacyOpen.value = true
  closeMenu()
}
function openContact() {
  isContactOpen.value = true
  contactSuccess.value = false
  contactError.value = ''
  contactMessage.value = ''
  closeMenu()
}

async function sendContact() {
  if (!contactMessage.value.trim() || contactMessage.value.trim().length < 10) return
  
  submittingContact.value = true
  contactError.value = ''
  contactSuccess.value = false
  
  try {
    await AxiosInstance.post('/contact', {
      message: contactMessage.value.trim()
    })
    contactSuccess.value = true
    contactMessage.value = ''
    setTimeout(() => {
      isContactOpen.value = false
      contactSuccess.value = false
    }, 2000)
  } catch (e) {
    contactError.value = 
      e?.response?.data?.detail?.message ||
      e?.response?.data?.detail ||
      e?.message ||
      'Failed to send message. Please try again.'
  } finally {
    submittingContact.value = false
  }
}

onMounted(async () => {
  document.addEventListener('click', handleClickOutside)
  await loadDashboard()
  await loadOpportunities()
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
    
<style scoped>

:global(:root){
  /* Light, friendly "education" theme */
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

.dashboard{
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

.navlinks a:hover{
  color:var(--text);
  text-decoration: underline;
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


/* Reddish "danger" button — for Logout, Delete, etc */
/* Soft logout button — fits your UI */
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

/* Hover: sharper, not glowy */
.btn-danger:hover{
  background:linear-gradient(180deg, #fee2e2, #fecaca);
  border-color:#ef4444;
  color:#991b1b;
  box-shadow:0 6px 14px rgba(239,68,68,.18);
  transform:translateY(-1px);
}

/* Pressed */
.btn-danger:active{
  transform:translateY(0);
  box-shadow:0 3px 8px rgba(239,68,68,.15);
}


/* Filled red version if you want it stronger */
.btn-danger-solid{
  background:linear-gradient(90deg, #ef4444, #dc2626);
  color:#fff;
  border:none;
  font-weight:700;
}

.btn-danger-solid:hover{
  box-shadow:0 14px 28px rgba(239,68,68,.35);
}


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
  gap: 5px;
  background:rgba(248,250,252,.95);
  backdrop-filter: blur(12px);
  border-top:1px solid rgba(148,163,184,.25);
  padding:0 24px;
  max-height:0;
  overflow:hidden;
  transition:max-height 0.3s ease-in-out, padding 0.3s ease-in-out;
}

.mobile-nav.active{
  max-height:400px;
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

/* RESPONSIVE */

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


.divider{
  border: none;
  border-top: 1px solid rgba(148,163,184,.35);
  margin: 10px 0;
}

.row-inline{
  display:flex;
  gap:10px;
  align-items:center;
  font-weight:600;
}


.main{
  padding:16px 0 40px;
}

.welcome-row{
  display:flex;
  justify-content:space-between;
  align-items:flex-start;
  gap:24px;
  margin:24px 0 20px;
}

.welcome-eyebrow{
  font-size:13px;
  text-transform:uppercase;
  letter-spacing:.15em;
  color:rgba(15,23,42,.6);
  margin-bottom:4px;
}

.welcome-title{
  font-size:28px;
  font-weight:800;
  letter-spacing:.02em;
  margin:0 0 6px;
}

.welcome-sub{
  font-size:14px;
  color:rgba(15,23,42,.7);
  max-width:420px;
}

.welcome-stats{
  display:flex;
  gap:12px;
  flex-wrap:wrap;
}

.stat-card{
  min-width:90px;
  padding:10px 12px;
  border-radius:12px;
  background:var(--panel);
  box-shadow:var(--shadow);
  border:var(--border);
}

.stat-label{
  font-size:11px;
  text-transform:uppercase;
  letter-spacing:.16em;
  color:rgba(15,23,42,.55);
  margin-bottom:4px;
}

.stat-value{
  font-size:20px;
  font-weight:700;
}

/* Layout grid */
.layout-grid{
  display:grid;
  grid-template-columns: minmax(0, 2.4fr) minmax(260px, 1fr);
  gap:24px;
  align-items:flex-start;
}

.main-column{
  display:flex;
  flex-direction:column;
  gap:18px;
}

.filters-row{
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:12px;
}

.pill-row{
  display:flex;
  flex-wrap:wrap;
  gap:8px;
}

.small-btn{
  padding:8px 12px;
  font-size:12px;
}

/* Reddish "danger" button — for Logout, Delete, etc */
/* Soft logout button — fits your UI */
.btn-danger1{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  gap:8px;
  padding:8px 12px;
  border-radius:999px;
  border:1px solid rgba(239,68,68,.25);
  background:linear-gradient(180deg, #fffafa, #fee2e2);
  color:#b91c1c;
  font-size:12px;
  font-weight:600;
  cursor:pointer;
  transition:all .18s ease;
}

/* Hover: sharper, not glowy */
.btn-danger1:hover{
  background:linear-gradient(180deg, #fee2e2, #fecaca);
  border-color:#ef4444;
  color:#991b1b;
  box-shadow:0 6px 14px rgba(239,68,68,.18);
  transform:translateY(-1px);
}

/* Pressed */
.btn-danger1:active{
  transform:translateY(0);
  box-shadow:0 3px 8px rgba(239,68,68,.15);
}


/* Filled red version if you want it stronger */
.btn-danger-solid1{
  background:linear-gradient(90deg, #ef4444, #dc2626);
  color:#fff;
  border:none;
  font-weight:700;
}

.btn-danger-solid1:hover{
  box-shadow:0 14px 28px rgba(239,68,68,.35);
}



.section-header{
  display:flex;
  flex-direction:column;
  gap:4px;
}

.section-header h2{
  font-size:18px;
  font-weight:700;
}

.small-text{
  font-size:12px;
}

.card-grid{
  display:grid;
  grid-template-columns: minmax(0, 1fr);
  gap:16px;
}

/* Opportunity cards */
.op-card{
  background:var(--card);
  border-radius:var(--radius);
  padding:14px 16px;
  box-shadow:var(--shadow);
  border:var(--border);
  display:flex;
  flex-direction:column;
  gap:8px;
}

.op-card-header{
  display:flex;
  justify-content:space-between;
  align-items:center;
}

.row-inline{
  display:flex;
  align-items:center;
  gap:10px;
  font-weight:600;
}
.row-inline input{ width:auto; }


.badge{
  font-size:11px;
  padding:4px 8px;
  border-radius:999px;
  background:rgba(37,99,235,.08);
  color:var(--accent);
  font-weight:600;
}

.op-title{
  font-size:16px;
  font-weight:700;
  margin:0;
}
/* Make long descriptions wrap normally */
.op-desc,
.op-title,
.op-org {
  white-space: normal;
  overflow-wrap: anywhere;   /* breaks long words/urls */
  word-break: break-word;    /* fallback */
}

/* If your card uses flex/grid, prevent min-width from blocking wrapping */
.op-card,
.op-card * {
  min-width: 0;
}

.op-org{
  font-size:13px;
  color:rgba(15,23,42,.7);
}

.op-desc{
  font-size:13px;
  color:rgba(15,23,42,.85);
}

.op-meta{
  font-size:12px;
  color:rgba(15,23,42,.65);
  display:flex;
  gap:4px;
  align-items:center;
}

.op-tags{
  display:flex;
  flex-wrap:wrap;
  gap:6px;
}

.chip{
  font-size:11px;
  padding:4px 8px;
  border-radius:999px;
  background:var(--card-2);
  border:1px solid rgba(148,163,184,.5);
}

/* Sidebar */
.sidebar{
  display:flex;
  flex-direction:column;
  gap:18px;
}

.sidebar-section{
  background:var(--panel-elevated);
  border-radius:var(--radius);
  padding:12px 14px;
  box-shadow:var(--shadow);
  border:var(--border);
}

.sidebar-section h3{
  font-size:14px;
  font-weight:700;
  margin-bottom:8px;
}

.sidebar-actions{
  display:flex;
  flex-direction:column;
  gap:8px;
}

.w-full{
  width:100%;
}

.saved-list{
  list-style:none;
  padding:0;
  margin:0;
  display:flex;
  flex-direction:column;
  gap:8px;
}

.saved-item{
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:8px;
  padding:6px 0;
  border-bottom:1px solid rgba(148,163,184,.25);
}

.saved-item:last-child{
  border-bottom:none;
}

.saved-title{
  font-size:13px;
  font-weight:600;
}

.saved-meta{
  font-size:12px;
  color:rgba(15,23,42,.6);
}

/* Icon buttons */
.icon-btn{
  background:transparent;
  border:none;
  cursor:pointer;
  font-size:13px;
}

.small-icon{
  font-size:14px;
}

/* Nav search + avatar */
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
.profile-dropdown-wrapper{
  position:relative;
}

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

.profile-info{
  flex:1;
  min-width:0;
}

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

.profile-divider{
  height:1px;
  background:rgba(148,163,184,.2);
  margin:0;
}

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

.profile-link:hover{
  background:rgba(148,163,184,.08);
}

.profile-link-icon{
  font-size:16px;
  width:20px;
  text-align:center;
}

.profile-logout{
  color:#dc2626;
}

.profile-logout:hover{
  background:rgba(239,68,68,.08);
}

/* Mobile profile header */
.mobile-profile-header{
  display:flex;
  align-items:center;
  gap:12px;
  padding:8px 0 12px;
}

.mobile-profile-info{
  flex:1;
  min-width:0;
}

.mobile-profile-name{
  margin:0;
  font-size:14px;
  font-weight:700;
  color:var(--text);
}

.mobile-profile-email{
  margin:2px 0 0;
  font-size:12px;
  color:rgba(15,23,42,.55);
}

.mobile-nav-divider{
  height:1px;
  background:rgba(148,163,184,.2);
  margin:8px 0;
}

/* RESPONSIVE */
@media (max-width: 900px){
  .welcome-row{
    flex-direction:column;
    align-items:flex-start;
  }

  .layout-grid{
    grid-template-columns: minmax(0, 1fr);
  }

  .nav-search{
    display:none;
  }
}
/* Minimal modal styling only. Won’t affect your existing layout. */
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

/* Make modal scrollable */
.modal{
  background: #fff;
  border-radius: 14px;
  padding: 20px;
  width: 100%;
  max-width: 520px;
  /* THIS is the key part */
  max-height: 85vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 20px 50px rgba(0,0,0,.25);
  z-index: 1001;
}

/* Smooth scrollbar */
.modal::-webkit-scrollbar{
  width: 8px;
}
.modal::-webkit-scrollbar-thumb{
  background: rgba(0,0,0,.2);
  border-radius: 4px;
}




.modal h3 {
  margin: 0 0 12px 0;
}

.form-row {
  display: grid;
  gap: 6px;
  margin: 10px 0;
}

.form-row label {
  font-size: 0.9rem;
  opacity: 0.8;
}

.form-row input,
.form-row select,
.form-row textarea {
  width: 100%;
  border: 1px solid rgba(0, 0, 0, 0.12);
  border-radius: 10px;
  padding: 10px 12px;
  outline: none;
}

/* Checkbox row alignment fix */
.form-row .row-inline {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  opacity: 1;
  cursor: pointer;
}

.form-row .row-inline input[type="checkbox"] {
  width: auto;
  margin: 0;
  cursor: pointer;
  accent-color: var(--accent);
}

.form-row textarea {
  min-height: 110px;
  resize: vertical;
}
    </style>