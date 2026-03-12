import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { AlertCircle, AlertTriangle } from "lucide-react";
import { useBIMStore } from "../../../store/useBIMStore";

export function IssueSidebar() {
    const { complianceResults, setSelectedIssue } = useBIMStore();
    const issues = complianceResults?.issues || [];

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
                            onClick={() => setSelectedIssue(issue)}
                        >
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-2">
                                    {(issue.type === "CLEARANCE_VIOLATION" || issue.type === "NAMING_VIOLATION") ? (
                                        <AlertCircle className="h-4 w-4 text-destructive" />
                                    ) : (
                                        <AlertTriangle className="h-4 w-4 text-yellow-500" />
                                    )}
                                    <span className="font-medium text-sm">{issue.type}</span>
                                </div>
                                <Badge variant={issue.status === "OPEN" ? "destructive" : "outline"} className="text-[10px] h-5 px-1.5">
                                    {issue.status}
                                </Badge>
                            </div>
                            <div className="text-sm font-medium">{issue.element_id}</div>
                            <div className="text-xs text-muted-foreground">{issue.description}</div>
                        </div>
                    ))}
                </div>
            </ScrollArea>
        </div>
    );
}
