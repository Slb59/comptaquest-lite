module.exports = {
  content: [
    "./templates/**/*.html",
    "./templates/**/*.js",
    "./static/css/**/*.css",
    "./static/js/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        bleup: 'var(--color-bleup)',
        brown: 'var(--color-brown)',
        vert: 'var(--color-vert)',
        violet: 'var(--color-violet)',
        or: 'var(--color-or)',
        taupe: 'var(--color-taupe)',
        white: 'var(--color-white)',
        verybrown: 'var(--color-verybrown)',
        gray: 'var(--color-gray)',
      },
      fontFamily: {
        cinzel: ['Cinzel', 'Arial', 'sans-serif'],
      }
    }
  },
  plugins: [],
}
