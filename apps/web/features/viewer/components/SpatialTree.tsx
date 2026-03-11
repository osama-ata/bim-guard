"use client";

import React, { useState } from "react";
import { ChevronRight, ChevronDown, Building2, Layers, MapPin, Home, Box } from "lucide-react";
import type { SpatialTreeNode } from "@/store/useBIMStore";

/** Map IFC type names to appropriate icons */
function getIconForType(type: string) {
    if (type === "IfcProject") return <Building2 className="h-4 w-4 shrink-0 text-blue-400" />;
    if (type === "IfcSite") return <MapPin className="h-4 w-4 shrink-0 text-green-400" />;
    if (type === "IfcBuilding") return <Home className="h-4 w-4 shrink-0 text-amber-400" />;
    if (type === "IfcBuildingStorey") return <Layers className="h-4 w-4 shrink-0 text-purple-400" />;
    return <Box className="h-4 w-4 shrink-0 text-muted-foreground" />;
}

/** Recursive node renderer */
function TreeNode({ node, depth = 0 }: { node: SpatialTreeNode; depth?: number }) {
    const hasChildren = node.children && node.children.length > 0;
    // Auto-expand the first 3 levels (Project, Site, Building)
    const [isOpen, setIsOpen] = useState(depth < 3);

    return (
        <div>
            <button
                onClick={() => hasChildren && setIsOpen(!isOpen)}
                className="flex w-full items-center gap-1.5 rounded-md px-1.5 py-1 text-left text-sm hover:bg-accent/50 transition-colors"
                style={{ paddingLeft: `${depth * 16 + 4}px` }}
                title={`${node.type} — ${node.globalId ?? "N/A"}`}
            >
                {/* Chevron or spacer */}
                {hasChildren ? (
                    isOpen ? (
                        <ChevronDown className="h-3.5 w-3.5 shrink-0 text-muted-foreground" />
                    ) : (
                        <ChevronRight className="h-3.5 w-3.5 shrink-0 text-muted-foreground" />
                    )
                ) : (
                    <span className="inline-block w-3.5" />
                )}

                {/* Type icon */}
                {getIconForType(node.type)}

                {/* Label */}
                <span className="truncate">{node.name}</span>

                {/* Child count badge */}
                {hasChildren && (
                    <span className="ml-auto shrink-0 rounded-full bg-muted px-1.5 py-0.5 text-[10px] text-muted-foreground">
                        {node.children.length}
                    </span>
                )}
            </button>

            {/* Children */}
            {isOpen && hasChildren && (
                <div>
                    {node.children.map((child, idx) => (
                        <TreeNode key={child.globalId ?? idx} node={child} depth={depth + 1} />
                    ))}
                </div>
            )}
        </div>
    );
}

/** Main Spatial Tree sidebar panel */
export function SpatialTree({ tree }: { tree: SpatialTreeNode | null }) {
    if (!tree) {
        return (
            <div className="flex h-full items-center justify-center p-4 text-sm text-muted-foreground">
                Upload an IFC file to view the model tree.
            </div>
        );
    }

    return (
        <div className="flex h-full flex-col">
            <div className="border-b px-3 py-2">
                <h3 className="text-sm font-semibold">Model Tree</h3>
            </div>
            <div className="flex-1 overflow-y-auto p-1">
                <TreeNode node={tree} />
            </div>
        </div>
    );
}
