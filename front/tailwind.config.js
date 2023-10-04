/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#FF6363',
        'secondary': {
          100: '#E2E2D5',
          200: '#888883',
        },
        'warning': '#FFA500',
        'danger': '#FF0000',
        'success': '#008000',
        'info': '#00FFFF',
        'dark': '#303952',
        'light': '#FFFFFF'
      },
    },
  },
  plugins: [],
}