# Niriksh

Niriksh is a privacy-first, edge-AI retail intelligence platform. It turns existing CCTV and IP camera feeds into shelf, shopper, and queue intelligence while keeping raw-video processing on-site. The product experience follows a simple operating loop: **See → Understand → Predict → Act**.

## Stack

- React 19 and TypeScript
- Vite
- Tailwind CSS 4
- Framer Motion
- Lucide React

## Run locally

```bash
npm install
npm run dev
```

Create an optimized production build with `npm run build`, then preview it with `npm run preview`.

## Project structure

```text
src/
├── components/
│   ├── landing/   # Homepage sections and product visualizations
│   ├── layout/    # Navigation and footer
│   └── ui/        # Shared interface primitives
├── data/          # Product content and mock operational data
├── hooks/         # Reusable browser hooks
├── lib/           # Shared animation configuration
├── styles/        # Theme, section, and responsive styles
└── types/         # Shared TypeScript types
```

The interface respects `prefers-reduced-motion`, supports keyboard navigation, and uses only lightweight CSS/UI visualizations—no customer imagery or raw-video assets.
