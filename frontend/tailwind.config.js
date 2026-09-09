/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        oil: {
          dark: '#0a101d',
          navy: '#0f172a',
          card: '#1e293b',
          border: '#334155',
          gold: '#f59e0b',
          accent: '#0284c7'
        }
      }
    },
  },
  plugins: [],
}
