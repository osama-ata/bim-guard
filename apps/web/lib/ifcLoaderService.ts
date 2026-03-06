"use client";

import * as OBC from "@thatopen/components";
import * as FRAGS from "@thatopen/fragments";
import type { ILoaderService } from "@/types";
import { CDN_URLS } from "@/config";

/**
 * Service for loading IFC and Fragment files
 * Implements ILoaderService interface
 */
export class IFCLoaderService implements ILoaderService {
    private components: OBC.Components;
    private isInitialized: boolean = false;

    constructor(components: OBC.Components) {
        this.components = components;
    }

    /**
     * Initialize the loader service
     * Sets up FragmentsManager and IfcLoader with CDN resources
     */
    async init(): Promise<void> {
        if (this.isInitialized) return;

        const fragments = this.components.get(OBC.FragmentsManager);
        const loader = this.components.get(OBC.IfcLoader);

        // Initialize FragmentsManager with worker from CDN
        if (!fragments.initialized) {
            const fetchedUrl = await fetch(CDN_URLS.worker);
            const workerBlob = await fetchedUrl.blob();
            const workerFile = new File([workerBlob], "worker.mjs", { type: "text/javascript" });
            const workerObjectUrl = URL.createObjectURL(workerFile);
            fragments.init(workerObjectUrl);
        }

        // Configure IfcLoader with WASM from CDN (using absolute URL)
        await loader.setup({
            autoSetWasm: false,
            wasm: {
                path: CDN_URLS.wasm,
                absolute: true,
            },
        });

        this.isInitialized = true;
    }

    /**
     * Load fragment files from paths
     */
    async loadFragments(paths: string[]): Promise<void> {
        await this.ensureInitialized();

        const fragments = this.components.get(OBC.FragmentsManager);
        for (const path of paths) {
            const file = await fetch(path);
            const buffer = await file.arrayBuffer();
            fragments.core.load(new Uint8Array(buffer), { modelId: path });
        }
    }

    /**
     * Import an IFC file
     */
    async importIFC(file: File): Promise<FRAGS.FragmentsModel> {
        await this.ensureInitialized();

        const loader = this.components.get(OBC.IfcLoader);
        const buffer = await file.arrayBuffer();
        const model = await loader.load(new Uint8Array(buffer), true, file.name);
        return model;
    }

    /**
     * Convert IFC to Fragments using IfcImporter
     */
    async convertToFragments(file: File): Promise<Uint8Array> {
        const buffer = await file.arrayBuffer();
        const bytes = new Uint8Array(buffer);

        const serializer = new FRAGS.IfcImporter();
        serializer.wasm = {
            path: "/lib/",
            absolute: false
        };

        const result = await serializer.process({ bytes });
        return result;
    }

    /**
     * Download a model as a fragment file
     */
    async downloadFragments(modelId: string): Promise<void> {
        const fragments = this.components.get(OBC.FragmentsManager);
        const model = fragments.list.get(modelId);

        if (!model) {
            throw new Error(`Model with ID ${modelId} not found`);
        }

        const buffer = await model.getBuffer(false); // compressed
        const blob = new Blob([buffer], { type: "application/octet-stream" });
        const file = new File([blob], `${modelId}.frag`);

        const link = document.createElement("a");
        link.href = URL.createObjectURL(file);
        link.download = `${modelId}.frag`;
        link.click();
        URL.revokeObjectURL(link.href);
    }

    /**
     * Ensure the service is initialized before operations
     */
    private async ensureInitialized(): Promise<void> {
        if (!this.isInitialized) {
            await this.init();
        }
    }
}
