import { SidebarTrigger } from "@/components/ui/sidebar";
import { Separator } from "@/components/ui/separator";

export function AppHeader() {
    return (
        <header className="sticky top-0 z-30 flex h-14 items-center gap-4 border-b bg-background px-4 sm:h-auto sm:border-0 sm:bg-transparent sm:px-6">
            <SidebarTrigger />
            <Separator orientation="vertical" className="h-6" />
            <div className="flex-1">
                <h2 className="text-lg font-semibold">Compliance Dashboard</h2>
            </div>
            <div className="flex items-center gap-4">
                {/* Placeholders for notifications, search, etc. */}
                <span className="text-sm text-muted-foreground">v1.0.0</span>
            </div>
        </header>
    );
}
