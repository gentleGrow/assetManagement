import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      screens: {
        mobile: {
          max: "840px",
        },
        tablet: {
          min: "841px",
          max: "1280px",
        },
        "except-mobile": {
          min: "840px",
        },

        "except-tablet": {
          min: "1280px",
        },
      },
      colors: {
        alert: "#F84A4A",
        decrease: "#0A6CFF",
        gray: {
          "0": "#FFFFFF",
          "5": "#F7F8FA",
          "10": "#EFF0F1",
          "20": "#D8DADC",
          "30": "#B9BCC1",
          "40": "#999DA4",
          "50": "#7A8088",
          "60": "#5D646E",
          "70": "#4F555E",
          "80": "#42474E",
          "90": "#35393F",
          "100": "#2A2D31",
        },
        green: {
          "10": "#E6FBF0",
          "20": "#C3F5DA",
          "30": "#94EBDD",
          "40": "#62E59E",
          "50": "#32DD81",
          "60": "#05D665",
          "70": "#04B656",
          "80": "#049848",
          "90": "#0373A9",
          "100": "#02602D",
        },
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        chart: {
          "1": "hsl(var(--chart-1))",
          "2": "hsl(var(--chart-2))",
          "3": "hsl(var(--chart-3))",
          "4": "hsl(var(--chart-4))",
          "5": "hsl(var(--chart-5))",
        },
      },
      fontSize: {
        "body-6xl": ["60px", { lineHeight: "150%" }],
        "body-5xl": ["48px", { lineHeight: "150%" }],
        "body-4xl": ["36px", { lineHeight: "150%" }],
        "body-3xl": ["30px", { lineHeight: "150%" }],
        "body-2xl": ["24px", { lineHeight: "150%" }],
        "body-xl": ["20px", { lineHeight: "150%" }],
        "body-lg": ["18px", { lineHeight: "150%" }],
        "body-md": ["16px", { lineHeight: "150%" }],
        "body-sm": ["14px", { lineHeight: "150%" }],
        "body-xs": ["12px", { lineHeight: "150%" }],
        "heading-1": ["24px", { lineHeight: "24px", fontWeight: 700 }],
        "heading-2": ["20px", { lineHeight: "24px", fontWeight: 700 }],
        "heading-4": ["16px", { lineHeight: "19.2px", fontWeight: 700 }],
        "body-1": ["16px", { lineHeight: "19.2px", fontWeight: 400 }],
        "body-2": ["14px", { lineHeight: "16.8px", fontWeight: 400 }],
        "body-3": ["14px", { lineHeight: "16.8px", fontWeight: 600 }],
        "body-4": ["12px", { lineHeight: "18px", fontWeight: 600 }],
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [require("tailwindcss-animate"), require("tailwind-scrollbar-hide")],
};

export default config;
