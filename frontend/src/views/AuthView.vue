<script setup>
import RegisterForm from '../components/auth/RegisterForm.vue';
import LoginForm from '../components/auth/LoginForm.vue';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '../composables/useAuth';
import { useToast } from '../composables/useToast';
import { getOAuthProviders, initiateGoogleOAuth } from '../services/oauth';

const activeTab = ref('login');
const router = useRouter();
const { handleLoginSuccess } = useAuth();
const { showError } = useToast();
const oauthProviders = ref({ providers: [], available: false });
const isLoadingProviders = ref(true);

const onRegistrationSuccess = () => {
  activeTab.value = 'login';
};

const handleGoogleLogin = async () => {
  try {
    // Get OAuth providers to check if Google is available
    const providers = await getOAuthProviders();
    if (!providers.providers.includes('google')) {
      showError('Google OAuth is not configured on the server');
      return;
    }

    // Initiate Google OAuth flow
    const authUrl = await initiateGoogleOAuth();
    window.location.href = authUrl;
  } catch (error) {
    console.error('Google OAuth error:', error);
    showError('Failed to initiate Google login. Please try again.');
  }
};

onMounted(async () => {
  try {
    const response = await getOAuthProviders();
    oauthProviders.value = response || { providers: [], available: false };
  } catch (error) {
    console.error('Failed to load OAuth providers:', error);
    // Set default values on error
    oauthProviders.value = { providers: [], available: false };
  } finally {
    isLoadingProviders.value = false;
  }
});
</script>

<template>
  <main class="flex items-center justify-center min-h-screen">
    <!-- Toast notifications -->
    <div class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
      <div class="card-body">
        <div class="text-center">
          <h1 class="text-5xl font-bold">pdfGen</h1>
          <p class="py-6">Generate your pdfs with pdfGen</p>
        </div>

        <div role="tablist" class="tabs tabs-lifted">
          <input
            type="radio"
            name="auth_tabs"
            role="tab"
            class="tab"
            aria-label="Login"
            v-model="activeTab"
            value="login"
            checked>
          <div role="tabpanel" class="tab-content p-4" v-if="activeTab === 'login'">
            <LoginForm />
          </div>

          <input
            type="radio"
            name="auth_tabs"
            role="tab"
            class="tab"
            aria-label="Register"
            v-model="activeTab"
            value="register">
          <div role="tabpanel" class="tab-content p-4" v-if="activeTab === 'register'">
            <RegisterForm @registration-success="onRegistrationSuccess" />
          </div>
        </div>

        <div class="divider">OR</div>

        <!-- Google Sign In Button -->
        <div v-if="!isLoadingProviders">
          <button
            v-if="oauthProviders.providers && oauthProviders.providers.includes('google')"
            @click="handleGoogleLogin"
            class="btn btn-outline gap-2 hover:bg-base-200 w-full"
          >
          <v-icon name="fc-google" />
          Continue with Google
          </button>
        </div>

        <!-- Loading state -->
        <div v-else class="flex justify-center">
          <span class="loading loading-spinner loading-sm"></span>
        </div>
      </div>
    </div>
  </main>
</template>
