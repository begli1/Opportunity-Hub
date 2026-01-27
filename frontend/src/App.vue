<template>
  <RouterView />
</template>

<script setup>
// empty on purpose
</script>

<style>
/* Reset body and html to allow proper scrolling */
html, body {
  margin: 0;
  padding: 0;
  overflow-x: hidden; /* Prevent horizontal scroll */
}

body {
  background-color: #f7fafc; /* Match Prelogin background */
}

#app {
  min-height: 100vh;
}
</style>