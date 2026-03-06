
import { StatsPanel } from "@/components/dashboard/stats-panel";
import { RecentActivityList } from "@/components/dashboard/recent-activity-list";
import { Button } from "@/components/ui/button";
import { PlusCircle } from "lucide-react";
import Link from "next/link";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export default function Home() {
  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight">Dashboard</h1>
        <div className="flex items-center gap-2">
          <Link href="/projects/new">
            <Button size="sm" className="gap-1">
              <PlusCircle className="h-3.5 w-3.5" />
              <span className="sr-only sm:not-sr-only sm:whitespace-nowrap">
                New Compliance Check
              </span>
            </Button>
          </Link>
        </div>
      </div>

      <StatsPanel />

      <div className="grid gap-4 md:gap-8 lg:grid-cols-2 xl:grid-cols-3">
        <Card className="xl:col-span-2">
          <CardHeader className="flex flex-row items-center">
            <div className="grid gap-2">
              <CardTitle>Recent Activity</CardTitle>
              <CardDescription>
                Recent transactions and system updates.
              </CardDescription>
            </div>
            <Button asChild size="sm" className="ml-auto gap-1">
              <Link href="/reports">
                View All
              </Link>
            </Button>
          </CardHeader>
          <CardContent>
            <RecentActivityList />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-2">
            <Button variant="outline" className="w-full justify-start text-left font-normal" asChild>
              <Link href="/viewer">
                Upload IFC Model
              </Link>
            </Button>
            <Button variant="outline" className="w-full justify-start text-left font-normal">
              Upload BEP Document
            </Button>
            <Button variant="outline" className="w-full justify-start text-left font-normal">
              Review Flagged Issues
            </Button>
            <Button variant="outline" className="w-full justify-start text-left font-normal">
              Generate Weekly Report
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
