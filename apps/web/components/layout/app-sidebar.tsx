"use client"

import * as React from "react"
import {
    BookOpen,
    Box,
    FileText,
    FolderPlus,
    LayoutDashboard,
    Play,
    Scale,
    Settings,
} from "lucide-react"

import {
    Sidebar,
    SidebarContent,
    SidebarFooter,
    SidebarGroup,
    SidebarGroupContent,
    SidebarGroupLabel,
    SidebarHeader,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
    SidebarRail,
} from "@/components/ui/sidebar"

// Navigation data
const data = {
    user: {
        name: "User Profile",
        email: "admin@bimguard.ai",
        avatar: "/avatars/shadcn.jpg",
    },
    navMain: [
        {
            title: "Platform",
            items: [
                {
                    title: "Dashboard",
                    url: "/dashboard",
                    icon: LayoutDashboard,
                },
                {
                    title: "New Project",
                    url: "/projects/new",
                    icon: FolderPlus,
                },
                {
                    title: "Viewer",
                    url: "/viewer",
                    icon: Box,
                },
            ],
        },
        {
            title: "Analysis",
            items: [
                {
                    title: "Run Analysis",
                    url: "/analysis/run",
                    icon: Play,
                },
                {
                    title: "Reports",
                    url: "/reports",
                    icon: FileText,
                },
            ],
        },
        {
            title: "Library",
            items: [
                {
                    title: "Documents",
                    url: "/library/documents",
                    icon: BookOpen,
                },
                {
                    title: "Rules",
                    url: "/library/rules",
                    icon: Scale,
                },
            ],
        },
    ],
}

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
    return (
        <Sidebar collapsible="icon" {...props}>
            <SidebarHeader>
                <div className="flex items-center gap-2 px-4 py-2">
                    <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
                        <Scale className="h-5 w-5" />
                    </div>
                    <span className="font-bold text-lg group-data-[collapsible=icon]:hidden">BIMGuard AI</span>
                </div>
            </SidebarHeader>
            <SidebarContent>
                {data.navMain.map((group) => (
                    <SidebarGroup key={group.title}>
                        <SidebarGroupLabel>{group.title}</SidebarGroupLabel>
                        <SidebarGroupContent>
                            <SidebarMenu>
                                {group.items.map((item) => (
                                    <SidebarMenuItem key={item.title}>
                                        <SidebarMenuButton asChild tooltip={item.title}>
                                            <a href={item.url}>
                                                <item.icon />
                                                <span>{item.title}</span>
                                            </a>
                                        </SidebarMenuButton>
                                    </SidebarMenuItem>
                                ))}
                            </SidebarMenu>
                        </SidebarGroupContent>
                    </SidebarGroup>
                ))}
            </SidebarContent>
            <SidebarFooter>
                <SidebarMenu>
                    <SidebarMenuItem>
                        <SidebarMenuButton asChild tooltip="Settings">
                            <a href="#">
                                <Settings />
                                <span>Settings</span>
                            </a>
                        </SidebarMenuButton>
                    </SidebarMenuItem>
                </SidebarMenu>
            </SidebarFooter>
            <SidebarRail />
        </Sidebar>
    )
}
