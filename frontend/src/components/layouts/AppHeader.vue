<script setup>
import { computed } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
import { useAuth } from '../../composables/useAuth';

const route = useRoute();
const { isGuestUser, userDisplayName, userInitials, userEmail } = useAuth();

const currentPageTitle = computed(() => {
  if (route.path.startsWith('/templates/') && route.path !== '/templates') {
    return 'Template Editor';
  } else if (route.path === '/templates') {
    return 'Templates';
  }
  return 'Dashboard';
});

// Define emits for parent component
const emit = defineEmits(['logout']);

const handleLogout = () => {
  emit('logout');
};
</script>

<template>
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
</template>
