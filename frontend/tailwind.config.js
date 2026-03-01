/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        elena: '#00ff88',
        marcus: '#ff6b6b',
      }
    },
  },
  plugins: [],
}
