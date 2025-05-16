import daisyui from 'daisyui'

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  plugins: [daisyui],
  daisyui: {
    themes: ["sunset"], // Only include sunset theme
    darkTheme: "sunset", // Use sunset as dark theme
    base: true,
    styled: true,
    utils: true,
    prefix: "",
    logs: true,
    themeRoot: ":root",
  },
}
