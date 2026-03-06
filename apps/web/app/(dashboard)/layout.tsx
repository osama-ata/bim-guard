
import { AppSidebar } from "@/components/layout/app-sidebar";
import { AppHeader } from "@/components/layout/app-header";
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import React from "react";

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
            <SidebarProvider>
                <AppSidebar />
                <SidebarInset>
                    <div className="flex flex-col h-full bg-muted/40 font-sans">
                        <AppHeader />
                        <main className="flex-1 gap-4 p-4 sm:px-6 sm:py-4 md:gap-8 overflow-auto">
                            {children}
                        </main>
                    </div>
                </SidebarInset>
            </SidebarProvider>
    );
}
