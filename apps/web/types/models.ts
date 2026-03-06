import * as OBC from "@thatopen/components";
import * as THREE from "three";

// Re-export config from the config directory
export {
    DEFAULT_VIEWER_CONFIG,
    CDN_URLS,
    LOCAL_PATHS,
    SAMPLE_MODELS,
    type ViewerConfig
} from "@/config";

/**
 * Represents the BIM world with its components
 */
export interface BIMWorld {
    scene: OBC.SimpleScene;
    camera: OBC.SimpleCamera;
    renderer: OBC.SimpleRenderer;
    full: OBC.World;
}

/**
 * Model load event data
 */
export interface ModelLoadEvent {
    modelId: string;
    object: THREE.Object3D;
}

/**
 * Camera position configuration
 */
export interface CameraPosition {
    eye: THREE.Vector3;
    target: THREE.Vector3;
}
