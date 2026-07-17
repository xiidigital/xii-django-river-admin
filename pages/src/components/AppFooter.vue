<template>
  <footer class="site-footer">
    <div class="footer-inner">
      <p class="copyright">
        &copy; {{ year }} XII Digital &amp;
        <a :href="contributorsUrl" target="_blank" rel="noopener">Contributors</a>
      </p>
      <ul class="footer-links">
        <li>
          <a :href="licenseUrl" target="_blank" rel="noopener">New BSD License</a>
        </li>
        <li>
          <a :href="repoUrl" target="_blank" rel="noopener">GitHub</a>
        </li>
      </ul>
    </div>
  </footer>
</template>

<script setup>
import { repoUrl, contributorsUrl, licenseUrl } from "../links.js";

const year = new Date().getFullYear();
</script>
