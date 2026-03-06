"use client";

import { forwardRef } from "react";

interface ViewerContainerProps {
    className?: string;
    children?: React.ReactNode;
}

/**
 * Pure container component for the 3D canvas
 * Handles the DOM element that Three.js renders into
 */
export const ViewerContainer = forwardRef<HTMLDivElement, ViewerContainerProps>(
    function ViewerContainer({ className = "", children }, ref) {
        return (
            <div
                ref={ref}
                className={className}
                style={{
                    width: "100vw",
                    height: "100vh",
                    position: "relative"
                }}
            >
                {children}
            </div>
        );
    }
);
