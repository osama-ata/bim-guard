"use client";

import { useQuery } from "@tanstack/react-query";
import { RuleDocument } from "@/types/rules";
import client from "@/services/api";
import { Loader2 } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function RulesManagerPage() {
    
    // Fetch rules from the new temporary FastAPI endpoint
    const { data: ruleDoc, isLoading, error } = useQuery<RuleDocument>({
        queryKey: ["compliance-rules"],
        queryFn: async () => {
            const { data, error } = await client.GET("/api/v1/rules/");
            if (error) {
                throw new Error("Failed to fetch rules");
            }
            return data as RuleDocument;
        }
    });

    return (
        <div className="container mx-auto py-6">
            <h1 className="text-3xl font-bold mb-4">Rule Manager</h1>
            <p className="text-muted-foreground mb-8">View and edit extracted validation rules.</p>

            {isLoading && (
                <div className="flex items-center gap-2 text-muted-foreground">
                    <Loader2 className="h-4 w-4 animate-spin" /> Loading rules...
                </div>
            )}

            {error && (
                <div className="text-red-500">
                    Failed to load rules. Make sure the backend API is running.
                </div>
            )}

            {ruleDoc && (
                <div className="flex flex-col gap-6">
                    <Card>
                        <CardHeader>
                            <CardTitle>{ruleDoc.name}</CardTitle>
                            <CardDescription>{ruleDoc.description}</CardDescription>
                        </CardHeader>
                    </Card>

                    <div className="grid gap-4 md:grid-cols-2">
                        {ruleDoc.categories.map((category) => (
                            <Card key={category.id}>
                                <CardHeader>
                                    <CardTitle className="text-lg">{category.name}</CardTitle>
                                </CardHeader>
                                <CardContent className="flex flex-col gap-4">
                                    {category.rules.map((rule) => (
                                        <div key={rule.id} className="p-4 rounded-lg border bg-muted/40 text-sm">
                                            <div className="flex justify-between items-start mb-2">
                                                <span className="font-semibold">{rule.reference}</span>
                                                <Badge variant="outline">{rule.type}</Badge>
                                            </div>
                                            <p className="mb-2 text-muted-foreground">{rule.description}</p>
                                            <div className="bg-background rounded p-2 border font-mono text-xs">
                                                Target: {rule.target_ifc_class}
                                                <br />
                                                Params: {JSON.stringify(rule.parameters)}
                                            </div>
                                        </div>
                                    ))}
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
