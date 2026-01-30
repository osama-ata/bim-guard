import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { AlertCircle, AlertTriangle } from "lucide-react";

export function IssueSidebar() {
    const issues = [
        {
            id: "C-1",
            severity: "critical",
            title: "Wall W-102 Clearance",
            description: "Clearance Violation",
        },
        {
            id: "C-2",
            severity: "critical",
            title: "Door D-404 Egress",
            description: "Width insufficient",
        },
        {
            id: "W-1",
            severity: "warning",
            title: "Window W-05 Naming",
            description: "Naming convention mismatch",
        },
        // Add more mock data as needed
        { id: "W-2", severity: "warning", title: "Slab S-22 Material", description: "Material not defined" },
        { id: "W-3", severity: "warning", title: "Beam B-11 Alignment", description: "Axis check failed" },
    ];

    return (
        <div className="flex h-full w-80 flex-col border-r bg-background">
            <div className="flex items-center justify-between border-b p-4">
                <h3 className="font-semibold">Issues Found</h3>
                <Badge variant="secondary">{issues.length}</Badge>
            </div>
            <ScrollArea className="flex-1">
                <div className="p-4 space-y-3">
                    {issues.map((issue) => (
                        <div
                            key={issue.id}
                            className="flex flex-col gap-2 rounded-lg border p-3 hover:bg-muted/50 cursor-pointer transition-colors"
                        >
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-2">
                                    {issue.severity === "critical" ? (
                                        <AlertCircle className="h-4 w-4 text-destructive" />
                                    ) : (
                                        <AlertTriangle className="h-4 w-4 text-yellow-500" />
                                    )}
                                    <span className="font-medium text-sm">{issue.id}</span>
                                </div>
                                <Badge variant={issue.severity === "critical" ? "destructive" : "outline"} className="text-[10px] h-5 px-1.5">
                                    {issue.severity}
                                </Badge>
                            </div>
                            <div className="text-sm font-medium">{issue.title}</div>
                            <div className="text-xs text-muted-foreground">{issue.description}</div>
                        </div>
                    ))}
                </div>
            </ScrollArea>
        </div>
    );
}
