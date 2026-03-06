"use client"

import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Check, X, Wand2 } from "lucide-react";

export function RuleEditorForm() {
    return (
        <Card className="h-full border-l-0 rounded-none shadow-none md:border-l md:rounded-lg">
            <CardHeader>
                <CardTitle>Rule Definition</CardTitle>
                <CardDescription>
                    Review and edit the extracted logic.
                </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
                <div className="space-y-2">
                    <Label htmlFor="rule-name">Rule Name</Label>
                    <Input id="rule-name" defaultValue="Wall Naming Convention" />
                </div>

                <div className="space-y-2">
                    <Label htmlFor="category">Category</Label>
                    <Select defaultValue="IfcWall">
                        <SelectTrigger id="category">
                            <SelectValue placeholder="Select Category" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="IfcWall">IfcWall</SelectItem>
                            <SelectItem value="IfcDoor">IfcDoor</SelectItem>
                            <SelectItem value="IfcWindow">IfcWindow</SelectItem>
                            <SelectItem value="IfcSlab">IfcSlab</SelectItem>
                        </SelectContent>
                    </Select>
                </div>

                <div className="space-y-2">
                    <Label htmlFor="logic">Logic (Regex / Python)</Label>
                    <div className="relative">
                        <Textarea
                            id="logic"
                            className="font-mono text-sm min-h-[100px]"
                            defaultValue="[A-Z]{3}-[0-9]{2}"
                        />
                        <Button size="icon" variant="ghost" className="absolute top-2 right-2 h-6 w-6 text-muted-foreground hover:text-primary">
                            <Wand2 className="h-4 w-4" />
                        </Button>
                    </div>
                </div>

                <div className="flex items-center gap-2 rounded-md border p-2 bg-muted/20">
                    <div className="h-2 w-2 rounded-full bg-green-500" />
                    <span className="text-sm font-medium">Confidence Score: 92%</span>
                </div>
            </CardContent>
            <CardFooter className="flex justify-between">
                <Button variant="outline" className="gap-2 text-destructive hover:bg-destructive/10">
                    <X className="h-4 w-4" /> Reject
                </Button>
                <Button className="gap-2">
                    <Check className="h-4 w-4" /> Approve Rule
                </Button>
            </CardFooter>
        </Card>
    );
}
