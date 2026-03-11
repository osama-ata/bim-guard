"use client";

import * as FRAGS from "@thatopen/fragments";
import * as WEBIFC from "web-ifc";
import { SpatialTreeNode } from "@/store/useBIMStore";

/**
 * Service for extracting spatial structure from IFC models
 */
export class SpatialTreeService {
    /**
     * Extracts the spatial tree from a FragmentsModel
     * Follows the hierarchy: Project -> Site -> Building -> Storey -> Elements
     */
    static async getSpatialTree(model: FRAGS.FragmentsModel): Promise<SpatialTreeNode | null> {
        // In @thatopen/fragments, properties are accessed via getLocalProperties() or .properties if loaded
        const properties = (model as any).properties || (await model.getLocalProperties?.());
        
        if (!properties) {
            console.warn("Model has no properties, cannot extract spatial tree");
            return null;
        }

        try {
            const propValues = Object.values(properties);
            
            // Pre-filter relations to speed up traversal
            const aggregates = propValues.filter((p: any) => p.type === WEBIFC.IFCRELAGGREGATES);
            const containment = propValues.filter((p: any) => p.type === WEBIFC.IFCRELCONTAINEDINSPATIALSTRUCTURE);

            // Find the project (should be only one)
            const project = propValues.find(
                (prop: any) => prop.type === WEBIFC.IFCPROJECT
            );

            if (!project) {
                console.warn("No IfcProject found in model");
                return null;
            }

            return this.traverse(project, properties, aggregates, containment);
        } catch (error) {
            console.error("Failed to extract spatial tree:", error);
            return null;
        }
    }

    /**
     * Recursively traverse the IFC structure
     */
    private static traverse(
        element: any, 
        properties: any, 
        allAggregates: any[], 
        allContainment: any[]
    ): SpatialTreeNode {
        const typeMap: Record<number, string> = {
            [WEBIFC.IFCPROJECT]: "IfcProject",
            [WEBIFC.IFCSITE]: "IfcSite",
            [WEBIFC.IFCBUILDING]: "IfcBuilding",
            [WEBIFC.IFCBUILDINGSTOREY]: "IfcBuildingStorey",
            [WEBIFC.IFCWALL]: "IfcWall",
            [WEBIFC.IFCWALLSTANDARDCASE]: "IfcWallStandardCase",
            [WEBIFC.IFCDOOR]: "IfcDoor",
            [WEBIFC.IFCWINDOW]: "IfcWindow",
            [WEBIFC.IFCSLAB]: "IfcSlab",
            [WEBIFC.IFCCOLUMN]: "IfcColumn",
            [WEBIFC.IFCBEAM]: "IfcBeam",
            [WEBIFC.IFCSPACE]: "IfcSpace",
        };

        const typeName = typeMap[element.type] || "Unknown";
        
        const node: SpatialTreeNode = {
            globalId: element.GlobalId?.value || null,
            name: element.Name?.value || typeName || "Unnamed",
            type: typeName,
            children: [],
        };

        // Find children via IfcRelAggregates (Decomposition)
        const aggregates = allAggregates.filter(
            (rel: any) => rel.RelatingObject?.value === element.expressID
        );

        for (const rel of aggregates as any[]) {
            if (rel.RelatedObjects) {
                for (const childId of rel.RelatedObjects) {
                    const child = properties[childId.value];
                    if (child) {
                        node.children.push(this.traverse(child, properties, allAggregates, allContainment));
                    }
                }
            }
        }

        // Find children via IfcRelContainedInSpatialStructure (Containment)
        const containment = allContainment.filter(
            (rel: any) => rel.RelatingStructure?.value === element.expressID
        );

        for (const rel of containment as any[]) {
            if (rel.RelatedElements) {
                for (const childId of rel.RelatedElements) {
                    const child = properties[childId.value];
                    if (child) {
                        // Elements can also be decomposed, so we traverse them too
                        node.children.push(this.traverse(child, properties, allAggregates, allContainment));
                    }
                }
            }
        }

        return node;
    }
}
