
import { IssueSidebar } from "@/features/compliance/components/issue-sidebar";
import { InspectorPanel } from "@/features/compliance/components/inspector-panel";
import { Viewer3DPlaceholder } from "@/features/compliance/components/viewer-3d-placeholder";

export default async function ComplianceResultsPage({
    params,
}: {
    params: Promise<{ id: string }>
}) {
    const { id } = await params

    return (
        <div className="flex flex-col h-[calc(100vh-4rem)] overflow-hidden">
            {/* Toolbar Area */}
            <div className="flex h-12 items-center justify-between border-b bg-background px-4">
                <span className="font-semibold text-sm">Results: <span className="font-normal text-muted-foreground">{id}</span></span>
                <div className="flex gap-2">
                    {/* Mock Toolbar items */}
                    <div className="h-6 w-24 bg-muted rounded animate-pulse" />
                    <div className="h-6 w-6 bg-muted rounded animate-pulse" />
                </div>
            </div>

            <div className="flex flex-1 overflow-hidden">
                {/* Left: Issues */}
                <IssueSidebar />

                {/* Center: 3D Canvas */}
                <div className="flex-1 relative">
                    <Viewer3DPlaceholder />
                </div>

                {/* Right: Inspector */}
                <InspectorPanel />
            </div>
        </div>
    );
}
