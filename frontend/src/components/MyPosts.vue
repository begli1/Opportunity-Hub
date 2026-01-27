<template>
  <div class="MyPosts">
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
            placeholder="Search your posts"
            v-model="searchQuery"
            @input="onSearchInput"
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
        <button class="btn-danger btn-danger-solid btn-post w-full" @click="onLogout">
          Logout
        </button>
      </nav>
    </header>

    <div v-if="pageError" class="error-popup">{{ pageError }}</div>

    <div class="section-header">
      <h2>Your Posts</h2>
      <span class="muted small-text">Manage your opportunities and applicants.</span>
    </div>

    <div v-if="loading" class="muted small-text" style="padding: 0 20px;">Loading…</div>

    <div v-else class="card-grid">
      <article v-for="op in filteredMyPosts" :key="op.id" class="op-card">
        <div class="op-card-header">
          <span class="badge">{{ prettyType(op.type) }}</span>
          <span class="count-pill">{{ op.applications_count || 0 }} applicants</span>
        </div>
                <!-- Moderation status -->
        <div v-if="op.is_flagged" class="flagged-box">
          <p class="flagged-title">⚠ Pending moderator review</p>
          <p class="flagged-text" v-if="op.flagged_reason">{{ op.flagged_reason }}</p>

          <p v-if="op.flagged_categories && op.flagged_categories.length" class="flagged-text">
            Flagged for:
            <span v-for="c in op.flagged_categories" :key="c" class="flag-chip">{{ c }}</span>
          </p>

          <p class="flagged-text" v-if="op.flagged_at">
            Flagged at: {{ formatDate(op.flagged_at) }}
          </p>

          <!-- Appeal status -->
          <div v-if="op.appeal_status" class="appeal-status-box">
            <p class="appeal-status-title">
              Appeal Status: 
              <span :class="'appeal-' + op.appeal_status">{{ prettyAppealStatus(op.appeal_status) }}</span>
            </p>
            <p class="flagged-text" v-if="op.appeal_message">
              Your message: "{{ op.appeal_message }}"
            </p>
            <p class="flagged-text" v-if="op.appeal_response">
              Moderator response: "{{ op.appeal_response }}"
            </p>
            <p class="flagged-text" v-if="op.appeal_decided_at">
              Decided at: {{ formatDate(op.appeal_decided_at) }}
            </p>
          </div>

          <!-- Appeal button (only if no appeal submitted yet) -->
          <div v-if="!op.appeal_status" class="appeal-actions">
            <button class="btn btn-primary small-btn" type="button" @click="openAppeal(op)">
              Appeal Decision
            </button>
          </div>
        </div>

        <!-- External URL pending approval notice -->
        <div v-if="op.allow_external_apply && op.external_apply_url && op.external_url_approved === null" class="pending-url-box">
          <p class="pending-url-title">🔗 External link pending review</p>
          <p class="pending-url-text">Your external application URL is awaiting moderator approval. Your post won't be visible to others until approved.</p>
        </div>

        <h3 class="op-title">{{ op.title }}</h3>
        <p class="op-org">{{ op.org }}</p>

        <p class="op-desc">{{ op.description }}</p>

        <div class="op-meta">
          <span>{{ op.location }}</span>
          <span>•</span>
          <span>Deadline: {{ formatDeadline(op) }}</span>
          <span>•</span>
          <span v-if="op.allow_apply">Open</span>
          <span v-else>Closed</span>
        </div>

        <div class="op-tags">
          <span v-for="tag in (op.tags || [])" :key="tag" class="chip">{{ tag }}</span>
        </div>

        <div class="op-actions">
          <button class="btn btn-outline small-btn" @click="openApplicants(op)">
            Manage applicants
          </button>

          <button class="btn btn-outline small-btn" @click="openEdit(op)">
            Edit
          </button>

          <button class="btn-danger btn-danger-solid small-btn" @click="deletePost(op.id)">
            Delete
          </button>
        </div>
      </article>
    </div>

    <!-- Applicants modal -->
    <div v-if="isApplicantsOpen" class="modal-backdrop" @click.self="closeApplicants">


      <div class="modal" style="max-width: 760px;">
        
        <h3>Applicants • {{ selectedOpp?.title }}</h3>
        <p class="muted small-text">{{ selectedOpp?.org }}</p>

        <div v-if="applicantsLoading" class="muted">Loading applicants…</div>
        <p v-if="applicantsError" class="error-popup">{{ applicantsError }}</p>

        <div v-if="!applicantsLoading && applicants.length === 0" class="muted">
          No applications yet.
        </div>

        <div v-for="a in applicants" :key="a.id" class="saved-item" style="margin-top: 12px;">
          <div style="flex: 1;">
            <p class="saved-title">{{ a.full_name }} • {{ a.email }}</p>
            <p class="muted small-text">Applied: {{ formatDate(a.created_at) }}</p>
            <p class="muted" style="margin-top: 6px;">{{ a.message || '—' }}</p>

            <p class="muted small-text" style="margin-top: 8px;">
              Status: <strong>{{ prettyStatus(a.status) }}</strong>
              <span v-if="a.decision_reason"> • Reason: {{ a.decision_reason }}</span>
            </p>

            <div v-if="a.status === 'pending'" style="margin-top: 10px; display:flex; gap: 8px; align-items:center;">
              <button class="btn btn-primary small-btn" :disabled="decidingId === a.id" @click="decide(a, 'accepted')">
                Accept
              </button>

              <button class="btn btn-outline small-btn" :disabled="decidingId === a.id" @click="startReject(a.id)">
                Reject
              </button>
            </div>

            <div v-if="rejectingId === a.id" style="margin-top: 10px;">
              <textarea
                v-model="rejectReason"
                placeholder="Optional rejection reason..."
                style="width: 100%; min-height: 70px;"
              ></textarea>
              <div style="margin-top: 8px; display:flex; gap: 8px;">
                <button
                  class="btn btn-danger btn-danger-solid small-btn"
                  :disabled="decidingId === a.id"
                  @click="decide(a, 'rejected', rejectReason)"
                >
                  Confirm reject
                </button>
                <button class="btn btn-ghost small-btn" :disabled="decidingId === a.id" @click="cancelReject">
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="op-actions" style="margin-top: 16px;">
          <button class="btn btn-ghost small-btn" @click="closeApplicants">Close</button>
        </div>
      </div>
    </div>

    <!-- Edit post modal -->
    <div v-if="isEditOpen" class="modal-backdrop" @click.self="closeEdit">
      <div class="modal" style="max-width: 760px;">
        <h3>Edit post</h3>
        <p class="muted small-text">{{ editForm.title || '—' }}</p>

        <div v-if="editError" class="error-popup">{{ editError }}</div>

        <div class="form-row">
          <label>Type</label>
          <select v-model="editForm.type">
            <option value="internship">Internship</option>
            <option value="club">Club</option>
            <option value="volunteering">Volunteering</option>
            <option value="tutor">Tutor</option>
          </select>
        </div>

        <div class="form-row">
          <label>Title</label>
          <input v-model="editForm.title" />
        </div>

        <div class="form-row">
          <label>Organization</label>
          <input v-model="editForm.org" />
        </div>

        <div class="form-row">
          <label>Description</label>
          <textarea v-model="editForm.description" style="min-height: 110px;"></textarea>
        </div>

        <div class="form-row">
          <label>Location</label>
          <input v-model="editForm.location" />
        </div>

        <div class="form-row">
          <label>Deadline (date)</label>
          <input type="date" v-model="editDeadlineDate" />
          <p class="muted small-text" style="margin-top: 6px;">
            Optional. If you prefer “Rolling” or “ASAP”, leave date empty and use deadline text.
          </p>
        </div>

        <div class="form-row">
          <label>Deadline text</label>
          <input v-model="editForm.deadline_text" placeholder="Rolling / ASAP / March 1…" />
        </div>

        <div class="form-row">
          <label>Tags (comma separated)</label>
          <input v-model="editTags" placeholder="python, cybersecurity, beginner-friendly" />
        </div>

        <div class="form-row" style="display:flex; gap: 12px; align-items:center;">
          <input id="allowApply" type="checkbox" v-model="editForm.allow_apply" />
          <label for="allowApply" style="margin: 0;">Allow applications</label>
        </div>

        <div class="form-row" style="display:flex; gap: 12px; align-items:center;">
          <input id="allowExternal" type="checkbox" v-model="editForm.allow_external_apply" />
          <label for="allowExternal" style="margin: 0;">Allow external apply link</label>
        </div>

        <div class="form-row" v-if="editForm.allow_external_apply">
          <label>External apply URL</label>
          <input v-model="editForm.external_apply_url" placeholder="https://…" />
        </div>

        <div class="op-actions" style="margin-top: 12px;">
          <button class="btn btn-ghost small-btn" :disabled="savingEdit" @click="closeEdit">Cancel</button>
          <button class="btn btn-primary small-btn" :disabled="savingEdit" @click="saveEdit">
            Save changes
          </button>
        </div>
      </div>
    </div>

    <!-- Appeal modal -->
    <div v-if="isAppealOpen" class="modal-backdrop" @click.self="closeAppeal">
      <div class="modal" style="max-width: 600px;">
        <h3>Appeal Decision</h3>
        <p class="muted small-text">
          Explain why your post "{{ appealOpp?.title }}" should be approved.
        </p>

        <div v-if="appealError" class="error-popup" style="position: static; margin: 12px 0;">
          {{ appealError }}
        </div>

        <div class="form-row">
          <label>Your appeal message</label>
          <textarea 
            v-model="appealMessage"
            placeholder="Please explain why this post should be approved. Be specific about why you believe the flag was in error..."
            style="min-height: 120px;"
          ></textarea>
          <p class="muted small-text">Minimum 10 characters. A moderator will review your appeal.</p>
        </div>

        <div class="op-actions" style="margin-top: 12px;">
          <button class="btn btn-ghost small-btn" :disabled="submittingAppeal" @click="closeAppeal">
            Cancel
          </button>
          <button 
            class="btn btn-primary small-btn" 
            :disabled="submittingAppeal || appealMessage.trim().length < 10" 
            @click="submitAppeal"
          >
            {{ submittingAppeal ? 'Submitting…' : 'Submit Appeal' }}
          </button>
        </div>
      </div>
    </div>

    <footer>
      <div class="container">
        <div class="footer-inner">
          <p class="muted">© <span>{{ year }}</span> Opportunity Hub. Built by students, for students.</p>
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

/* ========= nav ========= */
const isMenuOpen = ref(false)
function toggleMenu() { isMenuOpen.value = !isMenuOpen.value }
function closeMenu() { isMenuOpen.value = false }

/* ========= profile dropdown ========= */
const isProfileOpen = ref(false)
function toggleProfileDropdown() { isProfileOpen.value = !isProfileOpen.value }
function closeProfileDropdown() { isProfileOpen.value = false }
function handleClickOutside(e) {
  if (isProfileOpen.value && !e.target.closest('.profile-dropdown-wrapper')) {
    isProfileOpen.value = false
  }
}

/* ========= logout ========= */
function onLogout() {
  clearToken()
  router.push('/')
}

function goContact(op) {
  // simplest: send them to your contact page/section
  // change this to whatever route you have
  router.push('/dashboard') // or '/contact' if you have one
}


/* ========= state ========= */
const pageError = ref('')
const loading = ref(false)
const myPosts = ref([])

/* ========= search ========= */
const searchQuery = ref('')
let searchTimer = null

function onSearchInput() {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {}, 150)
}

const filteredMyPosts = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return myPosts.value
  return myPosts.value.filter((x) => {
    return (
      String(x.title || '').toLowerCase().includes(q) ||
      String(x.org || '').toLowerCase().includes(q) ||
      String(x.type || '').toLowerCase().includes(q)
    )
  })
})

function prettyType(t) {
  if (!t) return ''
  const s = String(t)
  return s.charAt(0).toUpperCase() + s.slice(1)
}

function prettyStatus(s) {
  const t = String(s || 'pending')
  return t.charAt(0).toUpperCase() + t.slice(1)
}

function prettyAppealStatus(s) {
  if (s === 'pending') return '⏳ Pending Review'
  if (s === 'approved') return '✅ Approved'
  if (s === 'denied') return '❌ Denied'
  return s ? s.charAt(0).toUpperCase() + s.slice(1) : ''
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

function parseTags(str) {
  return String(str || '')
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean)
}

/* ========= load posts ========= */
async function loadMyPosts() {
  pageError.value = ''
  loading.value = true
  try {
    const res = await AxiosInstance.get('/users/me/opportunities')
    myPosts.value = (res.data || []).map((op) => ({
      ...op,
      type: prettyType(op.type),
    }))
  } catch (e) {
    pageError.value =
      e?.response?.data?.detail?.message ||
      e?.response?.data?.detail ||
      e?.message ||
      'Could not load your posts'
  } finally {
    loading.value = false
  }
}

async function deletePost(id) {
  pageError.value = ''
  try {
    await AxiosInstance.delete(`/opportunities/${id}`)
    myPosts.value = myPosts.value.filter((x) => x.id !== id)
  } catch (e) {
    pageError.value = e?.response?.data?.detail?.message || 'Could not delete post'
  }
}

/* ========= Applicants modal ========= */
const isApplicantsOpen = ref(false)
const selectedOpp = ref(null)
const applicants = ref([])
const applicantsLoading = ref(false)
const applicantsError = ref('')
const decidingId = ref(null)
const rejectingId = ref(null)
const rejectReason = ref('')

async function openApplicants(op) {
  selectedOpp.value = op
  isApplicantsOpen.value = true
  applicantsError.value = ''
  applicants.value = []
  decidingId.value = null
  rejectingId.value = null
  rejectReason.value = ''

  applicantsLoading.value = true
  try {
    const res = await AxiosInstance.get(`/opportunities/${op.id}/applications`)
    applicants.value = res.data || []
  } catch (e) {
    applicantsError.value =
      e?.response?.data?.detail?.message ||
      e?.response?.data?.detail ||
      e?.message ||
      'Could not load applicants'
  } finally {
    applicantsLoading.value = false
  }
}

function closeApplicants() {
  isApplicantsOpen.value = false
  selectedOpp.value = null
  applicants.value = []
  applicantsError.value = ''
  decidingId.value = null
  rejectingId.value = null
  rejectReason.value = ''
}

function startReject(appId) {
  rejectingId.value = appId
  rejectReason.value = ''
}
function cancelReject() {
  rejectingId.value = null
  rejectReason.value = ''
}

async function decide(app, status, reason = '') {
  if (!selectedOpp.value) return
  applicantsError.value = ''
  decidingId.value = app.id
  try {
    const payload = { status }
    if (status === 'rejected') payload.reason = reason || ''

    const res = await AxiosInstance.patch(
      `/opportunities/${selectedOpp.value.id}/applications/${app.id}`,
      payload
    )

    applicants.value = applicants.value.map((x) => (x.id === app.id ? res.data : x))
    cancelReject()
    await loadMyPosts()
  } catch (e) {
    applicantsError.value =
      e?.response?.data?.detail?.message ||
      e?.response?.data?.detail ||
      e?.message ||
      'Could not update application'
  } finally {
    decidingId.value = null
  }
}

/* ========= Edit modal ========= */
const isEditOpen = ref(false)
const savingEdit = ref(false)
const editError = ref('')
const editOppId = ref(null)

const editForm = ref({
  type: 'internship',
  title: '',
  org: '',
  description: '',
  location: '',
  deadline_text: '',
  allow_apply: true,
  allow_external_apply: false,
  external_apply_url: '',
})

const editTags = ref('')
const editDeadlineDate = ref('') // yyyy-mm-dd

function openEdit(op) {
  editError.value = ''
  editOppId.value = op.id

  editForm.value = {
    type: (op.type || 'internship').toLowerCase(),
    title: op.title || '',
    org: op.org || '',
    description: op.description || '',
    location: op.location || '',
    deadline_text: op.deadline_text || '',
    allow_apply: Boolean(op.allow_apply),
    allow_external_apply: Boolean(op.allow_external_apply),
    external_apply_url: op.external_apply_url || '',
  }

  editTags.value = (op.tags || []).join(', ')

  // convert deadline_at -> yyyy-mm-dd
  if (op.deadline_at) {
    const d = new Date(op.deadline_at)
    const yyyy = d.getFullYear()
    const mm = String(d.getMonth() + 1).padStart(2, '0')
    const dd = String(d.getDate()).padStart(2, '0')
    editDeadlineDate.value = `${yyyy}-${mm}-${dd}`
  } else {
    editDeadlineDate.value = ''
  }

  isEditOpen.value = true
}

function closeEdit() {
  isEditOpen.value = false
  editOppId.value = null
  editError.value = ''
  savingEdit.value = false
}

async function saveEdit() {
  if (!editOppId.value) return
  editError.value = ''
  savingEdit.value = true

  try {
    // deadline_at: send ISO string or null/omit
    let deadline_at = null
    if (editDeadlineDate.value) {
      // store as UTC midnight to avoid weird offsets
      deadline_at = new Date(`${editDeadlineDate.value}T00:00:00.000Z`).toISOString()
    }

    const payload = {
      type: editForm.value.type,
      title: editForm.value.title,
      org: editForm.value.org,
      description: editForm.value.description,
      location: editForm.value.location,
      deadline_at: deadline_at, // can be null (backend should allow Optional)
      deadline_text: editForm.value.deadline_text || '',
      tags: parseTags(editTags.value),
      allow_apply: Boolean(editForm.value.allow_apply),
      allow_external_apply: Boolean(editForm.value.allow_external_apply),
      external_apply_url: editForm.value.allow_external_apply
        ? (editForm.value.external_apply_url || '')
        : '',
    }

    await AxiosInstance.patch(`/opportunities/${editOppId.value}`, payload)

    // Reload from server so we get moderation fields + correct state
    await loadMyPosts()

    closeEdit()

  } catch (e) {
    editError.value =
      e?.response?.data?.detail?.message ||
      e?.response?.data?.detail ||
      e?.message ||
      'Could not save changes'
  } finally {
    savingEdit.value = false
  }
}

/* ========= Appeal modal ========= */
const isAppealOpen = ref(false)
const appealOpp = ref(null)
const appealMessage = ref('')
const appealError = ref('')
const submittingAppeal = ref(false)

function openAppeal(op) {
  appealOpp.value = op
  appealMessage.value = ''
  appealError.value = ''
  isAppealOpen.value = true
}

function closeAppeal() {
  isAppealOpen.value = false
  appealOpp.value = null
  appealMessage.value = ''
  appealError.value = ''
  submittingAppeal.value = false
}

async function submitAppeal() {
  if (!appealOpp.value || appealMessage.value.trim().length < 10) return
  appealError.value = ''
  submittingAppeal.value = true

  try {
    await AxiosInstance.post(`/opportunities/${appealOpp.value.id}/appeal`, {
      message: appealMessage.value.trim(),
    })

    // Reload to show updated appeal status
    await loadMyPosts()
    closeAppeal()

  } catch (e) {
    appealError.value =
      e?.response?.data?.detail?.message ||
      e?.response?.data?.detail ||
      e?.message ||
      'Could not submit appeal'
  } finally {
    submittingAppeal.value = false
  }
}

// Auto-refresh when window regains focus (to catch moderator approvals)
function handleVisibilityChange() {
  if (document.visibilityState === 'visible') {
    loadMyPosts()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('visibilitychange', handleVisibilityChange)
  loadMyPosts()
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('visibilitychange', handleVisibilityChange)
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
  --card-2:#f9fafb;
  --radius:18px;
  --shadow:0 18px 40px rgba(15,23,42,.08);
  --border:1px solid rgba(15,23,42,.06);
}

*{ box-sizing:border-box; }

.MyPosts{
  min-height:100vh;
  background:
    radial-gradient(900px 500px at 10% -10%, rgba(59,130,246,.20), transparent 60%),
    radial-gradient(900px 600px at 90% 110%, rgba(45,212,191,.18), transparent 60%),
    var(--bg);
  color:var(--text);
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, "Helvetica Neue", Arial;
}

a{ color:inherit; text-decoration:none; }

/* ===== NAVBAR (kept as-is, only what it needs) ===== */

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

.w-full{ width:100%; }

/* ===== PAGE CONTENT (presentable) ===== */

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



.small-text{
  font-size:12px;
}

/* 2 cards per row on desktop, 1 on mobile */
.card-grid{
  max-width:1200px;
  margin:0 auto;
  padding:14px 24px 40px;
  display:grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
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
  gap:10px;
  min-height: 220px;
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

.icon-btn{
  background:transparent;
  border:none;
  cursor:pointer;
  font-size:16px;
  line-height:1;
  padding:6px 8px;
  border-radius:10px;
}

.icon-btn:hover{
  background:rgba(15,23,42,.05);
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

.op-desc{
  margin:0;
  font-size:13px;
  color:rgba(15,23,42,.85);
  display:-webkit-box;
  -webkit-line-clamp:3;
  -webkit-box-orient:vertical;
  overflow:hidden;
}

.op-meta{
  font-size:12px;
  color:rgba(15,23,42,.65);
  display:flex;
  gap:6px;
  align-items:center;
  flex-wrap:wrap;
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
  white-space:nowrap;
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
.flagged-box {
  margin: 10px 0 12px;
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid rgba(239, 68, 68, 0.35);
  background: rgba(239, 68, 68, 0.06);
}

.pending-url-box {
  margin: 10px 0 12px;
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid rgba(234, 179, 8, 0.35);
  background: rgba(234, 179, 8, 0.06);
}

.pending-url-title {
  font-weight: 700;
  margin: 0 0 6px;
  color: #ca8a04;
}

.pending-url-text {
  margin: 0;
  font-size: 0.85rem;
  color: var(--muted);
}

.flagged-title {
  font-weight: 700;
  margin: 0 0 6px;
}

.flagged-text {
  margin: 0 0 6px;
  font-size: 0.92rem;
  opacity: 0.9;
}

.flag-chip {
  display: inline-block;
  margin-left: 6px;
  padding: 2px 8px;
  border-radius: 999px;
  border: 1px solid rgba(239, 68, 68, 0.35);
  font-size: 0.78rem;
}

.appeal-status-box {
  margin-top: 10px;
  padding: 8px 10px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(148, 163, 184, 0.25);
}

.appeal-status-title {
  font-weight: 700;
  margin: 0 0 6px;
  font-size: 0.9rem;
}

.appeal-pending { color: #d97706; }
.appeal-approved { color: #16a34a; }
.appeal-denied { color: #dc2626; }

.appeal-actions {
  margin-top: 10px;
  display: flex;
  gap: 8px;
}

/* ===== RESPONSIVE ===== */

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
.taglist{
  display:flex;
  gap:8px;
  flex-wrap:wrap;
}

.taglist-chips{
  margin:10px 0 14px;
}




/* Error Popup */
.error-popup {
  position: fixed;
  bottom: 24px;
  right: 24px;

  max-width: 360px;
  padding: 14px 18px;

  background: #fee2e2;          /* soft red */
  color: #991b1b;               /* dark red text */
  border: 1px solid #fecaca;
  border-radius: 12px;

  font-size: 14px;
  line-height: 1.4;

  box-shadow:
    0 10px 25px rgba(0, 0, 0, 0.12);

  z-index: 9999;

  animation: slide-in 0.25s ease-out;
}

@keyframes slide-in {
  from {
    transform: translateY(12px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* tiny extras; safe even if you already have these */
.status-pill {
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 12px;
  border: 1px solid rgba(0,0,0,0.08);
}
.status-pill[data-status="pending"] { opacity: 0.8; }
.status-pill[data-status="accepted"] { font-weight: 700; }
.status-pill[data-status="rejected"] { font-weight: 700; }

.stack { display: grid; gap: 12px; margin-top: 10px; }
.app-card { border: 1px solid rgba(0,0,0,0.08); border-radius: 14px; padding: 12px; }
.app-top { display:flex; justify-content:space-between; gap: 12px; align-items:flex-start; }
.app-msg { white-space: pre-wrap; }


/* =========================
   MODALS (Applicants + Edit)
   ========================= */

/* Backdrop */
.modal-backdrop{
  position: fixed;
  inset: 0;
  background: rgba(2, 6, 23, .55);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 18px;
  z-index: 9990;
  animation: modal-fade .14s ease-out;
}

/* Modal container */
.modal{
  width: 100%;
  background: rgba(255,255,255,.94);
  border: 1px solid rgba(148,163,184,.25);
  border-radius: 18px;
  box-shadow: 0 28px 70px rgba(15,23,42,.25);
  padding: 18px 18px 16px;

  /* height + scroll handling */
  max-height: calc(100vh - 36px);
  overflow: hidden;

  animation: modal-pop .16s ease-out;
}

/* Make modal content scrollable when long */
.modal > *{
  max-width: 100%;
}

.modal h3{
  margin: 0 0 6px;
  font-size: 18px;
  font-weight: 900;
  letter-spacing: .01em;
}

.modal .muted{
  color: rgba(15,23,42,.65);
}

.modal .small-text{
  color: rgba(15,23,42,.60);
}

/* If you want a scroll area inside (no markup changes needed):
   the modal will scroll itself when content gets long */
.modal{
  overflow-y: auto;
}

/* Tighten the action row inside modal */
.modal .op-actions{
  position: sticky;
  bottom: -1px;
  background: rgba(255,255,255,.92);
  backdrop-filter: blur(8px);
  padding-top: 12px;
  border-top: 1px solid rgba(148,163,184,.18);
}

/* Form rows inside modal */
.form-row{
  display: grid;
  gap: 6px;
  margin-top: 12px;
}

.form-row label{
  font-size: 12px;
  font-weight: 800;
  color: rgba(15,23,42,.75);
}

.form-row input,
.form-row select,
.modal textarea{
  width: 100%;
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid rgba(148,163,184,.55);
  outline: none;
  font-size: 13px;
  background: rgba(255,255,255,.9);
}

.form-row input:focus,
.form-row select:focus,
.modal textarea:focus{
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--ring);
}

.modal textarea{
  resize: vertical;
  line-height: 1.35;
}

/* Applicants list cards (your "saved-item") */
.saved-item{
  display: flex;
  gap: 12px;
  padding: 12px;
  border-radius: 14px;
  border: 1px solid rgba(148,163,184,.35);
  background: rgba(249,250,251,.9);
  box-shadow: 0 10px 22px rgba(15,23,42,.06);
}

.saved-title{
  margin: 0;
  font-weight: 900;
  font-size: 13px;
  color: rgba(15,23,42,.92);
}

.saved-item .muted{
  margin: 0;
}

/* Status emphasis */
.saved-item strong{
  font-weight: 900;
}

/* Make the Reject reason textarea look good */
.modal textarea{
  border-radius: 14px;
}

/* Modal animations */
@keyframes modal-fade{
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes modal-pop{
  from { transform: translateY(8px) scale(.985); opacity: .95; }
  to { transform: translateY(0) scale(1); opacity: 1; }
}

/* Responsive tweaks */
@media (max-width: 640px){
  .modal-backdrop{ padding: 12px; }
  .modal{ padding: 16px 14px 14px; border-radius: 16px; }
  .modal h3{ font-size: 16px; }
  .saved-item{ padding: 10px; }
}

</style>

