<script setup>
import { ref } from 'vue';
import { RouterLink } from 'vue-router';

const features = [
  {
    title: 'Multiple Template Formats',
    description: 'Write your PDF templates using JSX, Vue, or plain HTML - choose what works best for you',
    icon: '📝'
  },
  {
    title: 'Live Editor',
    description: 'Design and preview your PDF templates in real-time using our online editor',
    icon: '✨'
  },
  {
    title: 'API Integration',
    description: 'Generate PDFs programmatically using our REST API endpoints',
    icon: '🔗'
  },
  {
    title: 'Self-Hosting Option',
    description: 'Deploy your own instance using Docker for complete control over your PDF generation service',
    icon: '🐳'
  }
];

const startOptions = [
  {
    title: 'Create Account',
    description: 'Sign up to save your templates, manage API keys, and access all features',
    icon: '👤',
    action: 'Sign Up',
    route: '/login',
    style: 'btn-primary'
  },
  {
    title: 'Try Instantly',
    description: 'Start creating templates right away with browser-only storage',
    icon: '🚀',
    action: 'Start Now',
    route: '/templates',
    style: 'btn-secondary'
  },
  {
    title: 'Self Host',
    description: 'Clone or fork the repository to run your own instance',
    icon: '📦',
    action: 'View Repository',
    link: 'https://github.com/Basekodu/pdfgen',
    style: 'btn-outline'
  }
];
</script>

<template>
  <main class="min-h-screen bg-gradient-to-br from-base-100 to-base-200 py-12 px-4">
    <!-- Hero Section -->
    <div class="max-w-6xl mx-auto text-center mb-16">
      <h1 class="text-6xl font-bold mb-4">pdfGen</h1>
      <p class="text-xl text-base-content/80 mb-8">
        Transform your templates into beautiful PDFs with ease
      </p>
    </div>

    <!-- Get Started Options -->
    <div class="max-w-5xl mx-auto mb-20">
      <h2 class="text-3xl font-bold text-center mb-12">Choose Your Path</h2>
      <div class="grid md:grid-cols-3 gap-8">
        <div v-for="option in startOptions" :key="option.title"
             class="card bg-base-100 shadow-xl hover:shadow-2xl transition-all hover:-translate-y-1">
          <div class="card-body text-center">
            <div class="text-4xl mb-4">{{ option.icon }}</div>
            <h3 class="text-xl font-bold mb-2">{{ option.title }}</h3>
            <p class="text-base-content/70 mb-6">{{ option.description }}</p>
            <div class="card-actions justify-center">
              <RouterLink
                v-if="option.route"
                :to="option.route"
                :class="['btn', option.style]">
                {{ option.action }}
              </RouterLink>
              <a
                v-else
                :href="option.link"
                target="_blank"
                rel="noopener noreferrer"
                :class="['btn', option.style]">
                {{ option.action }}
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Features Grid -->
    <div class="max-w-6xl mx-auto">
      <div class="grid md:grid-cols-2 gap-8">
        <div v-for="feature in features" :key="feature.title"
             class="card bg-base-100 shadow-xl hover:shadow-2xl transition-shadow">
          <div class="card-body">
            <div class="text-4xl mb-4">{{ feature.icon }}</div>
            <h2 class="card-title">{{ feature.title }}</h2>
            <p class="text-base-content/70">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Usage Section -->
    <div class="max-w-6xl mx-auto mt-16">
      <div class="card bg-base-100 shadow-xl">
        <div class="card-body">
          <h2 class="text-3xl font-bold mb-6">Two Ways to Use pdfGen</h2>

          <div class="grid md:grid-cols-2 gap-8">
            <!-- Cloud Option -->
            <div class="space-y-4">
              <h3 class="text-2xl font-semibold">☁️ Cloud Service</h3>
              <ul class="list-disc list-inside space-y-2 text-base-content/70">
                <li>Use our live editor to create templates</li>
                <li>Generate PDFs via API calls</li>
                <li>No setup required</li>
                <li>Perfect for quick prototypes</li>
              </ul>
            </div>

            <!-- Self-hosted Option -->
            <div class="space-y-4">
              <h3 class="text-2xl font-semibold">🏢 Self-Hosted</h3>
              <ul class="list-disc list-inside space-y-2 text-base-content/70">
                <li>Deploy using Docker</li>
                <li>Full control over the service</li>
                <li>Enhanced security & privacy</li>
                <li>Ideal for enterprise use</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
