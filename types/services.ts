import * as THREE from "three";
import * as FRAGS from "@thatopen/fragments";

/**
 * Interface for the IFC Loader Service
 * Handles loading and exporting of IFC/Fragment models
 */
export interface ILoaderService {
    /**
     * Initialize the loader service
     */
    init(): Promise<void>;

    /**
     * Load fragment files from paths
     */
    loadFragments(paths: string[]): Promise<void>;

    /**
     * Import an IFC file
     */
    importIFC(file: File): Promise<FRAGS.FragmentsModel>;

    /**
     * Download a model as a fragment file
     */
    downloadFragments(modelId: string): Promise<void>;
}

/**
 * Interface for camera controls
 */
export interface ICameraService {
    /**
     * Fit the camera view to contain the given object
     */
    fitToModel(object: THREE.Object3D): void;

    /**
     * Set camera position and look target
     */
    setLookAt(
        eyeX: number, eyeY: number, eyeZ: number,
        targetX: number, targetY: number, targetZ: number
    ): Promise<void>;

    /**
     * Get the Three.js camera instance
     */
    getCamera(): THREE.PerspectiveCamera | THREE.OrthographicCamera;
}

/**
 * Interface for fragments management
 */
export interface IFragmentsService {
    /**
     * Subscribe to model loaded events
     */
    onModelLoaded(callback: (model: FRAGS.FragmentsModel) => void): () => void;

    /**
     * Get a model by its ID
     */
    getModel(id: string): FRAGS.FragmentsModel | undefined;

    /**
     * Get all loaded models
     */
    getAllModelIds(): string[];

    /**
     * Check if any models are loaded
     */
    hasModels(): boolean;

    /**
     * Update fragments rendering
     */
    update(force?: boolean): void;

    /**
     * Dispose all loaded models
     */
    disposeAll(): void;
}

/**
 * Interface for performance statistics
 */
export interface IStatsService {
    /**
     * Begin a frame measurement
     */
    begin(): void;

    /**
     * End a frame measurement
     */
    end(): void;

    /**
     * Get the stats DOM element for mounting
     */
    getDom(): HTMLElement;

    /**
     * Dispose the stats service
     */
    dispose(): void;
}
