"use client";

import dynamic from "next/dynamic";
import { useBIMStore } from "@/store/useBIMStore";
import { SpatialTree } from "@/features/viewer/components/SpatialTree";

// This is the magic part: ssr: false prevents the 'HTMLElement' error
const IFCViewer = dynamic(() => import("@/components/IFCViewer"), {
    ssr: false,
    loading: () => <p>Loading 3D Engine...</p>
});

export default function ViewerPage() {
    const spatialTree = useBIMStore((state) => state.spatialTree);

    return (
        <main className="flex h-[calc(100vh-4rem)]">
            {/* Left sidebar — Spatial Tree */}
            <aside className="w-72 shrink-0 overflow-hidden border-r bg-background">
                <SpatialTree tree={spatialTree} />
            </aside>

            {/* 3D Viewer fills remaining space */}
            <div className="flex-1">
                <IFCViewer />
            </div>
        </main>
    );
}