"use client";

import { useRef } from "react";
import { useBIMViewer } from "@/hooks/useBIMViewer";

export default function HomepageViewer() {
    const containerRef = useRef<HTMLDivElement>(null);

    // Use the viewer with default settings (includes grid)
    useBIMViewer(containerRef, {
        createGrid: true,
        cameraPosition: {
            eye: [74, 16, 0.2],
            target: [30, -4, 27],
        },
        backgroundColor: 0x202932,
    });

    return (
        <div
            ref={containerRef}
            id="container"
            className="absolute inset-0 -z-10 opacity-50 grayscale transition-opacity duration-1000"
        />
    );
}
