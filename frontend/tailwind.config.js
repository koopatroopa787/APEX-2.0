/** @type {import('tailwindcss').Config} */
module.exports = {
    darkMode: 'class',
    content: [
        "./src/**/*.{js,jsx,ts,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                "primary": "#ff382e",
                "background-light": "#f8f5f5",
                "background-dark": "#000000",
                "panel-border": "#2A2A2A",
                "panel-bg": "rgba(20, 20, 20, 0.4)",
                "alert-red": "#FF3B30",
            },
            fontFamily: {
                display: ["Inter", "sans-serif"],
                mono: ['JetBrains Mono', 'monospace'],
            },
            animation: {
                'scan-y': 'scan-y 4s linear infinite',
                'marquee': 'marquee 20s linear infinite',
            },
            keyframes: {
                'scan-y': {
                    '0%': { transform: 'translateY(-100%)' },
                    '100%': { transform: 'translateY(100vh)' },
                },
                'marquee': {
                    '0%': { transform: 'translateX(100%)' },
                    '100%': { transform: 'translateX(-100%)' },
                }
            }
        },
    },
    plugins: [],
}
