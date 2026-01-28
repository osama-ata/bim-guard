# BIM Guard

A professional IFC model viewer and validator built with Next.js and @thatopen/components.

## Getting Started

First, run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

---

## Development Conventions

This project follows **SOLID principles** for maintainability and testability.

### Architecture Overview

```
bim-guard/
├── app/                    # Next.js App Router pages
├── components/
│   ├── ui/                 # Shadcn UI components
│   ├── viewer/             # Viewer-specific components
│   │   ├── ViewerToolbar.tsx
│   │   ├── ViewerStats.tsx
│   │   └── ViewerContainer.tsx
│   ├── IFCViewer.tsx       # Main viewer (composed)
│   └── HomepageViewer.tsx
├── hooks/                  # React custom hooks
│   └── useBIMViewer.ts
├── services/               # Business logic services
│   ├── CameraService.ts
│   ├── FragmentsService.ts
│   └── StatsService.ts
├── lib/                    # Utilities and context
│   ├── ifcLoaderService.ts
│   └── BIMContext.tsx
├── types/                  # TypeScript interfaces
│   ├── services.ts
│   └── models.ts
└── public/lib/             # Static assets (WASM, workers)
```

### SOLID Principles Applied

| Principle | Implementation |
|-----------|----------------|
| **S**ingle Responsibility | Each service/component has one job |
| **O**pen/Closed | Extend via interfaces, not modification |
| **L**iskov Substitution | Services are interchangeable via interfaces |
| **I**nterface Segregation | Small, focused interfaces in `types/` |
| **D**ependency Inversion | Components depend on abstractions |

### Coding Guidelines

1. **Services must implement interfaces** defined in `types/services.ts`
2. **Components should compose**, not inherit - use sub-components
3. **Services require initialization** - always call `init()` before use
4. **Use refs for service instances** in React components to maintain stability
5. **Callbacks should be memoized** with `useCallback` to prevent re-renders

### Service Initialization Order

```typescript
// 1. Create and init loader service first (initializes FragmentsManager)
const loaderService = new IFCLoaderService(components);
await loaderService.init();

// 2. Create other services after FragmentsManager is ready
const fragmentsService = new FragmentsService(fragmentsManager, scene);
fragmentsService.init(); // Safe to call now

// 3. Camera and Stats services don't require async init
const cameraService = new CameraService(camera);
const statsService = new StatsService();
```

### Adding New Features

1. **Define interface first** in `types/services.ts`
2. **Create service** in `services/` implementing the interface
3. **Create UI component** in `components/viewer/` if needed
4. **Compose in parent** component using refs and proper initialization

### Key Dependencies

- `@thatopen/components` - BIM components library
- `@thatopen/fragments` - Fragment model handling
- `web-ifc` - IFC parsing engine
- `three` - 3D rendering

---

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [That Open Docs](https://docs.thatopen.com)
- [Three.js Documentation](https://threejs.org/docs)

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new).
