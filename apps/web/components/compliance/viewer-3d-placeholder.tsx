"use client";

import { Box } from "lucide-react";

export function Viewer3DPlaceholder() {
    return (
        <div className="relative h-full w-full bg-neutral-900 flex flex-col items-center justify-center text-neutral-400">
            <div className="absolute inset-0 grid grid-cols-[repeat(20,minmax(0,1fr))] grid-rows-[repeat(20,minmax(0,1fr))] opacity-10 pointer-events-none">
                {Array.from({ length: 400 }).map((_, i) => (
                    <div key={i} className="border-[0.5px] border-neutral-700" />
                ))}
            </div>

            <Box className="h-24 w-24 mb-4 text-primary animate-pulse" />
            <h3 className="text-xl font-bold text-white">3D Viewer Canvas</h3>
            <p className="text-sm max-w-md text-center mt-2 px-4">
                IfcOpenShell / WebIFC rendering context will be initialized here.
                <br />
                Geometry and 'Halo' visualizations will be drawn on this layer.
            </p>

            <div className="absolute bottom-4 left-4 bg-black/50 backdrop-blur-sm p-2 rounded-md text-xs font-mono">
                FPS: 60 | Draw Calls: 0
            </div>
        </div>
    );
}
