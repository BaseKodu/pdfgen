<script setup>
import { computed, ref } from 'vue';
import { RouterLink, useRoute, useRouter } from 'vue-router';
import { logout } from '../../services/auth';
import { useToast } from '../../composables/useToast';
import { useAuth } from '../../composables/useAuth';

const route = useRoute();
const router = useRouter();
const { showSuccess } = useToast();
const { user, isGuestUser, userDisplayName, userInitials, userEmail, handleLogout: authLogout } = useAuth();

const currentPageTitle = computed(() => {
  if (route.path.startsWith('/templates/') && route.path !== '/templates') {
    return 'Template Editor';
  } else if (route.path === '/templates') {
    return 'Templates';
  }
  return 'Dashboard';
});

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

const currentYear = ref(new Date().getFullYear());
</script>

<template>
  <div class="flex flex-col h-screen bg-base-200">
    <!-- Top Header -->
    <header class="bg-base-100 border-b border-base-300 px-6 py-2 flex items-center justify-between">
      <div class="flex items-center space-x-4">
        <!-- Logo/Brand -->
        <RouterLink to="/templates" class="flex items-center space-x-3">
          <div>
            <h1 class="text-lg font-bold text-base-content">pdfGen</h1>
          </div>
        </RouterLink>

      </div>

      <!-- Right side actions -->
      <div class="flex items-center space-x-4">
        <div>
          <div class="flex items-center gap-3">
            <h2 class="text-xl font-semibold text-base-content">{{ currentPageTitle }}</h2>
            <div v-if="isGuestUser" class="badge badge-warning badge-sm">Guest Mode</div>
          </div>

        </div>

        <!-- Quick Actions -->
        <div class="flex items-center space-x-2">
          <!-- User Menu -->
          <div class="dropdown dropdown-end">
            <div tabindex="0" role="button" class="btn btn-ghost btn-circle avatar">
              <div class="w-10 rounded-full flex items-center justify-center"
                   :class="isGuestUser ? 'bg-warning text-warning-content' : 'bg-neutral text-neutral-content'">
                <span class="text-sm font-medium">{{ userInitials }}</span>
              </div>
            </div>
            <ul tabindex="0" class="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52">
              <li class="menu-title">
                <div class="flex items-center gap-2">
                  <span>{{ userDisplayName }}</span>
                  <div v-if="isGuestUser" class="badge badge-orange badge-xs">Guest</div>
                </div>
                <span class="text-xs opacity-60">{{ userEmail }}</span>
              </li>
              <li><a href="https://github.com/Basekodu/pdfgen" target="_blank">📖 Documentation</a></li>
              <li><a href="https://github.com/Basekodu/pdfgen" target="_blank">🐛 Report Issue</a></li>
              <li><a href="mailto:support@pdfgen.com">💬 Support</a></li>
              <div class="divider my-1"></div>
              <li><a @click="handleLogout" class="text-error">Logout</a></li>
            </ul>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 overflow-auto">
      <RouterView />
    </main>

    <!-- Footer -->
    <footer class="bg-base-100 border-t border-base-300 px-6 py-3">
      <div class="flex items-center justify-between text-sm text-base-content/60">
        <div class="flex items-center space-x-4">
          <span>&copy; {{ currentYear }} pdfGen</span>
          <span>•</span>
          <a href="https://github.com/Basekodu/pdfgen" target="_blank" class="hover:text-base-content transition-colors">
            Open Source
          </a>
        </div>

      </div>
    </footer>
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
