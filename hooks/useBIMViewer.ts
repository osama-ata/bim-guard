"use client";

import { useRef, useEffect, useState } from "react";
import * as OBC from "@thatopen/components";

export interface BIMWorld {
    scene: OBC.SimpleScene;
    camera: OBC.SimpleCamera;
    renderer: OBC.SimpleRenderer;
    /** Full world object for components that require it (e.g., Grids) */
    full: OBC.World;
}

interface UseBIMViewerOptions {
    /** Whether to create a grid */
    createGrid?: boolean;
    /** Initial camera position */
    cameraPosition?: {
        eye: [number, number, number];
        target: [number, number, number];
    };
    /** Background color (null for transparent) */
    backgroundColor?: number | null;
}

interface UseBIMViewerResult {
    components: OBC.Components | null;
    world: BIMWorld | null;
    isReady: boolean;
}

const DEFAULT_OPTIONS: UseBIMViewerOptions = {
    createGrid: true,
    cameraPosition: {
        eye: [74, 16, 0.2],
        target: [30, -4, 27],
    },
    backgroundColor: null,
};

/**
 * Custom hook for initializing the BIM viewer
 * Follows the official That Open documentation pattern
 */
export function useBIMViewer(
    containerRef: React.RefObject<HTMLDivElement | null>,
    options: UseBIMViewerOptions = {}
): UseBIMViewerResult {
    const mergedOptions = { ...DEFAULT_OPTIONS, ...options };
    const componentsRef = useRef<OBC.Components | null>(null);
    const worldRef = useRef<BIMWorld | null>(null);
    const [isReady, setIsReady] = useState(false);

    useEffect(() => {
        const container = containerRef.current;
        if (!container) return;

        // Initialize components
        const components = new OBC.Components();
        componentsRef.current = components;

        // Create worlds manager
        const worlds = components.get(OBC.Worlds);

        // Create a simple 3D world
        const world = worlds.create<
            OBC.SimpleScene,
            OBC.SimpleCamera,
            OBC.SimpleRenderer
        >();

        // Setup scene
        world.scene = new OBC.SimpleScene(components);
        world.scene.setup();
        world.scene.three.background = mergedOptions.backgroundColor !== null
            ? new (require("three").Color)(mergedOptions.backgroundColor)
            : null;

        // Setup renderer
        world.renderer = new OBC.SimpleRenderer(components, container);

        // Setup camera
        world.camera = new OBC.SimpleCamera(components);
        if (mergedOptions.cameraPosition) {
            const { eye, target } = mergedOptions.cameraPosition;
            world.camera.controls.setLookAt(eye[0], eye[1], eye[2], target[0], target[1], target[2]);
        }

        // Initialize components
        components.init();

        // Create grid if requested
        if (mergedOptions.createGrid) {
            const grids = components.get(OBC.Grids);
            const grid = grids.create(world);
            // Ensure grid is visible
            if (mergedOptions.backgroundColor === null) {
                // If transparent background, grid lines should be visible
                // Grids usually have default colors, but transparency might need attention
            }
        }

        // Handle resize
        const resizeObserver = new ResizeObserver(() => {
            if (world.renderer) world.renderer.resize();
            if (world.camera) world.camera.updateAspect();
        });
        resizeObserver.observe(container);

        // Store world reference
        worldRef.current = {
            scene: world.scene,
            camera: world.camera,
            renderer: world.renderer,
            full: world,
        };

        // Mark as ready
        setIsReady(true);

        // Cleanup
        return () => {
            resizeObserver.disconnect();
            components.enabled = false;
            components.dispose();
            componentsRef.current = null;
            worldRef.current = null;
            setIsReady(false);
        };
    }, [containerRef]);

    return {
        components: componentsRef.current,
        world: worldRef.current,
        isReady,
    };
}
