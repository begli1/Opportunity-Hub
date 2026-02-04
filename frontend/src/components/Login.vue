<script setup>
import { ref, reactive } from 'vue'
import {login} from '@/lib/authAPI'

import { useAuth } from '@/lib/authStore'
import { useRouter } from 'vue-router'
const { setToken } = useAuth()
const router = useRouter()


const email = ref('')
const password = ref('')
const errorMessage = ref('')
const submitting = ref(false)

const errors = reactive({ email: false, password: false })

function validateLogin({ email, password }) {
  const out = {}

  const e = (email ?? '').trim().toLowerCase()
  const p = password ?? ''

  if (!e) out.email = 'Email is required!'
  else if (!/^\S+@\S+\.\S+$/.test(e)) out.email = 'Enter a valid email address'

  if (!p) out.password = 'Password is required!'

  return { out, normalized: { email: e, password: p } }
}

async function handleLogin() {
  submitting.value = true
  errorMessage.value = ''

  const { out, normalized } = validateLogin({
    email: email.value,
    password: password.value,
  })

  errors.email = !!out.email
  errors.password = !!out.password
  errorMessage.value = Object.values(out).join(' ')

if (!errorMessage.value) {
    // ✅ Ready to call your API (Axios/fetch). Do NOT log secrets.
    // Example payload is normalized (trimmed + lowercased email).
    const payload = normalized

    try {
      const data = await login(payload)
      setToken(data.access_token, data.expires_in) // Pass expires_in

      await router.push('/moderation')

    } catch (err) {

      // 1) No response at all → network/server issue
      if (!err.response) {
        errorMessage.value = 'Could not reach server. Try again later.'
        return
      }

      // 2) We have a response from backend
      const status = err.response.status
      const detail = err.response.data?.detail || {}
      const code = detail.code

      if (status === 401 && code === 'INVALID_CREDENTIALS') {
        errors.email = true
        errors.password = true
        errorMessage.value = detail.message || 'Incorrect email or password'
      } else {
        errorMessage.value = 'Something went wrong. Please try again.'
      }

    }
  }


  submitting.value = false
}
</script>

<template>
  <body>
  <div class="wrapper">
    <h1 class="noninteractive">Log In</h1>
    <p id="error-message" role="alert">{{ errorMessage }}</p>

    <form @submit.prevent="handleLogin">
      <!-- EMAIL -->
      <div class="field" :class="{ incorrect: errors.email }">
        <label for="email-input" aria-hidden="true"><span>@</span></label>
        <input
          id="email-input"
          v-model.trim="email"
          type="email"
          name="email"
          placeholder="E-mail"
          autocomplete="email"
          :aria-invalid="errors.email ? 'true' : 'false'"
          @input="errors.email = false"
          required
        />
      </div>

      <!-- PASSWORD -->
      <div class="field" :class="{ incorrect: errors.password }">
        <label for="password-input" aria-hidden="true">
          <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px">
            <path d="M240-80q-33 0-56.5-23.5T160-160v-400q0-33 23.5-56.5T240-640h40v-80q0-83 58.5-141.5T480-920q83 0 141.5 58.5T680-720v80h40q33 0 56.5 23.5T800-560v400q0 33-23.5 56.5T720-80H240Zm240-200q33 0 56.5-23.5T560-360q0-33-23.5-56.5T480-440q-33 0-56.5 23.5T400-360q0 33 23.5 56.5T480-280ZM360-640h240v-80q0-50-35-85t-85-35q-50 0-85 35t-35 85v80Z"/>
          </svg>
        </label>
        <input
          id="password-input"
          v-model="password"
          type="password"
          name="password"
          placeholder="Password"
          autocomplete="current-password"
          :aria-invalid="errors.password ? 'true' : 'false'"
          @input="errors.password = false"
          required
        />
      </div>

      <p>New here? <RouterLink to="/signup">Sign up</RouterLink></p>
      <button type="submit" :disabled="submitting">{{ submitting ? 'Logging in…' : 'Log In' }}</button>
    </form>
  </div>
</body>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

:global(:root){
  --accent:#2563eb;
  --accent-2:#14b8a6;
  --base-color:#ffffff;
  --text-color:#0f172a;
  --input-color:#f1f5f9;
}
body{
  min-height:100vh;
  background:url('@/assets/background.jpg') no-repeat center center;
  background-size:cover;
  overflow:hidden;
}

*{ margin:0; padding:0; box-sizing:border-box; }
html{
  font-family:'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size:14px;
  color:var(--text-color);
  text-align:center;
}

.wrapper{
  background-color:var(--base-color);
  height:100vh;
  width:min(70%, 500px);
  padding:40px;
  border-radius:0 24px 24px 0;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  box-shadow:20px 0 60px rgba(15,23,42,.08);
}

h1{
  font-size:2.5rem;
  font-weight:800;
  background:linear-gradient(135deg, var(--accent), var(--accent-2));
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  margin-bottom:8px;
}

/* form layout */
form{
  width:min(380px, 100%);
  margin-top:24px; margin-bottom:40px;
  display:flex; flex-direction:column; align-items:center; gap:14px;
}
.field{ width:100%; display:flex; justify-content:center; }
.field > label{
  flex-shrink:0; height:48px; width:48px;
  background:linear-gradient(135deg, var(--accent), var(--accent-2));
  color:var(--base-color);
  border-radius:12px 0 0 12px;
  display:flex; justify-content:center; align-items:center;
  font-size:1.25rem; font-weight:500;
}
.field > label svg, .field > label svg * { fill: var(--base-color); }

.field > input{
  flex-grow:1; min-width:0; height:48px; padding:0 16px; font:inherit;
  border-radius:0 12px 12px 0;
  border:2px solid var(--input-color); border-left:none;
  background-color:var(--input-color);
  transition:all 0.2s ease;
  font-size:14px;
}
.field > input:hover{ border-color:rgba(37,99,235,.3); }
.field > input:focus{ outline:none; border-color:var(--accent); background:#fff; }
.field:focus-within > label{ background:var(--text-color); }

form input::placeholder{ color:#94a3b8; }

/* button */
form button{
  width:100%;
  background:linear-gradient(135deg, var(--accent), var(--accent-2));
  color:white;
  font:inherit;
  font-weight:700;
  cursor:pointer;
  border:none;
  border-radius:12px;
  padding:14px 24px;
  box-shadow:0 4px 14px rgba(37,99,235,.25);
  transition:all 0.2s ease;
  margin-top:8px;
}
form button[disabled]{ opacity:.6; cursor:not-allowed; }
form button:hover:not([disabled]){
  transform:translateY(-2px);
  box-shadow:0 8px 20px rgba(37,99,235,.3);
}
form button:active{
  transform:scale(0.98);
}

/* links */
p{ color:#64748b; font-size:13px; }
a{ text-decoration:none; color:var(--accent); font-weight:600; }
a:hover{ text-decoration:underline; }

/* responsive */
@media(max-width:900px){
  body{ background:none; }
  .wrapper{ width:100%; border-radius:0; padding:24px; }
  h1{ font-size:2rem; }
}

/* errors */
.field.incorrect > label{ background:linear-gradient(135deg, #ef4444, #f87171); }
.field.incorrect > input{ border-color:#ef4444; }
#error-message{ color:#ef4444; font-size:13px; min-height:20px; }
.noninteractive { user-select:none; cursor:default; }
</style>
