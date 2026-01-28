"use client";

import { useRef, useEffect, useCallback, useState } from "react";
import * as OBC from "@thatopen/components";
import * as FRAGS from "@thatopen/fragments";
import * as THREE from "three";
import { FragmentsService } from "@/services";

interface UseFragmentsOptions {
    scene: THREE.Scene | null;
    camera: THREE.PerspectiveCamera | THREE.OrthographicCamera | null;
    onModelLoaded?: (model: FRAGS.FragmentsModel) => void;
}

interface UseFragmentsResult {
    fragmentsService: FragmentsService | null;
    isReady: boolean;
    modelIds: string[];
    update: (force?: boolean) => void;
}

/**
 * Custom hook for managing fragment models
 * Encapsulates FragmentsService logic for React components
 */
export function useFragments(
    components: OBC.Components | null,
    options: UseFragmentsOptions
): UseFragmentsResult {
    const { scene, camera, onModelLoaded } = options;
    const serviceRef = useRef<FragmentsService | null>(null);
    const [isReady, setIsReady] = useState(false);
    const [modelIds, setModelIds] = useState<string[]>([]);

    // Initialize service
    useEffect(() => {
        if (!components || !scene) return;

        const fragmentsManager = components.get(OBC.FragmentsManager);
        const service = new FragmentsService(fragmentsManager, scene);

        // Only initialize after FragmentsManager is ready
        if (fragmentsManager.initialized) {
            service.init();
            serviceRef.current = service;
            setIsReady(true);
        }

        return () => {
            serviceRef.current = null;
            setIsReady(false);
        };
    }, [components, scene]);

    // Handle model loaded events
    useEffect(() => {
        if (!isReady || !serviceRef.current) return;

        const unsubscribe = serviceRef.current.onModelLoaded((model) => {
            // Update model IDs list
            setModelIds(serviceRef.current?.getAllModelIds() ?? []);

            // Use camera for LOD updates
            if (camera) {
                model.useCamera(camera);
            }

            // Update fragments
            serviceRef.current?.update(true);

            // Call user callback
            onModelLoaded?.(model);
        });

        return unsubscribe;
    }, [isReady, camera, onModelLoaded]);

    // Update function
    const update = useCallback((force = false) => {
        serviceRef.current?.update(force);
    }, []);

    return {
        fragmentsService: serviceRef.current,
        isReady,
        modelIds,
        update,
    };
}
