/**
 * Viewer Configuration
 * Centralized settings for the BIM viewer
 */

export interface ViewerConfig {
    /** Path to the fragments worker */
    workerPath: string;
    /** Path to WASM files */
    wasmPath: string;
    /** Whether to use absolute URLs for WASM/worker */
    useAbsoluteUrls: boolean;
    /** Default background color (hex) */
    backgroundColor: number;
    /** Auto-zoom to model when loaded */
    autoZoomOnLoad: boolean;
    /** Camera fit retry settings */
    cameraFitRetry: {
        maxAttempts: number;
        delayMs: number;
    };
    /** Default camera position */
    defaultCameraPosition: {
        eye: [number, number, number];
        target: [number, number, number];
    };
}

/**
 * CDN URLs for That Open libraries
 */
export const CDN_URLS = {
    worker: "https://thatopen.github.io/engine_fragment/resources/worker.mjs",
    wasm: "https://unpkg.com/web-ifc@0.0.74/",
} as const;

/**
 * Local paths for development (if needed)
 */
export const LOCAL_PATHS = {
    worker: "/lib/worker.mjs",
    wasm: "/lib/",
} as const;

/**
 * Default viewer configuration
 */
export const DEFAULT_VIEWER_CONFIG: ViewerConfig = {
    workerPath: CDN_URLS.worker,
    wasmPath: CDN_URLS.wasm,
    useAbsoluteUrls: true,
    backgroundColor: 0x202932,
    autoZoomOnLoad: true,
    cameraFitRetry: {
        maxAttempts: 10,
        delayMs: 200,
    },
    defaultCameraPosition: {
        eye: [12, 6, 8],
        target: [0, 0, -10],
    },
};

/**
 * Sample models available in the application
 */
export const SAMPLE_MODELS = {
    schoolArq: "/models/school_arq.frag",
} as const;
