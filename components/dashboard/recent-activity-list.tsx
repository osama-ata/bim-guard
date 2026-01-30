import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

export function RecentActivityList() {
    const activities = [
        {
            user: "Alice Smith",
            action: "uploaded",
            target: "Hospital Block A.ifc",
            time: "2 hours ago",
            initials: "AS",
        },
        {
            user: "Bob Jones",
            action: "updated rule",
            target: "Fire Safety Code - Sections 4.5",
            time: "4 hours ago",
            initials: "BJ",
        },
        {
            user: "Charlie Day",
            action: "ran analysis",
            target: "Office Tower - Phase 2",
            time: "yesterday",
            initials: "CD",
        },
        {
            user: "System",
            action: "extracted",
            target: "BEP_v2.pdf",
            time: "yesterday",
            initials: "AI",
        },
    ];

    return (
        <div className="space-y-8">
            {activities.map((activity, index) => (
                <div key={index} className="flex items-center">
                    <Avatar className="h-9 w-9">
                        <AvatarImage src="/avatars/01.png" alt="Avatar" />
                        <AvatarFallback>{activity.initials}</AvatarFallback>
                    </Avatar>
                    <div className="ml-4 space-y-1">
                        <p className="text-sm font-medium leading-none">
                            {activity.user}
                        </p>
                        <p className="text-sm text-muted-foreground">
                            {activity.action} <span className="font-semibold text-foreground">{activity.target}</span>
                        </p>
                    </div>
                    <div className="ml-auto font-medium text-sm text-muted-foreground">
                        {activity.time}
                    </div>
                </div>
            ))}
        </div>
    );
}
