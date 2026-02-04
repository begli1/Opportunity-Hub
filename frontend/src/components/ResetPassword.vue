<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { resetPassword } from '@/lib/authAPI'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const token = computed(() => (route.query.token ?? '').trim())
const newPassword = ref('')
const confirmPassword = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const submitting = ref(false)
const errors = reactive({ newPassword: false, confirmPassword: false })

onMounted(() => {
  if (!token.value) {
    errorMessage.value = 'Missing reset token. Please use the link from your email or request a new one.'
  }
})

function validate() {
  const out = {}
  const np = newPassword.value ?? ''
  const cp = confirmPassword.value ?? ''
  if (np.length < 8) out.newPassword = 'Password must be at least 8 characters.'
  if (np !== cp) out.confirmPassword = 'Passwords do not match.'
  return out
}

async function handleSubmit() {
  errorMessage.value = ''
  successMessage.value = ''
  if (!token.value) {
    errorMessage.value = 'Missing reset token. Please use the link from your email.'
    return
  }
  const out = validate()
  errors.newPassword = !!out.newPassword
  errors.confirmPassword = !!out.confirmPassword
  if (Object.keys(out).length) {
    errorMessage.value = Object.values(out).join(' ')
    return
  }
  submitting.value = true
  try {
    const data = await resetPassword({ token: token.value, new_password: newPassword.value })
    successMessage.value = data.message || 'Password has been reset. You can now log in.'
    setTimeout(() => router.push('/login'), 2500)
  } catch (err) {
    const detail = err.response?.data?.detail
    const code = detail?.code
    const msg = detail?.message || 'This link may be invalid or expired. Please request a new one.'
    errorMessage.value = msg
    if (code === 'INVALID_OR_EXPIRED_TOKEN') {
      errors.newPassword = true
      errors.confirmPassword = true
    }
  }
  submitting.value = false
}
</script>

<template>
  <body>
    <div class="wrapper">
      <h1 class="noninteractive">Set new password</h1>
      <p id="error-message" role="alert">{{ errorMessage }}</p>
      <p v-if="successMessage" class="success-message" role="status">{{ successMessage }}</p>

      <form v-if="token && !successMessage" @submit.prevent="handleSubmit">
        <div class="field" :class="{ incorrect: errors.newPassword }">
          <label for="new-password" aria-hidden="true">
            <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px">
              <path d="M240-80q-33 0-56.5-23.5T160-160v-400q0-33 23.5-56.5T240-640h40v-80q0-83 58.5-141.5T480-920q83 0 141.5 58.5T680-720v80h40q33 0 56.5 23.5T800-560v400q0 33-23.5 56.5T720-80H240Zm240-200q33 0 56.5-23.5T560-360q0-33-23.5-56.5T480-440q-33 0-56.5 23.5T400-360q0 33 23.5 56.5T480-280ZM360-640h240v-80q0-50-35-85t-85-35q-50 0-85 35t-35 85v80Z"/>
            </svg>
          </label>
          <input
            id="new-password"
            v-model="newPassword"
            type="password"
            name="new_password"
            placeholder="New password (min 8 characters)"
            autocomplete="new-password"
            :aria-invalid="errors.newPassword ? 'true' : 'false'"
            @input="errors.newPassword = false"
            required
            minlength="8"
          />
        </div>
        <div class="field" :class="{ incorrect: errors.confirmPassword }">
          <label for="confirm-password" aria-hidden="true">
            <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px">
              <path d="M240-80q-33 0-56.5-23.5T160-160v-400q0-33 23.5-56.5T240-640h40v-80q0-83 58.5-141.5T480-920q83 0 141.5 58.5T680-720v80h40q33 0 56.5 23.5T800-560v400q0 33-23.5 56.5T720-80H240Zm240-200q33 0 56.5-23.5T560-360q0-33-23.5-56.5T480-440q-33 0-56.5 23.5T400-360q0 33 23.5 56.5T480-280ZM360-640h240v-80q0-50-35-85t-85-35q-50 0-85 35t-35 85v80Z"/>
            </svg>
          </label>
          <input
            id="confirm-password"
            v-model="confirmPassword"
            type="password"
            name="confirm_password"
            placeholder="Confirm new password"
            autocomplete="new-password"
            :aria-invalid="errors.confirmPassword ? 'true' : 'false'"
            @input="errors.confirmPassword = false"
            required
          />
        </div>
        <button type="submit" :disabled="submitting">
          {{ submitting ? 'Resetting…' : 'Reset password' }}
        </button>
      </form>

      <p v-if="!token" class="back-link">
        <RouterLink to="/forgot-password">Request a new reset link</RouterLink>
      </p>
      <p v-else class="back-link">
        <RouterLink to="/login">Back to log in</RouterLink>
      </p>
    </div>
  </body>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

:global(:root) {
  --accent: #2563eb;
  --accent-2: #14b8a6;
  --base-color: #ffffff;
  --text-color: #0f172a;
  --input-color: #f1f5f9;
}
body {
  min-height: 100vh;
  background: url('@/assets/background.jpg') no-repeat center center;
  background-size: cover;
  overflow: hidden;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 14px;
  color: var(--text-color);
  text-align: center;
}
.wrapper {
  background-color: var(--base-color);
  height: 100vh;
  width: min(70%, 500px);
  padding: 40px;
  border-radius: 0 24px 24px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 20px 0 60px rgba(15, 23, 42, 0.08);
}
h1 {
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 8px;
}
form {
  width: min(380px, 100%);
  margin-top: 24px;
  margin-bottom: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
}
.field { width: 100%; display: flex; justify-content: center; }
.field > label {
  flex-shrink: 0;
  height: 48px;
  width: 48px;
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  color: var(--base-color);
  border-radius: 12px 0 0 12px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.field > label svg, .field > label svg * { fill: var(--base-color); }
.field > input {
  flex-grow: 1;
  min-width: 0;
  height: 48px;
  padding: 0 16px;
  font: inherit;
  border-radius: 0 12px 12px 0;
  border: 2px solid var(--input-color);
  border-left: none;
  background-color: var(--input-color);
  transition: all 0.2s ease;
  font-size: 14px;
}
.field > input:hover { border-color: rgba(37, 99, 235, 0.3); }
.field > input:focus { outline: none; border-color: var(--accent); background: #fff; }
form button {
  width: 100%;
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  color: white;
  font: inherit;
  font-weight: 700;
  cursor: pointer;
  border: none;
  border-radius: 12px;
  padding: 14px 24px;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25);
  transition: all 0.2s ease;
  margin-top: 8px;
}
form button[disabled] { opacity: 0.6; cursor: not-allowed; }
form button:hover:not([disabled]) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(37, 99, 235, 0.3);
}
#error-message { color: #ef4444; font-size: 13px; min-height: 20px; }
.success-message { color: #0f172a; margin-top: 8px; max-width: 360px; }
.back-link { margin-top: 16px; }
p { color: #64748b; font-size: 13px; }
a { text-decoration: none; color: var(--accent); font-weight: 600; }
a:hover { text-decoration: underline; }
.field.incorrect > label { background: linear-gradient(135deg, #ef4444, #f87171); }
.field.incorrect > input { border-color: #ef4444; }
.noninteractive { user-select: none; cursor: default; }
@media (max-width: 900px) {
  body { background: none; }
  .wrapper { width: 100%; border-radius: 0; padding: 24px; }
  h1 { font-size: 2rem; }
}
</style>
