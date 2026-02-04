<script setup>
import { ref, reactive } from 'vue'
import { forgotPassword } from '@/lib/authAPI'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const resetLink = ref('')
const submitting = ref(false)
const errors = reactive({ email: false })

function validateEmail(e) {
  const v = (e ?? '').trim().toLowerCase()
  if (!v) return { error: 'Email is required.', normalized: v }
  if (!/^\S+@\S+\.\S+$/.test(v)) return { error: 'Enter a valid email address.', normalized: v }
  return { error: null, normalized: v }
}

async function handleSubmit() {
  errorMessage.value = ''
  successMessage.value = ''
  resetLink.value = ''
  const { error, normalized } = validateEmail(email.value)
  errors.email = !!error
  if (error) {
    errorMessage.value = error
    return
  }
  submitting.value = true
  try {
    const data = await forgotPassword({ email: normalized })
    successMessage.value = data.message || 'If an account exists with that email, you will receive a link to reset your password.'
    if (data.reset_link) resetLink.value = data.reset_link
  } catch (err) {
    if (!err.response) {
      errorMessage.value = 'Could not reach server. Try again later.'
    } else {
      errorMessage.value = err.response?.data?.detail?.message || 'Something went wrong. Please try again.'
    }
  }
  submitting.value = false
}
</script>

<template>
  <body>
    <div class="wrapper">
      <h1 class="noninteractive">Forgot password</h1>
      <p id="error-message" role="alert">{{ errorMessage }}</p>
      <p v-if="successMessage" class="success-message" role="status">{{ successMessage }}</p>
      <p v-if="resetLink" class="dev-link">
        <strong>Development:</strong> Use this link to reset your password:
        <a :href="resetLink" target="_blank" rel="noopener noreferrer">Reset password</a>
      </p>

      <form v-if="!successMessage" @submit.prevent="handleSubmit">
        <div class="field" :class="{ incorrect: errors.email }">
          <label for="forgot-email" aria-hidden="true"><span>@</span></label>
          <input
            id="forgot-email"
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
        <button type="submit" :disabled="submitting">
          {{ submitting ? 'Sending…' : 'Send reset link' }}
        </button>
      </form>

      <p class="back-link">
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
  font-size: 1.25rem;
  font-weight: 500;
}
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
.dev-link { font-size: 12px; color: #64748b; margin-top: 12px; max-width: 360px; }
.dev-link a { color: var(--accent); font-weight: 600; }
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
