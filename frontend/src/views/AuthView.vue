<script setup>
import RegisterForm from '../components/auth/RegisterForm.vue';
import LoginForm from '../components/auth/LoginForm.vue';
import AppToast from '../components/ui/AppToast.vue';
import { ref } from 'vue';

const activeTab = ref('login');

const onRegistrationSuccess = () => {
  activeTab.value = 'login';
};
</script>

<template>
  <main class="flex items-center justify-center min-h-screen">
    <!-- Toast notifications -->
    <AppToast position="top-center" />
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
        <a href="/auth/google" class="btn btn-outline gap-2 hover:bg-base-200">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 48 48">
            <!-- Google logo SVG paths -->
          </svg>
          Continue with Google
        </a>
      </div>
    </div>
  </main>
</template>
