<template>
  <div class="Moderator">
    <header>
      <div class="container nav">
        <!-- Brand -->
        <router-link to="/moderation" class="brand-link" @click="closeMenu">
          <span class="brand">
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
            <span class="brand-text">
              Opportunity Hub
              <span class="brand-sub">Moderation</span>
            </span>
          </span>
        </router-link>

        <!-- Desktop right actions -->
        <nav class="nav-actions desktop-nav">
          <!-- Profile dropdown -->
          <div class="profile-dropdown-wrapper">
            <button class="avatar-btn" @click="toggleProfileDropdown" title="Moderator profile">
              <span class="avatar-circle mod-avatar">MOD</span>
            </button>
            <div v-if="isProfileOpen" class="profile-dropdown">
              <div class="profile-header mod-profile-header">
                <span class="profile-avatar mod-avatar">MOD</span>
                <div class="profile-info">
                  <p class="profile-name">{{ userName }}</p>
                  <p class="profile-email">{{ userEmail }}</p>
                  <span class="mod-badge">Moderator</span>
                </div>
              </div>
              <div class="profile-divider"></div>
              <button class="profile-link profile-logout" @click="onLogout">
                <span class="profile-link-icon">🚪</span> Logout
              </button>
            </div>
          </div>
        </nav>

        <!-- Hamburger -->
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

      <!-- Mobile nav -->
      <nav class="mobile-nav" :class="{ active: isMenuOpen }">
        <div class="mobile-profile-header">
          <span class="avatar-circle mod-avatar">MOD</span>
          <div class="mobile-profile-info">
            <p class="mobile-profile-name">{{ userName }}</p>
            <p class="mobile-profile-email">{{ userEmail }}</p>
            <span class="mod-badge">Moderator</span>
          </div>
        </div>
        <div class="mobile-nav-divider"></div>
        <button class="btn-danger btn-danger-solid w-full" @click="onLogout">
          Logout
        </button>
      </nav>
    </header>

    <div v-if="pageError" class="error-popup">{{ pageError }}</div>

    <!-- Header with tabs -->
    <div class="section-header">
      <div class="title-row">
        <h2>Moderation Dashboard</h2>
        <button class="btn btn-ghost small-btn" @click="refresh">Refresh</button>
      </div>

      <span class="muted small-text">
        Review user appeals, reported posts, and external links.
      </span>

      <!-- Tabs -->
      <div class="tabs-row">
        <button 
          class="tab-btn" 
          :class="{ active: activeTab === 'appeals' }" 
          @click="activeTab = 'appeals'"
        >
          Appeals
          <span v-if="appeals.length" class="tab-badge">{{ appeals.length }}</span>
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: activeTab === 'reports' }" 
          @click="activeTab = 'reports'"
        >
          Reports
          <span v-if="reports.length" class="tab-badge danger">{{ reports.length }}</span>
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: activeTab === 'links' }" 
          @click="activeTab = 'links'"
        >
          External Links
          <span v-if="externalUrls.length" class="tab-badge warning">{{ externalUrls.length }}</span>
        </button>
      </div>
    </div>

    <div v-if="loading" class="muted small-text" style="padding: 0 20px;">
      Loading…
    </div>

    <!-- Appeals Tab -->
    <div v-else-if="activeTab === 'appeals'">
      <div v-if="appeals.length === 0" class="empty-wrap">
        <div class="empty-card">
          <h3>No pending appeals</h3>
          <p class="muted">
            When users appeal their flagged posts, they will appear here for review.
          </p>
        </div>
      </div>

      <div v-else class="card-grid">
        <article v-for="op in appeals" :key="op.id" class="op-card">
          <div class="op-card-top">
            <div class="left">
              <span class="badge">{{ prettyType(op.type) }}</span>
              <span class="flag-pill">Flagged</span>
            </div>
            <div class="right">
              <span class="time-pill" v-if="op.appeal_at">
                Appealed {{ shortDate(op.appeal_at) }}
              </span>
            </div>
          </div>

          <h3 class="op-title">{{ op.title }}</h3>
          <p class="op-org">{{ op.org }}</p>
          <p class="op-creator">by @{{ op.creator_username }}</p>

          <p class="op-desc">{{ op.description }}</p>

          <!-- Flag info -->
          <div class="mod-box">
            <div class="mod-row">
              <span class="mod-k">Flag Reason</span>
              <span class="mod-v">{{ op.flagged_reason || 'Auto-flagged by AI' }}</span>
            </div>
            <div class="mod-row" v-if="(op.flagged_categories || []).length">
              <span class="mod-k">Categories</span>
              <div class="tag-row">
                <span v-for="c in op.flagged_categories" :key="c" class="chip danger-chip">{{ c }}</span>
              </div>
            </div>
          </div>

          <!-- Appeal message -->
          <div class="appeal-box">
            <div class="appeal-header">
              <span class="appeal-icon">📝</span>
              <span class="appeal-label">User's Appeal</span>
            </div>
            <p class="appeal-message">"{{ op.appeal_message }}"</p>
          </div>

          <div class="op-actions">
            <button 
              class="btn btn-primary small-btn" 
              :disabled="decidingId === op.id"
              @click="decideAppeal(op.id, 'approved')"
            >
              Approve
            </button>
            <button 
              class="btn btn-outline small-btn" 
              :disabled="decidingId === op.id"
              @click="openDenyModal(op)"
            >
              Deny
            </button>
          </div>
        </article>
      </div>
    </div>

    <!-- Reports Tab -->
    <div v-else-if="activeTab === 'reports'">
      <div v-if="reports.length === 0" class="empty-wrap">
        <div class="empty-card">
          <h3>No reported posts</h3>
          <p class="muted">
            When users report posts, they will appear here for review.
          </p>
        </div>
      </div>

      <div v-else class="card-grid single-col">
        <article v-for="op in reports" :key="op.id" class="op-card report-card">
          <div class="op-card-top">
            <div class="left">
              <span class="badge">{{ prettyType(op.type) }}</span>
              <span class="report-pill">{{ op.reports_count }} report{{ op.reports_count > 1 ? 's' : '' }}</span>
            </div>
          </div>

          <h3 class="op-title">{{ op.title }}</h3>
          <p class="op-org">{{ op.org }}</p>
          <p class="op-creator">by @{{ op.creator_username }}</p>

          <p class="op-desc">{{ op.description }}</p>

          <div class="op-meta">
            <span>{{ op.location }}</span>
            <span>•</span>
            <span>Contact: {{ op.contact_email }}</span>
          </div>

          <!-- Reports list -->
          <div class="reports-box">
            <div class="reports-header">
              <span class="reports-icon">🚨</span>
              <span class="reports-label">Reports ({{ op.reports_count }})</span>
            </div>
            
            <div v-for="r in op.reports" :key="r.id" class="report-item">
              <div class="report-item-header">
                <span class="reporter">@{{ r.reporter_username }}</span>
                <span class="report-reason-chip">{{ r.reason }}</span>
                <span class="report-time">{{ shortDate(r.created_at) }}</span>
              </div>
              <p v-if="r.comment" class="report-comment">"{{ r.comment }}"</p>
            </div>
          </div>

          <div class="op-actions">
            <button 
              class="btn btn-outline small-btn" 
              :disabled="decidingId === op.id"
              @click="decideReport(op.id, 'dismiss')"
            >
              Dismiss Reports
            </button>
            <button 
              class="btn btn-danger btn-danger-solid small-btn" 
              :disabled="decidingId === op.id"
              @click="openTakeDownModal(op)"
            >
              Take Down
            </button>
          </div>
        </article>
      </div>
    </div>

    <!-- External Links Tab -->
    <div v-else-if="activeTab === 'links'">
      <div v-if="externalUrls.length === 0" class="empty-wrap">
        <div class="empty-card">
          <h3>No external links pending</h3>
          <p class="muted small-text">All external application URLs have been reviewed.</p>
        </div>
      </div>

      <div v-else class="card-grid">
        <article v-for="link in externalUrls" :key="link.id" class="op-card link-card">
          <div class="op-card-header">
            <span class="badge">{{ prettyType(link.type) }}</span>
            <span class="status-pill pending">Pending Review</span>
          </div>

          <h3 class="op-title">{{ link.title }}</h3>
          <p class="op-org">{{ link.org }}</p>

          <div class="link-url-box">
            <span class="link-label">External Application URL:</span>
            <span class="link-url-plain" :title="link.external_apply_url">{{ link.external_apply_url }}</span>
            <p class="link-warning-note muted small-text">
              User-submitted links are shown as text only. Use "Open (logged)" or "Copy URL (logged)" below; both actions are logged.
            </p>
            <div class="link-action-buttons">
              <button
                type="button"
                class="btn btn-outline small-btn"
                :disabled="decidingId === link.id || sandboxCopyId === link.id"
                @click="copyUrlLogged(link)"
              >
                {{ sandboxCopyId === link.id ? 'Copied' : 'Copy URL (logged)' }}
              </button>
              <button
                type="button"
                class="btn btn-outline small-btn open-sandbox-btn"
                :disabled="decidingId === link.id || sandboxOpeningId === link.id"
                @click="openSandboxModal(link)"
              >
                {{ sandboxOpeningId === link.id ? 'Opening…' : 'Open (logged)' }}
              </button>
            </div>
          </div>

          <p class="op-desc">{{ link.description }}</p>

          <div class="link-meta">
            <span>Posted by: <strong>{{ link.creator_username }}</strong></span>
            <span>•</span>
            <span>{{ formatDate(link.created_at) }}</span>
          </div>

          <div class="op-actions">
            <button 
              class="btn btn-outline small-btn" 
              :disabled="decidingId === link.id"
              @click="decideExternalUrl(link.id, false)"
            >
              Reject
            </button>
            <button 
              class="btn btn-primary small-btn" 
              :disabled="decidingId === link.id"
              @click="decideExternalUrl(link.id, true)"
            >
              Approve
            </button>
          </div>
        </article>
      </div>
    </div>

    <!-- Deny Appeal Modal -->
    <div v-if="isDenyModalOpen" class="modal-backdrop" @click.self="closeDenyModal">
      <div class="modal" style="max-width: 500px;">
        <h3>Deny Appeal</h3>
        <p class="muted small-text">
          Denying the appeal for "{{ denyOp?.title }}". The post will remain flagged.
        </p>

        <div class="form-row">
          <label>Response to user (optional)</label>
          <textarea 
            v-model="denyResponse"
            placeholder="Explain why the appeal was denied..."
            style="min-height: 80px;"
          ></textarea>
        </div>

        <div class="op-actions" style="margin-top: 12px;">
          <button class="btn btn-ghost small-btn" @click="closeDenyModal">Cancel</button>
          <button 
            class="btn btn-danger btn-danger-solid small-btn" 
            :disabled="decidingId === denyOp?.id"
            @click="confirmDeny"
          >
            Deny Appeal
          </button>
        </div>
      </div>
    </div>

    <!-- Open (logged) Modal – Safe External Link Review -->
    <div v-if="isSandboxModalOpen" class="modal-backdrop" @click.self="closeSandboxModal">
      <div class="modal" style="max-width: 540px;">
        <h3>Open link (logged)</h3>
        <p class="muted small-text">
          This link was submitted by a user and may be unsafe. Opens in a new tab with no referrer; use a VM or separate browser profile for full safety.
        </p>
        <p v-if="sandboxLinkInfo" class="sandbox-url-display">{{ sandboxLinkInfo.normalized_url }}</p>
        <div v-if="sandboxLinkInfo" class="sandbox-risk-row">
          <span class="risk-badge" :class="'risk-' + sandboxLinkInfo.risk_level">{{ sandboxLinkInfo.risk_level }}</span>
          <span v-if="sandboxLinkInfo.allowlisted" class="allowlist-tag">Allowlisted domain</span>
          <ul v-if="sandboxLinkInfo.reasons?.length" class="risk-reasons muted small-text">
            <li v-for="r in sandboxLinkInfo.reasons" :key="r">{{ r }}</li>
          </ul>
        </div>
        <p class="muted small-text" style="margin-top: 8px;">
          Opening or copying will be <strong>logged</strong> for audit. Do not enter credentials or sensitive data on the opened page.
        </p>
        <div v-if="sandboxLinkInfo && sandboxLinkInfo.risk_level === 'HIGH'" class="form-row">
          <label class="row-inline">
            <input type="checkbox" v-model="sandboxHighRiskAck" />
            I understand the risks and will open only in a safe environment
          </label>
        </div>
        <div class="op-actions" style="margin-top: 16px;">
          <button class="btn btn-ghost small-btn" type="button" @click="closeSandboxModal">Cancel</button>
          <button
            class="btn btn-outline small-btn"
            type="button"
            :disabled="sandboxOpeningId !== null || sandboxCopyingInModal"
            @click="copyUrlInModal"
          >
            {{ sandboxCopyingInModal ? 'Copied' : 'Copy URL (logged)' }}
          </button>
          <button
            class="btn btn-primary small-btn"
            type="button"
            :disabled="sandboxOpeningId !== null || (sandboxLinkInfo && sandboxLinkInfo.risk_level === 'HIGH' && !sandboxHighRiskAck)"
            @click="confirmOpenInSandbox"
          >
            {{ sandboxOpeningId ? 'Opening…' : 'Open (logged)' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Take Down Modal -->
    <div v-if="isTakeDownModalOpen" class="modal-backdrop" @click.self="closeTakeDownModal">
      <div class="modal" style="max-width: 500px;">
        <h3>Take Down Post</h3>
        <p class="muted small-text">
          Taking down "{{ takeDownOp?.title }}" will flag it and hide it from public view.
        </p>

        <div class="form-row">
          <label>Reason for takedown (optional)</label>
          <textarea 
            v-model="takeDownReason"
            placeholder="Explain why this post is being taken down..."
            style="min-height: 80px;"
          ></textarea>
        </div>

        <div class="op-actions" style="margin-top: 12px;">
          <button class="btn btn-ghost small-btn" @click="closeTakeDownModal">Cancel</button>
          <button 
            class="btn btn-danger btn-danger-solid small-btn" 
            :disabled="decidingId === takeDownOp?.id"
            @click="confirmTakeDown"
          >
            Take Down
          </button>
        </div>
      </div>
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

const { clearToken, setUser, user } = useAuth()
const year = new Date().getFullYear()

// User info from authStore
const userName = computed(() => user.value?.username || 'Moderator')
const userEmail = computed(() => user.value?.email || '')

/* nav */
const isMenuOpen = ref(false)
function toggleMenu() { isMenuOpen.value = !isMenuOpen.value }
function closeMenu() { isMenuOpen.value = false }

/* profile dropdown */
const isProfileOpen = ref(false)
function toggleProfileDropdown() { isProfileOpen.value = !isProfileOpen.value }
function closeProfileDropdown() { isProfileOpen.value = false }
function handleClickOutside(e) {
  if (isProfileOpen.value && !e.target.closest('.profile-dropdown-wrapper')) {
    isProfileOpen.value = false
  }
}

/* logout */
function onLogout() {
  clearToken()
  router.push('/')
}

/* state */
const pageError = ref('')
const loading = ref(false)
const activeTab = ref('appeals')

const appeals = ref([])
const reports = ref([])
const externalUrls = ref([])

const decidingId = ref(null)

/* deny modal */
const isDenyModalOpen = ref(false)
const denyOp = ref(null)
const denyResponse = ref('')

function openDenyModal(op) {
  denyOp.value = op
  denyResponse.value = ''
  isDenyModalOpen.value = true
}

function closeDenyModal() {
  isDenyModalOpen.value = false
  denyOp.value = null
  denyResponse.value = ''
}

/* open (logged) / copy (logged) – safe external link review */
const isSandboxModalOpen = ref(false)
const sandboxLink = ref(null)
const sandboxLinkInfo = ref(null)
const sandboxOpeningId = ref(null)
const sandboxCopyId = ref(null)
const sandboxCopyingInModal = ref(false)
const sandboxHighRiskAck = ref(false)

async function openSandboxModal(link) {
  sandboxLink.value = link
  sandboxLinkInfo.value = null
  sandboxOpeningId.value = null
  sandboxHighRiskAck.value = false
  isSandboxModalOpen.value = true
  try {
    const res = await AxiosInstance.get(`/moderation/external-urls/${link.id}/link-info`)
    sandboxLinkInfo.value = res.data
  } catch (e) {
    pageError.value =
      e?.response?.data?.detail?.message ||
      e?.response?.data?.detail ||
      e?.message ||
      'Could not load link info'
    closeSandboxModal()
  }
}

function closeSandboxModal() {
  isSandboxModalOpen.value = false
  sandboxLink.value = null
  sandboxLinkInfo.value = null
  sandboxOpeningId.value = null
  sandboxCopyingInModal.value = false
  sandboxHighRiskAck.value = false
}

async function confirmOpenInSandbox() {
  if (!sandboxLink.value?.id) return
  pageError.value = ''
  sandboxOpeningId.value = sandboxLink.value.id
  try {
    const res = await AxiosInstance.post(`/moderation/external-urls/${sandboxLink.value.id}/open-in-sandbox`, { action: 'open' })
    const url = res.data?.normalized_url
    if (url) {
      window.open(url, '_blank', 'noopener,noreferrer')
    }
    closeSandboxModal()
  } catch (e) {
    pageError.value =
      e?.response?.data?.detail?.message ||
      e?.response?.data?.detail ||
      e?.message ||
      'Could not open link'
  } finally {
    sandboxOpeningId.value = null
  }
}

async function copyUrlLogged(link) {
  if (!link?.id) return
  pageError.value = ''
  sandboxCopyId.value = link.id
  try {
    const res = await AxiosInstance.post(`/moderation/external-urls/${link.id}/open-in-sandbox`, { action: 'copy' })
    const url = res.data?.normalized_url
    if (url && typeof navigator !== 'undefined' && navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(url)
    }
  } catch (e) {
    pageError.value =
      e?.response?.data?.detail?.message ||
      e?.response?.data?.detail ||
      e?.message ||
      'Could not copy URL'
  } finally {
    sandboxCopyId.value = null
  }
}

async function copyUrlInModal() {
  if (!sandboxLink.value?.id) return
  sandboxCopyingInModal.value = true
  pageError.value = ''
  try {
    const res = await AxiosInstance.post(`/moderation/external-urls/${sandboxLink.value.id}/open-in-sandbox`, { action: 'copy' })
    const url = res.data?.normalized_url
    if (url && typeof navigator !== 'undefined' && navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(url)
    }
  } catch (e) {
    pageError.value =
      e?.response?.data?.detail?.message ||
      e?.response?.data?.detail ||
      e?.message ||
      'Could not copy URL'
  } finally {
    sandboxCopyingInModal.value = false
  }
}

/* take down modal */
const isTakeDownModalOpen = ref(false)
const takeDownOp = ref(null)
const takeDownReason = ref('')

function openTakeDownModal(op) {
  takeDownOp.value = op
  takeDownReason.value = ''
  isTakeDownModalOpen.value = true
}

function closeTakeDownModal() {
  isTakeDownModalOpen.value = false
  takeDownOp.value = null
  takeDownReason.value = ''
}

/* helpers */
function prettyType(t) {
  const s = String(t || '')
  return s ? s.charAt(0).toUpperCase() + s.slice(1) : ''
}

function parseUTCDate(value) {
  if (!value) return null
  // Ensure UTC timezone is recognized - append Z if no timezone info
  let dateStr = String(value)
  if (!dateStr.includes('Z') && !dateStr.includes('+') && !dateStr.includes('-', 10)) {
    dateStr += 'Z'
  }
  return new Date(dateStr)
}

function shortDate(value) {
  const d = parseUTCDate(value)
  if (!d) return ''
  return d.toLocaleDateString() + ' ' + d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

function formatDate(value) {
  const d = parseUTCDate(value)
  if (!d) return '—'
  return d.toLocaleString()
}

/* load data */
async function loadAppeals() {
  try {
    const res = await AxiosInstance.get('/moderation/appeals')
    appeals.value = res.data || []
  } catch (e) {
    if (e?.response?.status === 403) {
      router.push('/dashboard')
      return
    }
    throw e
  }
}

async function loadReports() {
  try {
    const res = await AxiosInstance.get('/moderation/reports')
    reports.value = res.data || []
  } catch (e) {
    if (e?.response?.status === 403) {
      router.push('/dashboard')
      return
    }
    throw e
  }
}

async function loadExternalUrls() {
  try {
    const res = await AxiosInstance.get('/moderation/external-urls')
    externalUrls.value = res.data || []
  } catch (e) {
    if (e?.response?.status === 403) {
      router.push('/dashboard')
      return
    }
    throw e
  }
}

async function loadAll() {
  pageError.value = ''
  loading.value = true
  try {
    await Promise.all([loadAppeals(), loadReports(), loadExternalUrls()])
  } catch (e) {
    pageError.value =
      e?.response?.data?.detail?.message ||
      e?.response?.data?.detail ||
      e?.message ||
      'Could not load moderation data'
  } finally {
    loading.value = false
  }
}

async function refresh() {
  closeMenu()
  await loadAll()
}

async function loadCurrentModerator() {
  try {
    const res = await AxiosInstance.get('/dashboard')
    const me = res.data?.me
    if (me) {
      setUser({ id: me.id, username: me.username, email: me.email })
    }
  } catch (e) {
    pageError.value =
      e?.response?.data?.detail?.message ||
      e?.response?.data?.detail ||
      e?.message ||
      'Could not load moderator profile'
  }
}

/* appeal actions */
async function decideAppeal(id, status, response = '') {
  if (!id) return
  pageError.value = ''
  decidingId.value = id
  try {
    await AxiosInstance.post(`/moderation/appeals/${id}/decide`, { status, response })
    appeals.value = appeals.value.filter((x) => x.id !== id)
    closeDenyModal()
  } catch (e) {
    pageError.value =
      e?.response?.data?.detail?.message ||
      e?.response?.data?.detail ||
      e?.message ||
      'Could not process appeal'
  } finally {
    decidingId.value = null
  }
}

async function confirmDeny() {
  if (!denyOp.value) return
  await decideAppeal(denyOp.value.id, 'denied', denyResponse.value)
}

/* report actions */
async function decideReport(id, action, reason = '') {
  if (!id) return
  pageError.value = ''
  decidingId.value = id
  try {
    await AxiosInstance.post(`/moderation/reports/${id}/decide`, { action, reason })
    reports.value = reports.value.filter((x) => x.id !== id)
    closeTakeDownModal()
  } catch (e) {
    pageError.value =
      e?.response?.data?.detail?.message ||
      e?.response?.data?.detail ||
      e?.message ||
      'Could not process report'
  } finally {
    decidingId.value = null
  }
}

async function confirmTakeDown() {
  if (!takeDownOp.value) return
  await decideReport(takeDownOp.value.id, 'take_down', takeDownReason.value)
}

/* external url actions */
async function decideExternalUrl(id, approved) {
  if (!id) return
  pageError.value = ''
  decidingId.value = id
  try {
    await AxiosInstance.post(`/moderation/external-urls/${id}/decide`, { approved })
    externalUrls.value = externalUrls.value.filter((x) => x.id !== id)
  } catch (e) {
    pageError.value =
      e?.response?.data?.detail?.message ||
      e?.response?.data?.detail ||
      e?.message ||
      'Could not process external URL'
  } finally {
    decidingId.value = null
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  loadCurrentModerator()
  loadAll()
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
:global(:root){
  --bg:#f3f4ff;
  --panel:#ffffff;
  --muted:#000000;
  --text:#0f172a;
  --accent:#2563eb;
  --accent-2:#14b8a6;
  --ring:rgba(37,99,235,.25);
  --card:#ffffff;
  --radius:18px;
  --shadow:0 18px 40px rgba(15,23,42,.08);
  --border:1px solid rgba(15,23,42,.06);
}

*{ box-sizing:border-box; }

.Moderator{
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

.brand-link{ display:flex; align-items:center; }
.brand{
  display:flex;
  align-items:center;
  gap:10px;
  font-weight:900;
  letter-spacing:.02em;
  font-size:18px;
}
.brand svg{ width:30px; height:30px; }
.brand-text{ display:flex; flex-direction:column; line-height:1.05; }
.brand-sub{
  font-size:11px;
  font-weight:800;
  color:rgba(15,23,42,.55);
  letter-spacing:.08em;
  text-transform:uppercase;
  margin-top:2px;
}

.nav-actions{
  display:flex;
  gap:12px;
  align-items:center;
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
.btn-outline{ background:#fff; }
.btn-primary{
  background:linear-gradient(90deg, var(--accent), var(--accent-2));
  color:#fff;
  border:none;
  font-weight:900;
}
.btn-ghost{
  background:transparent;
  border:1px solid rgba(148,163,184,.35);
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
  font-weight:800;
  cursor:pointer;
  transition:all .18s ease;
}
.btn-danger-solid{
  background:linear-gradient(90deg, #ef4444, #dc2626);
  color:#fff;
  border:none;
}

.avatar-btn{ background:transparent; border:none; cursor:pointer; padding:0; }
.avatar-circle{
  width:32px;
  height:32px;
  border-radius:999px;
  display:inline-flex;
  align-items:center;
  justify-content:center;
  font-size:12px;
  font-weight:900;
  background:linear-gradient(135deg, var(--accent), var(--accent-2));
  color:#fff;
}

.mod-avatar{
  background:linear-gradient(135deg, #dc2626, #ea580c);
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
.mod-profile-header{
  background:linear-gradient(135deg, rgba(220,38,38,.08), rgba(234,88,12,.05));
}
.profile-avatar{
  width:44px;
  height:44px;
  border-radius:999px;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:14px;
  font-weight:900;
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
.mod-badge{
  display:inline-block;
  margin-top:4px;
  padding:2px 8px;
  border-radius:999px;
  background:linear-gradient(90deg, #dc2626, #ea580c);
  color:#fff;
  font-size:10px;
  font-weight:800;
  text-transform:uppercase;
  letter-spacing:.05em;
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

.mobile-nav{
  display:none;
  flex-direction:column;
  gap:10px;
  background:rgba(248,250,252,.95);
  backdrop-filter: blur(12px);
  border-top:1px solid rgba(148,163,184,.25);
  padding:0 24px;
  max-height:0;
  overflow:hidden;
  transition:max-height 0.3s ease-in-out, padding 0.3s ease-in-out;
}
.mobile-nav.active{ max-height:200px; padding:16px 24px; }

.w-full{ width:100%; }

.section-header{
  max-width:1200px;
  margin:0 auto;
  padding:16px 24px 0;
  display:flex;
  flex-direction:column;
  gap:8px;
}
.title-row{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:12px;
}
.section-header h2{
  margin:0;
  font-size:20px;
  font-weight:900;
  letter-spacing:.01em;
}

.muted{ color:rgba(15,23,42,.65); }
.small-text{ font-size:12px; }

/* Tabs */
.tabs-row{
  display:flex;
  gap:8px;
  margin-top:12px;
}

.tab-btn{
  padding:10px 18px;
  border-radius:999px;
  border:1px solid rgba(148,163,184,.4);
  background:#fff;
  font-size:14px;
  font-weight:700;
  cursor:pointer;
  transition:all .15s ease;
  display:flex;
  align-items:center;
  gap:8px;
}

.tab-btn:hover{
  border-color:var(--accent);
}

.tab-btn.active{
  background:linear-gradient(90deg, var(--accent), var(--accent-2));
  color:#fff;
  border:none;
}

.tab-badge{
  padding:2px 8px;
  border-radius:999px;
  background:rgba(255,255,255,.25);
  font-size:12px;
  font-weight:900;
}

.tab-badge.danger{
  background:rgba(239,68,68,.15);
  color:#dc2626;
}

.tab-badge.warning{
  background:rgba(245,158,11,.15);
  color:#d97706;
}

.tab-btn.active .tab-badge{
  background:rgba(255,255,255,.25);
  color:#fff;
}

.tab-btn.active .tab-badge.danger{
  background:rgba(255,255,255,.25);
  color:#fff;
}

.card-grid{
  max-width:1200px;
  margin:0 auto;
  padding:14px 24px 40px;
  display:grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap:16px;
}

.card-grid.single-col{
  grid-template-columns: 1fr;
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
}

.report-card{
  max-width:800px;
}

.op-card-top{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:10px;
}
.left{ display:flex; gap:8px; align-items:center; flex-wrap:wrap; }
.right{ display:flex; gap:8px; align-items:center; }

.badge{
  font-size:11px;
  padding:4px 8px;
  border-radius:999px;
  background:rgba(37,99,235,.08);
  color:var(--accent);
  font-weight:800;
}
.flag-pill{
  font-size:11px;
  padding:4px 8px;
  border-radius:999px;
  background:rgba(239,68,68,.10);
  color:#b91c1c;
  border:1px solid rgba(239,68,68,.22);
  font-weight:900;
}
.report-pill{
  font-size:11px;
  padding:4px 8px;
  border-radius:999px;
  background:rgba(245,158,11,.10);
  color:#b45309;
  border:1px solid rgba(245,158,11,.22);
  font-weight:900;
}
.time-pill{
  font-size:11px;
  padding:4px 8px;
  border-radius:999px;
  background:rgba(15,23,42,.04);
  color:rgba(15,23,42,.70);
  border:1px solid rgba(15,23,42,.08);
  font-weight:800;
}

.op-title{
  font-size:16px;
  font-weight:900;
  margin:0;
}
.op-org{
  margin:0;
  font-size:13px;
  color:rgba(15,23,42,.7);
  font-weight:700;
}
.op-creator{
  margin:0;
  font-size:12px;
  color:rgba(15,23,42,.55);
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
.op-desc{
  margin:0;
  font-size:13px;
  color:rgba(15,23,42,.78);
  line-height:1.5;
  display:-webkit-box;
  -webkit-line-clamp:3;
  -webkit-box-orient: vertical;
  overflow:hidden;
}

.mod-box{
  border:1px solid rgba(148,163,184,.25);
  background:rgba(248,250,252,.90);
  border-radius:14px;
  padding:10px 12px;
}
.mod-row{
  display:grid;
  grid-template-columns: 96px 1fr;
  gap:10px;
  align-items:start;
  margin:6px 0;
}
.mod-k{
  font-size:11px;
  font-weight:900;
  letter-spacing:.08em;
  text-transform:uppercase;
  color:rgba(15,23,42,.55);
}
.mod-v{
  font-size:12px;
  color:rgba(15,23,42,.78);
  word-break:break-word;
}
.tag-row{
  display:flex;
  gap:6px;
  flex-wrap:wrap;
  margin-top:2px;
}
.chip{
  font-size:11px;
  padding:4px 8px;
  border-radius:999px;
  background:rgba(37,99,235,.08);
  color:var(--accent);
  font-weight:800;
  border:1px solid rgba(37,99,235,.18);
}
.danger-chip{
  background:rgba(239,68,68,.10);
  color:#b91c1c;
  border:1px solid rgba(239,68,68,.22);
}

/* Appeal box */
.appeal-box{
  border:1px solid rgba(37,99,235,.25);
  background:rgba(37,99,235,.04);
  border-radius:14px;
  padding:12px;
}
.appeal-header{
  display:flex;
  align-items:center;
  gap:8px;
  margin-bottom:8px;
}
.appeal-icon{ font-size:16px; }
.appeal-label{
  font-size:12px;
  font-weight:900;
  text-transform:uppercase;
  letter-spacing:.08em;
  color:var(--accent);
}
.appeal-message{
  margin:0;
  font-size:13px;
  color:rgba(15,23,42,.85);
  font-style:italic;
  line-height:1.5;
}

/* Reports box */
.reports-box{
  border:1px solid rgba(245,158,11,.25);
  background:rgba(245,158,11,.04);
  border-radius:14px;
  padding:12px;
}
.reports-header{
  display:flex;
  align-items:center;
  gap:8px;
  margin-bottom:10px;
}
.reports-icon{ font-size:16px; }
.reports-label{
  font-size:12px;
  font-weight:900;
  text-transform:uppercase;
  letter-spacing:.08em;
  color:#b45309;
}

.report-item{
  padding:10px;
  background:rgba(255,255,255,.7);
  border-radius:10px;
  margin-bottom:8px;
  border:1px solid rgba(148,163,184,.15);
}
.report-item:last-child{ margin-bottom:0; }

.report-item-header{
  display:flex;
  align-items:center;
  gap:8px;
  flex-wrap:wrap;
  margin-bottom:4px;
}
.reporter{
  font-size:12px;
  font-weight:800;
  color:rgba(15,23,42,.8);
}
.report-reason-chip{
  font-size:10px;
  padding:2px 8px;
  border-radius:999px;
  background:rgba(239,68,68,.10);
  color:#b91c1c;
  font-weight:800;
  text-transform:uppercase;
}
.report-time{
  font-size:11px;
  color:rgba(15,23,42,.5);
  margin-left:auto;
}
.report-comment{
  margin:4px 0 0;
  font-size:12px;
  color:rgba(15,23,42,.7);
  font-style:italic;
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

/* empty */
.empty-wrap{
  max-width:1200px;
  margin:0 auto;
  padding:14px 24px 40px;
}
.empty-card{
  background:#fff;
  border-radius:18px;
  border:1px solid rgba(148,163,184,.18);
  box-shadow:var(--shadow);
  padding:18px;
}

/* modal */
.modal-backdrop{
  position:fixed;
  inset:0;
  background:rgba(15,23,42,.44);
  display:flex;
  align-items:center;
  justify-content:center;
  padding:18px;
  z-index:2000;
}
.modal{
  width:100%;
  background:#fff;
  border-radius:18px;
  border:1px solid rgba(148,163,184,.25);
  box-shadow:0 22px 60px rgba(15,23,42,.25);
  padding:16px;
}

.form-row{
  margin:12px 0;
}
.form-row label{
  display:block;
  font-size:12px;
  font-weight:700;
  margin-bottom:6px;
  color:rgba(15,23,42,.7);
}
.form-row textarea{
  width:100%;
  padding:10px 12px;
  border-radius:10px;
  border:1px solid rgba(148,163,184,.4);
  font-size:13px;
  font-family:inherit;
  resize:vertical;
}
.form-row textarea:focus{
  outline:none;
  border-color:var(--accent);
  box-shadow:0 0 0 2px var(--ring);
}

/* External Links tab */
.status-pill{
  padding:4px 10px;
  border-radius:999px;
  font-size:11px;
  font-weight:700;
  text-transform:uppercase;
  letter-spacing:.03em;
}
.status-pill.pending{
  background:rgba(245,158,11,.15);
  color:#d97706;
}

.link-url-box{
  margin:12px 0;
  padding:12px;
  border-radius:10px;
  background:rgba(37,99,235,.05);
  border:1px solid rgba(37,99,235,.15);
}
.link-label{
  display:block;
  font-size:11px;
  font-weight:700;
  color:var(--muted);
  text-transform:uppercase;
  letter-spacing:.03em;
  margin-bottom:6px;
}
.link-url{
  display:block;
  font-size:13px;
  color:var(--accent);
  word-break:break-all;
  text-decoration:none;
}
.link-url:hover{
  text-decoration:underline;
}
.link-url-plain{
  display:block;
  font-size:13px;
  color:var(--text);
  word-break:break-all;
  cursor:text;
  user-select:text;
}
.link-warning-note{
  margin:8px 0 10px;
  font-size:11px;
}
.link-action-buttons{
  display:flex;
  flex-wrap:wrap;
  gap:8px;
  margin-top:8px;
}
.open-sandbox-btn{
  margin-top:0;
}
.sandbox-url-display{
  font-size:12px;
  word-break:break-all;
  padding:8px 10px;
  background:rgba(15,23,42,.06);
  border-radius:8px;
  margin:8px 0 0;
}
.sandbox-risk-row{
  margin-top:10px;
  display:flex;
  flex-wrap:wrap;
  align-items:center;
  gap:8px;
}
.risk-badge{
  font-size:11px;
  font-weight:700;
  text-transform:uppercase;
  padding:4px 8px;
  border-radius:6px;
}
.risk-LOW{
  background:rgba(34,197,94,.15);
  color:#15803d;
}
.risk-MEDIUM{
  background:rgba(245,158,11,.15);
  color:#b45309;
}
.risk-HIGH{
  background:rgba(239,68,68,.15);
  color:#b91c1c;
}
.allowlist-tag{
  font-size:11px;
  color:var(--accent);
  font-weight:600;
}
.risk-reasons{
  width:100%;
  margin:4px 0 0;
  padding-left:18px;
}
.risk-reasons li{
  margin:2px 0;
}
.form-row .row-inline{
  display:flex;
  align-items:center;
  gap:8px;
  font-weight:500;
  cursor:pointer;
}
.form-row .row-inline input[type="checkbox"]{
  width:auto;
  margin:0;
}
.link-meta{
  display:flex;
  gap:6px;
  align-items:center;
  flex-wrap:wrap;
  font-size:12px;
  color:var(--muted);
  margin:10px 0;
}
.link-meta strong{
  color:var(--text);
}

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

/* error popup */
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
</style>
