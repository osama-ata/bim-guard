import { PDFViewerPlaceholder } from "@/components/rule-studio/pdf-viewer-placeholder";
import { RuleEditorForm } from "@/components/rule-studio/rule-editor-form";
import { Separator } from "@/components/ui/separator";

export default function RuleExtractionPage() {
    return (
        <div className="flex flex-col h-[calc(100vh-4rem)] overflow-hidden">
            <div className="flex items-center justify-between px-6 py-3 border-b bg-background">
                <div>
                    <h1 className="text-lg font-semibold">Rule Extraction Studio</h1>
                    <p className="text-xs text-muted-foreground">ISO 19650 Naming Convention.pdf</p>
                </div>
                <div className="text-sm text-muted-foreground">
                    Auto-saving...
                </div>
            </div>

            <div className="flex flex-1 overflow-hidden">
                {/* Left Panel: Source Document */}
                <div className="flex-1 bg-muted/30 p-4 overflow-auto">
                    <PDFViewerPlaceholder />
                </div>

                <Separator orientation="vertical" className="w-[1px]" />

                {/* Right Panel: Rule Logic */}
                <div className="w-full md:w-[400px] lg:w-[450px] bg-background border-l overflow-y-auto">
                    <RuleEditorForm />
                </div>
            </div>
        </div>
    );
}
