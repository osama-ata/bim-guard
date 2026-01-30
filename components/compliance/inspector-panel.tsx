import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Check, X } from "lucide-react";

export function InspectorPanel() {
    return (
        <div className="flex h-full w-80 flex-col border-l bg-background">
            <div className="border-b p-4">
                <h3 className="font-semibold">Inspector</h3>
            </div>
            <div className="flex-1 overflow-auto p-4">
                <div className="space-y-4">
                    <div>
                        <h4 className="text-sm font-medium text-muted-foreground mb-1">Issue Details</h4>
                        <div className="text-lg font-bold">Clearance Violation</div>
                        <p className="text-sm text-destructive mt-1">Found 10mm, Required 50mm</p>
                    </div>

                    <Separator />

                    <div>
                        <h4 className="text-sm font-medium text-muted-foreground mb-1">Element</h4>
                        <div className="rounded-md bg-muted p-2 text-xs font-mono">
                            IfcWallStandardCase [23423]
                        </div>
                    </div>

                    <Separator />

                    <div>
                        <h4 className="text-sm font-medium text-muted-foreground mb-1">Source Rule</h4>
                        <p className="text-sm text-primary underline cursor-pointer">
                            BEP Section 4.1.2 - Fire Egress
                        </p>
                    </div>

                    <Tabs defaultValue="properties" className="w-full">
                        <TabsList className="w-full">
                            <TabsTrigger value="properties" className="flex-1">Props</TabsTrigger>
                            <TabsTrigger value="comments" className="flex-1">Comments</TabsTrigger>
                        </TabsList>
                        <TabsContent value="properties" className="pt-4">
                            <div className="space-y-2 text-xs">
                                <div className="flex justify-between">
                                    <span className="text-muted-foreground">GlobalId</span>
                                    <span className="font-mono">3lKj89...2k</span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-muted-foreground">Name</span>
                                    <span>Wall-Int-01</span>
                                </div>
                            </div>
                        </TabsContent>
                        <TabsContent value="comments" className="pt-4">
                            <p className="text-xs text-muted-foreground">No comments yet.</p>
                        </TabsContent>
                    </Tabs>
                </div>
            </div>
            <div className="border-t p-4 flex gap-2">
                <Button variant="outline" className="flex-1 text-xs">
                    <X className="mr-2 h-3 w-3" /> Ignore
                </Button>
                <Button className="flex-1 text-xs">
                    <Check className="mr-2 h-3 w-3" /> Mark Resolved
                </Button>
            </div>
        </div>
    );
}
