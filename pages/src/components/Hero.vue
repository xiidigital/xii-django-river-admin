<template>
  <section class="hero">
    <div class="hero-inner">
      <img src="/img/brand/logo.png" alt="xii-django-river-admin" class="hero-logo" />
      <p class="hero-tagline">
        A shiny admin interface for
        <a href="https://github.com/xiidigital/xii-django-river" target="_blank" rel="noopener"
          >django-river</a
        >, forked and modernized for Django 4.2&ndash;6.0, Python 3.10&ndash;3.13, and
        Vue&nbsp;3 / Vuetify&nbsp;3.
      </p>
      <div class="hero-actions">
        <a :href="docsUrl" target="_blank" rel="noopener" class="btn btn-primary">Get Started</a>
        <a :href="repoUrl" target="_blank" rel="noopener" class="btn btn-outline">GitHub</a>
      </div>
      <div class="hero-star">
        <span>Star us on</span>
        <a :href="repoUrl" target="_blank" rel="noopener">
          <img src="/img/brand/github-white-slim.png" alt="GitHub" />
        </a>
      </div>
    </div>
  </section>
</template>

<script setup>
import { repoUrl, docsUrl } from "../links.js";
</script>
