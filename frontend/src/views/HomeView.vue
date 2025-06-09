<script setup>
import { ref } from 'vue';

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
</script>

<template>
  <main class="min-h-screen bg-gradient-to-br from-base-100 to-base-200 py-12 px-4">
    <!-- Hero Section -->
    <div class="max-w-6xl mx-auto text-center mb-16">
      <h1 class="text-6xl font-bold mb-4">pdfGen</h1>
      <p class="text-xl text-base-content/80 mb-8">
        Transform your templates into beautiful PDFs with ease
      </p>
      <div class="flex gap-4 justify-center">
        <button class="btn btn-primary">Get Started</button>
        <button class="btn btn-outline">View Documentation</button>
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
