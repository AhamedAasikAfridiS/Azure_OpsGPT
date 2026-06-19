/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        opsgpt: {
          primary: "#0F766E",
          hover: "#115E59",
          accent: "#0891B2",
          text: "#0F172A",
          muted: "#64748B",
          background: "#F8FAFC",
          surface: "#FFFFFF",
          border: "#E2E8F0",
          success: "#059669",
          warning: "#D97706",
          danger: "#DC2626"
        }
      },
      borderRadius: {
        ops: "8px"
      }
    }
  },
  plugins: []
};
