/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        drought: {
          low: '#fef3c7',
          medium: '#f59e0b',
          high: '#dc2626',
          extreme: '#7f1d1d'
        }
      }
    },
  },
  plugins: [],
}