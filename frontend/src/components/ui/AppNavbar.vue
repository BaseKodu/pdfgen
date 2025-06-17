<script setup>
import { logout } from '../../services/auth';
import AppButton from './AppButton.vue';
import { useRouter } from 'vue-router';
import { RouterLink } from 'vue-router';

const router = useRouter();

const handleLogout = () => {
  logout();
  router.push('/login');
};
</script>

<template>
  <div class="navbar bg-base-100 shadow-sm">
  <div class="flex-1">
    <RouterLink to="/templates" class="btn btn-ghost text-xl">pdfGen</RouterLink>

  </div>
  <div class="flex-none">
    <ul class="menu menu-horizontal px-1">
      <AppButton @click="handleLogout">Logout</AppButton>

    </ul>
  </div>
</div>
</template>

