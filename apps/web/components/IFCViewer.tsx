"use client";

import { useRef, useEffect, useCallback, useState } from "react";
import * as THREE from "three";
import * as OBC from "@thatopen/components";

import { useBIMViewer, useCamera } from "@/hooks";
import { useBIMStore } from "@/store/useBIMStore";
import { IFCLoaderService } from "@/lib/ifcLoaderService";
import { FragmentsService, StatsService, SpatialTreeService } from "@/services";
import { ViewerContainer, ViewerToolbar } from "@/features/viewer/components";
import { DEFAULT_VIEWER_CONFIG } from "@/config";

/**
 * Main IFC Viewer component
 * Composes hooks and sub-components following SOLID principles
 */
export default function IFCViewer() {
    const containerRef = useRef<HTMLDivElement>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);
    const { components, world, isReady: isViewerReady } = useBIMViewer(containerRef);
    const uploadedFile = useBIMStore((state) => state.uploadedFile);
    const setSpatialTree = useBIMStore((state) => state.setSpatialTree);

    // Use camera hook
    const { fitToModelWithRetry } = useCamera(world?.camera ?? null);

    // Track initialization state
    const [isServicesReady, setIsServicesReady] = useState(false);

    // Service refs
    const loaderServiceRef = useRef<IFCLoaderService | null>(null);
    const fragmentsServiceRef = useRef<FragmentsService | null>(null);
    const statsServiceRef = useRef<StatsService | null>(null);

    // Initialize services when viewer is ready
    useEffect(() => {
        if (!isViewerReady || !components || !world) return;

        const initServices = async () => {
            // Create loader service first and initialize it
            const loaderService = new IFCLoaderService(components);
            await loaderService.init();
            loaderServiceRef.current = loaderService;

            // Create fragments service after FragmentsManager is initialized
            const fragmentsService = new FragmentsService(
                components.get(OBC.FragmentsManager),
                world.scene.three
            );
            fragmentsService.init();
            fragmentsServiceRef.current = fragmentsService;

            // Create stats service
            statsServiceRef.current = new StatsService();

            setIsServicesReady(true);
        };

        initServices();

        return () => {
            loaderServiceRef.current = null;
            fragmentsServiceRef.current = null;
            if (statsServiceRef.current) {
                statsServiceRef.current.dispose();
                statsServiceRef.current = null;
            }
            setIsServicesReady(false);
        };
    }, [isViewerReady, components, world]);

    // Setup fragments and camera sync
    useEffect(() => {
        if (!isServicesReady || !world || !fragmentsServiceRef.current) return;

        // Sync camera updates with fragments
        const handleCameraUpdate = () => {
            fragmentsServiceRef.current?.update();
        };
        world.camera.controls.addEventListener("update", handleCameraUpdate);

        // Handle model loading with auto-zoom
        const unsubscribe = fragmentsServiceRef.current.onModelLoaded(async (model) => {
            model.useCamera(world.camera.three);
            fragmentsServiceRef.current?.update(true);

            // Auto-zoom to model with retry
            if (DEFAULT_VIEWER_CONFIG.autoZoomOnLoad && model.object instanceof THREE.Object3D) {
                await fitToModelWithRetry(model.object);
            }

            // Extract and set spatial tree
            const tree = await SpatialTreeService.getSpatialTree(model);
            if (tree) {
                console.log("Spatial tree extracted successfully:", tree);
                setSpatialTree(tree);
            }
        });

        return () => {
            world.camera.controls.removeEventListener("update", handleCameraUpdate);
            unsubscribe();
        };
    }, [isServicesReady, world, fitToModelWithRetry, setSpatialTree]);

    // Load uploaded file if present
    useEffect(() => {
        if (!isServicesReady || !loaderServiceRef.current || !fragmentsServiceRef.current || !uploadedFile) return;

        const loadUploadedFile = async () => {
            console.log("Importing uploaded IFC file:", uploadedFile.name);
            // Clear existing models
            fragmentsServiceRef.current?.disposeAll();

            try {
                await loaderServiceRef.current!.importIFC(uploadedFile);
            } catch (error) {
                console.error("Failed to import IFC file:", error);
            }
        };

        loadUploadedFile();
    }, [isServicesReady, uploadedFile]);

    // Setup stats
    useEffect(() => {
        if (!isServicesReady || !containerRef.current || !world || !statsServiceRef.current) return;

        containerRef.current.appendChild(statsServiceRef.current.getDom());

        world.renderer.onBeforeUpdate.add(() => statsServiceRef.current?.begin());
        world.renderer.onAfterUpdate.add(() => statsServiceRef.current?.end());

        return () => {
            statsServiceRef.current?.dispose();
        };
    }, [isServicesReady, world]);

    // Handlers
    const handleImportIFC = useCallback(() => {
        fileInputRef.current?.click();
    }, []);

    const handleFileSelected = useCallback(async (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file && loaderServiceRef.current && fragmentsServiceRef.current) {
            console.log("Importing IFC file:", file.name, file.size, "bytes");

            // Clear existing models
            fragmentsServiceRef.current.disposeAll();

            try {
                const model = await loaderServiceRef.current.importIFC(file);
                console.log("IFC imported successfully:", model);
            } catch (error) {
                console.error("Failed to import IFC:", error);
            }
        }
    }, []);

    const handleExportFragments = useCallback(async () => {
        if (!fragmentsServiceRef.current || !loaderServiceRef.current) return;

        const modelId = fragmentsServiceRef.current.getFirstModelId();
        if (modelId) {
            await loaderServiceRef.current.downloadFragments(modelId);
        }
    }, []);

    const handleRemoveModel = useCallback(() => {
        if (fragmentsServiceRef.current) {
            fragmentsServiceRef.current.disposeAll();
        }
    }, []);

    const handleBackgroundChange = useCallback((color: THREE.Color) => {
        if (world) {
            world.scene.config.backgroundColor = color;
        }
    }, [world]);

    return (
        <ViewerContainer ref={containerRef}>
            <input
                type="file"
                ref={fileInputRef}
                style={{ display: "none" }}
                accept=".ifc"
                onChange={handleFileSelected}
            />
            {isServicesReady && world && (
                <ViewerToolbar
                    containerRef={containerRef}
                    onImportIFC={handleImportIFC}
                    onRemoveModel={handleRemoveModel}
                    onExportFragments={handleExportFragments}
                    onBackgroundChange={handleBackgroundChange}
                />
            )}
        </ViewerContainer>
    );
}
