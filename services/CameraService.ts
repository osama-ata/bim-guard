"use client";

import * as THREE from "three";
import * as OBC from "@thatopen/components";
import type { ICameraService } from "@/types";

/**
 * Service for managing camera controls
 * Implements ICameraService interface
 */
export class CameraService implements ICameraService {
    private camera: OBC.SimpleCamera;

    constructor(camera: OBC.SimpleCamera) {
        this.camera = camera;
    }

    /**
     * Fit the camera view to contain the given object
     */
    fitToModel(object: THREE.Object3D): void {
        const box = new THREE.Box3().setFromObject(object);

        // Check if box is valid (not empty)
        if (box.isEmpty()) {
            console.warn("CameraService: Cannot fit to empty bounding box, skipping");
            return;
        }

        this.camera.controls.fitToBox(box, true);
    }

    /**
     * Fit the camera view with retry until geometry is available
     */
    async fitToModelWithRetry(object: THREE.Object3D, maxAttempts = 10, delayMs = 200): Promise<boolean> {
        for (let attempt = 0; attempt < maxAttempts; attempt++) {
            const box = new THREE.Box3().setFromObject(object);

            if (!box.isEmpty()) {
                this.camera.controls.fitToBox(box, true);
                console.log(`CameraService: Fitted to model on attempt ${attempt + 1}`);
                return true;
            }

            // Wait before retry
            await new Promise(resolve => setTimeout(resolve, delayMs));
        }

        console.warn("CameraService: Could not fit to model after max attempts");
        return false;
    }

    /**
     * Set camera position and look target
     */
    async setLookAt(
        eyeX: number, eyeY: number, eyeZ: number,
        targetX: number, targetY: number, targetZ: number
    ): Promise<void> {
        await this.camera.controls.setLookAt(eyeX, eyeY, eyeZ, targetX, targetY, targetZ);
    }

    /**
     * Get the Three.js camera instance
     */
    getCamera(): THREE.PerspectiveCamera | THREE.OrthographicCamera {
        return this.camera.three;
    }

    /**
     * Get the camera controls for advanced operations
     */
    getControls() {
        return this.camera.controls;
    }
}
