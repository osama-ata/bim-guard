"use client";

import * as OBC from "@thatopen/components";
import * as FRAGS from "@thatopen/fragments";
import * as THREE from "three";
import type { IFragmentsService } from "@/types";

/**
 * Service for managing fragment models
 * Implements IFragmentsService interface
 */
export class FragmentsService implements IFragmentsService {
    private fragmentsManager: OBC.FragmentsManager;
    private scene: THREE.Scene;
    private listeners: ((model: FRAGS.FragmentsModel) => void)[] = [];
    private isInitialized: boolean = false;

    constructor(fragmentsManager: OBC.FragmentsManager, scene: THREE.Scene) {
        this.fragmentsManager = fragmentsManager;
        this.scene = scene;
        // Don't setup listener here - wait for init()
    }

    /**
     * Initialize the service after FragmentsManager is ready
     * Must be called after FragmentsManager.init()
     */
    init(): void {
        if (this.isInitialized) return;

        this.fragmentsManager.list.onItemSet.add(({ value: model }) => {
            // Add model to scene
            this.scene.add(model.object);

            // Notify all listeners
            this.listeners.forEach(callback => callback(model));
        });

        this.isInitialized = true;
    }

    /**
     * Subscribe to model loaded events
     * Returns an unsubscribe function
     */
    onModelLoaded(callback: (model: FRAGS.FragmentsModel) => void): () => void {
        this.listeners.push(callback);
        return () => {
            const index = this.listeners.indexOf(callback);
            if (index > -1) {
                this.listeners.splice(index, 1);
            }
        };
    }

    /**
     * Get a model by its ID
     */
    getModel(id: string): FRAGS.FragmentsModel | undefined {
        return this.fragmentsManager.list.get(id);
    }

    /**
     * Get all loaded model IDs
     */
    getAllModelIds(): string[] {
        return Array.from(this.fragmentsManager.list.keys());
    }

    /**
     * Check if any models are loaded
     */
    hasModels(): boolean {
        return this.fragmentsManager.list.size > 0;
    }

    /**
     * Update fragments rendering
     */
    update(force: boolean = false): void {
        if (this.fragmentsManager.enabled) {
            this.fragmentsManager.core.update(force);
        }
    }

    /**
     * Get the first loaded model ID (convenience method)
     */
    getFirstModelId(): string | undefined {
        const ids = this.getAllModelIds();
        return ids.length > 0 ? ids[0] : undefined;
    }

    /**
     * Dispose all loaded models
     */
    disposeAll(): void {
        const ids = this.getAllModelIds();
        for (const id of ids) {
            const model = this.fragmentsManager.list.get(id);
            if (model) {
                this.fragmentsManager.list.delete(id);
                this.scene.remove(model.object);
                model.dispose();
            }
        }
    }
}
