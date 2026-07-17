<template>
  <section class="screenshots">
    <div class="screenshots-inner">
      <div class="screenshots-intro">
        <h1>Modern design</h1>
        <p>The admin UI is built with Vue 3 &amp; Vuetify 3.</p>
      </div>
      <div class="screenshots-grid">
        <figure v-for="shot in shots" :key="shot.src" class="screenshot-card">
          <img :src="shot.src" :alt="shot.alt" loading="lazy" />
          <figcaption>{{ shot.alt }}</figcaption>
        </figure>
      </div>
    </div>
  </section>
</template>

<script setup>
const shots = [
  { src: "/img/theme/home.png", alt: "Home / dashboard" },
  { src: "/img/theme/create-function.png", alt: "Create function" },
  { src: "/img/theme/reprio.png", alt: "Reprioritize" },
  { src: "/img/theme/timeline.png", alt: "Workflow timeline" },
];
</script>
