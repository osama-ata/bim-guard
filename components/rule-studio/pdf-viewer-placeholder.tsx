import { FileText } from "lucide-react";

export function PDFViewerPlaceholder() {
    return (
        <div className="flex h-full w-full flex-col items-center justify-center rounded-md border-2 border-dashed bg-muted/50 p-10">
            <FileText className="h-16 w-16 text-muted-foreground" />
            <h3 className="mt-4 text-lg font-semibold">PDF Document Viewer</h3>
            <p className="mt-2 text-center text-sm text-muted-foreground">
                Document content will be rendered here.
                <br />
                highlighed sections will correspond to extracted rules.
            </p>
        </div>
    );
}
