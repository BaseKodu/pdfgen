/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./views/**/*.{html,js,ejs}", // adjust based on your template engine
    "./public/**/*.{html,js}"
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui')
  ],
}