"use client";

import React, { useState } from "react";
import { Check, ClipboardList, ShieldAlert } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useBIMStore } from "../../../store/useBIMStore";
import { API_BASE_URL } from "@/lib/apiConfig";

const MOCK_RULE_SETS = [
  {
    id: "obc_part9",
    name: "OBC Part 9 (Housing)",
    rules: 15,
    description: "Ontario Building Code requirements for small residential buildings."
  },
  {
    id: "iso_19650",
    name: "ISO 19650 (Naming)",
    rules: 8,
    description: "International standard for managing information over the whole life cycle of a built asset."
  }
];

export function RuleSetSelector() {
  const [selectedIds, setSelectedIds] = useState<string[]>(["obc_part9"]);
  const { uploadedFile, setComplianceResults, setComplianceCheckStatus } = useBIMStore();

  const toggleRuleSet = (id: string) => {
    setSelectedIds(prev => 
      prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]
    );
  };

  const handleRunCheck = async () => {
    if (!uploadedFile) return;

    setComplianceCheckStatus("processing");
    const formData = new FormData();
    formData.append("file", uploadedFile);
    formData.append("rule_set_ids", JSON.stringify(selectedIds));

    try {
      const response = await fetch(`${API_BASE_URL}/compliance/check`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Check failed");

      const results = await response.json();
      setComplianceResults(results);
      setComplianceCheckStatus("completed");
    } catch (error) {
      console.error(error);
      setComplianceCheckStatus("failed");
    }
  };

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center gap-2 mb-2">
        <ClipboardList className="h-5 w-5 text-blue-500" />
        <h3 className="text-lg font-semibold">Select Rule Sets</h3>
      </div>
      
      <div className="grid gap-3">
        {MOCK_RULE_SETS.map((set) => (
          <Card 
            key={set.id} 
            className={`cursor-pointer transition-colors ${selectedIds.includes(set.id) ? 'border-primary bg-primary/5' : ''}`}
            onClick={() => toggleRuleSet(set.id)}
          >
            <CardContent className="p-4 flex items-start gap-3">
              <div className={`mt-1 h-5 w-5 rounded-full border flex items-center justify-center ${selectedIds.includes(set.id) ? 'bg-primary border-primary text-primary-foreground' : 'bg-background'}`}>
                {selectedIds.includes(set.id) && <Check className="h-3 w-3" />}
              </div>
              <div className="flex-1">
                <p className="font-medium">{set.name}</p>
                <p className="text-xs text-muted-foreground">{set.description}</p>
                <span className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground mt-2 inline-block px-1.5 py-0.5 bg-muted rounded">
                  {set.rules} Rules
                </span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Button 
        className="w-full mt-4" 
        disabled={!uploadedFile || selectedIds.length === 0}
        onClick={handleRunCheck}
      >
        <ShieldAlert className="mr-2 h-4 w-4" />
        Run Compliance Check
      </Button>
    </div>
  );
}
