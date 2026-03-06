"use client";

import * as THREE from "three";
import * as BUI from "@thatopen/ui";
import { useEffect, useRef } from "react";

interface ViewerToolbarProps {
    onImportIFC: () => void;
    onExportFragments: () => void;
    onRemoveModel: () => void;
    onBackgroundChange: (color: THREE.Color) => void;
    containerRef: React.RefObject<HTMLElement | null>;
}

/**
 * Toolbar component for the BIM viewer
 * Handles controls panel with import/export buttons
 */
export function ViewerToolbar({
    onImportIFC,
    onExportFragments,
    onRemoveModel,
    onBackgroundChange,
    containerRef
}: ViewerToolbarProps) {
    const panelRef = useRef<BUI.PanelSection | null>(null);

    useEffect(() => {
        BUI.Manager.init();

        const panel = BUI.Component.create<BUI.PanelSection>(() => {
            return BUI.html`
                <bim-panel label="BIM Guard Viewer" style="position: fixed; top: 10px; right: 10px;">
                    <bim-panel-section label="Controls">
                        <bim-label style="white-space: normal; margin-bottom: 8px;">🚀 The IFC has been converted to Fragments. Controls ready!</bim-label>
                        
                        <bim-color-input 
                            label="Background" 
                            color="#202932" 
                            @input="${({ target }: { target: BUI.ColorInput }) => {
                    onBackgroundChange(new THREE.Color(target.color));
                }}">
                        </bim-color-input>
                        
                        <bim-button label="Import IFC" @click="${onImportIFC}"></bim-button>
                        <bim-button label="Remove Model" @click="${onRemoveModel}"></bim-button>
                        <bim-button label="Download Fragments" @click="${onExportFragments}"></bim-button>
                    </bim-panel-section>
                </bim-panel>
            `;
        });

        panelRef.current = panel;
        containerRef.current?.appendChild(panel);

        return () => {
            panel.remove();
        };
    }, [onImportIFC, onExportFragments, onBackgroundChange, containerRef]);

    return null;
}
