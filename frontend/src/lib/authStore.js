import { computed, ref, watch } from "vue"

const TOKEN_KEY = 'auth_token'
const TOKEN_EXPIRY_KEY = 'auth_token_expiry'
const USER_KEY = 'auth_user'

// Initialize from localStorage
const token = ref(localStorage.getItem(TOKEN_KEY))
const tokenExpiry = ref(localStorage.getItem(TOKEN_EXPIRY_KEY) ? parseInt(localStorage.getItem(TOKEN_EXPIRY_KEY)) : null)

// User info storage
const storedUser = localStorage.getItem(USER_KEY)
const user = ref(storedUser ? JSON.parse(storedUser) : null)

export function useAuth() {
    function setToken(newToken, expiresIn) {
        token.value = newToken
        // Store in localStorage
        localStorage.setItem(TOKEN_KEY, newToken)
        
        // Calculate expiry timestamp (expiresIn is in seconds)
        if (expiresIn) {
            const expiryTime = Date.now() + (expiresIn * 1000)
            tokenExpiry.value = expiryTime
            localStorage.setItem(TOKEN_EXPIRY_KEY, expiryTime.toString())
        }
    }

    function setUser(userInfo) {
        user.value = userInfo
        if (userInfo) {
            localStorage.setItem(USER_KEY, JSON.stringify(userInfo))
        } else {
            localStorage.removeItem(USER_KEY)
        }
    }

    function clearToken() {
        token.value = null
        tokenExpiry.value = null
        user.value = null
        localStorage.removeItem(TOKEN_KEY)
        localStorage.removeItem(TOKEN_EXPIRY_KEY)
        localStorage.removeItem(USER_KEY)
    }

    function isTokenExpired() {
        if (!tokenExpiry.value) return true
        return Date.now() >= tokenExpiry.value
    }

    // Check if token is valid (exists and not expired)
    const isAuthenticated = computed(() => {
        return token.value !== null && !isTokenExpired()
    })

    // Get user initials for avatar
    const userInitials = computed(() => {
        if (!user.value?.username) return '??'
        const name = user.value.username
        return name.substring(0, 2).toUpperCase()
    })
    
    // Auto-clear token if expired
    watch(tokenExpiry, (expiry) => {
        if (expiry && Date.now() >= expiry) {
            clearToken()
        }
    })

    return { 
        token, 
        user,
        userInitials,
        isAuthenticated, 
        setToken,
        setUser,
        clearToken,
        isTokenExpired
    }
}