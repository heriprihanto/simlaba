/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        theme: {
          DEFAULT: '#308e87',
          hover: '#27756f',
          light: '#eaf4f3',
          dark: '#1e5955',
          secondary: '#f39159',
          'secondary-hover': '#e27b41',
          'secondary-light': '#fef4ee'
        }
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'Inter', 'sans-serif']
      }
    },
  },
  plugins: [],
}
