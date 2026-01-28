"use client";

import { useRef, useEffect, useCallback } from "react";
import * as OBC from "@thatopen/components";
import * as THREE from "three";
import { CameraService } from "@/services";

interface UseCameraResult {
    cameraService: CameraService | null;
    fitToModel: (object: THREE.Object3D) => void;
    fitToModelWithRetry: (object: THREE.Object3D) => Promise<boolean>;
    setLookAt: (
        eyeX: number, eyeY: number, eyeZ: number,
        targetX: number, targetY: number, targetZ: number
    ) => Promise<void>;
    getCamera: () => THREE.Camera | null;
}

/**
 * Custom hook for camera control
 * Encapsulates CameraService logic for React components
 */
export function useCamera(camera: OBC.SimpleCamera | null): UseCameraResult {
    const serviceRef = useRef<CameraService | null>(null);

    // Initialize service
    useEffect(() => {
        if (!camera) return;

        serviceRef.current = new CameraService(camera);

        return () => {
            serviceRef.current = null;
        };
    }, [camera]);

    // Fit camera to model
    const fitToModel = useCallback((object: THREE.Object3D) => {
        serviceRef.current?.fitToModel(object);
    }, []);

    // Fit camera to model with retry
    const fitToModelWithRetry = useCallback(async (object: THREE.Object3D): Promise<boolean> => {
        return serviceRef.current?.fitToModelWithRetry(object) ?? false;
    }, []);

    // Set camera look at position
    const setLookAt = useCallback(async (
        eyeX: number, eyeY: number, eyeZ: number,
        targetX: number, targetY: number, targetZ: number
    ) => {
        await serviceRef.current?.setLookAt(eyeX, eyeY, eyeZ, targetX, targetY, targetZ);
    }, []);

    // Get the Three.js camera
    const getCamera = useCallback(() => {
        return serviceRef.current?.getCamera() ?? null;
    }, []);

    return {
        cameraService: serviceRef.current,
        fitToModel,
        fitToModelWithRetry,
        setLookAt,
        getCamera,
    };
}
