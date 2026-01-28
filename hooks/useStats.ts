"use client";

import { useRef, useEffect, useCallback } from "react";
import { StatsService } from "@/services";

interface UseStatsOptions {
    container: HTMLElement | null;
    onBeforeUpdate?: () => void;
    onAfterUpdate?: () => void;
}

interface UseStatsResult {
    statsService: StatsService | null;
    begin: () => void;
    end: () => void;
}

/**
 * Custom hook for performance statistics
 * Encapsulates StatsService logic for React components
 */
export function useStats(options: UseStatsOptions): UseStatsResult {
    const { container, onBeforeUpdate, onAfterUpdate } = options;
    const serviceRef = useRef<StatsService | null>(null);

    // Initialize service and attach to container
    useEffect(() => {
        if (!container) return;

        const service = new StatsService();
        serviceRef.current = service;
        container.appendChild(service.getDom());

        return () => {
            service.dispose();
            serviceRef.current = null;
        };
    }, [container]);

    // Begin frame measurement
    const begin = useCallback(() => {
        serviceRef.current?.begin();
        onBeforeUpdate?.();
    }, [onBeforeUpdate]);

    // End frame measurement
    const end = useCallback(() => {
        serviceRef.current?.end();
        onAfterUpdate?.();
    }, [onAfterUpdate]);

    return {
        statsService: serviceRef.current,
        begin,
        end,
    };
}
