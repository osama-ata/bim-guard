"use client";

import dynamic from "next/dynamic";

// This is the magic part: ssr: false prevents the 'HTMLElement' error
const IFCViewer = dynamic(() => import("@/components/IFCViewer"), {
    ssr: false,
    loading: () => <p>Loading 3D Engine...</p>
});

export default function ViewerPage() {
    return (
        <main>
            <IFCViewer />
        </main>
    );
}