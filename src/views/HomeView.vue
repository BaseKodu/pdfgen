<script setup lang="ts">
import { ref } from 'vue';

const email = ref('');
const password = ref('');
const confirmPassword = ref('');

const handleLogin = () => {
  // Handle login logic here
  console.log('Logging in with:', { email: email.value, password: password.value });
};
const handleRegister = () => {
  // Handle registration logic here
  console.log('Registering with:', { email: email.value, password: password.value, confirmPassword: confirmPassword.value });
};
const handleGoogleSignIn = () => {
  // Handle Google sign-in logic here
  console.log('Signing in with Google');
};


</script>

<template>
  <main class="flex items-center justify-center min-h-screen">
    <div class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
      <div class="card-body">
        <div class="text-center">
          <h1 class="text-5xl font-bold">pdfGen</h1>
          <p class="py-6">Generate your pdfs with pdfGen</p>
        </div>

        <div role="tablist" class="tabs tabs-lifted">
          <input type="radio" name="auth_tabs" role="tab" class="tab" aria-label="Login" checked />
          <div role="tabpanel" class="tab-content p-4">
            <form class="space-y-4">
              <div class="form-control">
                <label class="label"><span class="label-text">Email</span></label>
                <input type="email" v-model="email" placeholder="email" class="input input-bordered" required />
              </div>
              <div class="form-control">
                <label class="label"><span class="label-text">Password</span></label>
                <input type="password" v-model="password" placeholder="password" class="input input-bordered" required />
              </div>
              <div class="form-control mt-6">
                <button class="btn btn-primary">Login</button>
              </div>
            </form>
          </div>

          <input type="radio" name="auth_tabs" role="tab" class="tab" aria-label="Register" />
          <div role="tabpanel" class="tab-content p-4">
            <form class="space-y-4">
              <div class="form-control">
                <label class="label"><span class="label-text">Email</span></label>
                <input type="email" v-model="email" placeholder="email" class="input input-bordered" required />
              </div>
              <div class="form-control">
                <label class="label"><span class="label-text">Password</span></label>
                <input type="password" v-model="password" placeholder="password" class="input input-bordered" required />
              </div>
              <div class="form-control">
                <label class="label"><span class="label-text">Confirm Password</span></label>
                <input type="password" v-model="confirmPassword" placeholder="confirm password" class="input input-bordered" required />
              </div>
              <div class="form-control mt-6">
                <button class="btn btn-primary">Register</button>
              </div>
            </form>
          </div>
        </div>

        <div class="divider">OR</div>

        <!-- Google Sign In Button -->
        <a href="/auth/google" class="btn btn-outline gap-2 hover:bg-base-200">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 48 48">
            <path fill="#FFC107" d="M43.611 20.083H42V20H24v8h11.303c-1.649 4.657-6.08 8-11.303 8-6.627 0-12-5.373-12-12s5.373-12 12-12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.268 4 24 4 12.955 4 4 12.955 4 24s8.955 20 20 20 20-8.955 20-20c0-1.341-.138-2.65-.389-3.917z"/>
            <path fill="#FF3D00" d="m6.306 14.691 6.571 4.819C14.655 15.108 18.961 12 24 12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.268 4 24 4 16.318 4 9.656 8.337 6.306 14.691z"/>
            <path fill="#4CAF50" d="M24 44c5.166 0 9.86-1.977 13.409-5.192l-6.19-5.238A11.91 11.91 0 0 1 24 36c-5.202 0-9.619-3.317-11.283-7.946l-6.522 5.025C9.505 39.556 16.227 44 24 44z"/>
            <path fill="#1976D2" d="M43.611 20.083H42V20H24v8h11.303a12.04 12.04 0 0 1-4.087 5.571l.003-.002 6.19 5.238C36.971 39.205 44 34 44 24c0-1.341-.138-2.65-.389-3.917z"/>
          </svg>
          Continue with Google
        </a>
      </div>
    </div>
  </main>
</template>
