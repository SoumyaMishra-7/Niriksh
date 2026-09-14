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

## Backend and live demo

```bash
cd backend
python -m pip install -r requirements.txt
python -m app.db.seed
uvicorn app.main:app --reload
```

API documentation is at `http://localhost:8000/docs`. Start the deterministic live scenario with `POST /api/v1/demo/start`; use `/demo/reset` to restore seed data and `/demo/connectivity` to demonstrate offline metadata queuing. The frontend connects through `src/services/api` and `useNirikshLiveStore`.

## Edge vision

The independently runnable [`edge/`](edge/) package converts video files, webcams, or RTSP streams into privacy-safe shelf, footfall, dwell, heatmap, queue, and camera-health observations. See [`edge/README.md`](edge/README.md) for model setup, demo commands, privacy behavior, evaluation utilities, and the future Qualcomm QAIRT/QNN path.
