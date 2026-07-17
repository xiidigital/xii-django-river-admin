<template>
  <div id="app">
    <AppHeader />
    <main>
      <Hero />
      <Screenshots />
    </main>
    <AppFooter />
  </div>
</template>

<script setup>
import AppHeader from "./components/AppHeader.vue";
import AppFooter from "./components/AppFooter.vue";
import Hero from "./components/Hero.vue";
import Screenshots from "./components/Screenshots.vue";
</script>
