<script setup>
import { useRouter } from 'vue-router';
import { logout } from '../../services/auth';
import { useToast } from '../../composables/useToast';
import { useAuth } from '../../composables/useAuth';
import AppHeader from './AppHeader.vue';
import AppFooter from './AppFooter.vue';

const router = useRouter();
const { showSuccess } = useToast();
const { handleLogout: authLogout } = useAuth();

const handleLogout = async () => {
  try {
    await logout();
    authLogout(); // Clear global auth state
    showSuccess('Logged out successfully');
    router.push('/');
  } catch (error) {
    console.error('Logout error:', error);
  }
};
</script>

<template>
  <div class="flex flex-col h-screen bg-base-200">
    <!-- Header Component -->
    <AppHeader @logout="handleLogout" />

    <!-- Main Content -->
    <main class="flex-1 overflow-auto">
      <RouterView />
    </main>

    <!-- Footer Component -->
    <AppFooter />
  </div>
</template>

<style scoped>
/* Custom scrollbar */
main::-webkit-scrollbar {
  width: 6px;
}

main::-webkit-scrollbar-track {
  background: transparent;
}

main::-webkit-scrollbar-thumb {
  background: hsl(var(--bc) / 0.2);
  border-radius: 3px;
}

main::-webkit-scrollbar-thumb:hover {
  background: hsl(var(--bc) / 0.3);
}
</style>
