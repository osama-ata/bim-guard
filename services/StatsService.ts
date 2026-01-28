"use client";

import Stats from "stats.js";
import type { IStatsService } from "@/types";

/**
 * Service for performance statistics
 * Implements IStatsService interface
 */
export class StatsService implements IStatsService {
    private stats: Stats;

    constructor() {
        this.stats = new Stats();
        this.stats.showPanel(0); // 0: fps, 1: ms, 2: mb
        this.stats.dom.style.position = "absolute";
        this.stats.dom.style.top = "0";
        this.stats.dom.style.left = "0";
    }

    /**
     * Begin a frame measurement
     */
    begin(): void {
        this.stats.begin();
    }

    /**
     * End a frame measurement
     */
    end(): void {
        this.stats.end();
    }

    /**
     * Get the stats DOM element for mounting
     */
    getDom(): HTMLElement {
        return this.stats.dom;
    }

    /**
     * Dispose the stats service
     */
    dispose(): void {
        this.stats.dom.remove();
    }
}
