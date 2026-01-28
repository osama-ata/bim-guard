"use client";

import { useEffect, useRef } from "react";
import { StatsService } from "@/services";
import type { IStatsService } from "@/types";

interface ViewerStatsProps {
    containerRef: React.RefObject<HTMLElement | null>;
    onBeforeUpdate: (callback: () => void) => void;
    onAfterUpdate: (callback: () => void) => void;
}

/**
 * Performance stats overlay component
 * Shows FPS and frame timing
 */
export function ViewerStats({
    containerRef,
    onBeforeUpdate,
    onAfterUpdate
}: ViewerStatsProps) {
    const statsRef = useRef<IStatsService | null>(null);

    useEffect(() => {
        if (!containerRef.current) return;

        const stats = new StatsService();
        statsRef.current = stats;

        containerRef.current.appendChild(stats.getDom());

        onBeforeUpdate(() => stats.begin());
        onAfterUpdate(() => stats.end());

        return () => {
            stats.dispose();
            statsRef.current = null;
        };
    }, [containerRef, onBeforeUpdate, onAfterUpdate]);

    return null;
}
