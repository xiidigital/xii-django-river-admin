<template>
  <header class="site-header">
    <nav class="navbar">
      <a href="/" class="navbar-brand">
        <img src="/img/brand/logo.png" alt="xii-django-river-admin logo" />
        <span>xii-django-river-admin</span>
      </a>

      <button
        class="navbar-toggle"
        type="button"
        aria-label="Toggle navigation"
        @click="menuOpen = !menuOpen"
      >
        &#9776;
      </button>

      <div class="navbar-menu" :class="{ 'is-open': menuOpen }">
        <div class="navbar-dropdown">
          <button type="button" class="nav-link dropdown-toggle" @click="examplesOpen = !examplesOpen">
            Examples
          </button>
          <div class="dropdown-panel" v-show="examplesOpen">
            <a
              :href="`${repoUrl}/tree/master/examples/shipping_example`"
              target="_blank"
              rel="noopener"
              class="dropdown-item"
            >
              <strong>Shipping</strong>
              <span>An example shipping workflow built with xii-django-river-admin</span>
            </a>
            <a
              :href="`${repoUrl}/tree/master/examples/issue_tracker_example`"
              target="_blank"
              rel="noopener"
              class="dropdown-item"
            >
              <strong>Issue Tracking</strong>
              <span>A simple issue tracking workflow built with xii-django-river-admin</span>
            </a>
          </div>
        </div>

        <a :href="docsUrl" target="_blank" rel="noopener" class="nav-link">Docs</a>

        <a :href="repoUrl" target="_blank" rel="noopener" class="nav-link nav-link-icon">
          GitHub
        </a>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { ref } from "vue";
import { repoUrl, docsUrl } from "../links.js";

const menuOpen = ref(false);
const examplesOpen = ref(false);
</script>
