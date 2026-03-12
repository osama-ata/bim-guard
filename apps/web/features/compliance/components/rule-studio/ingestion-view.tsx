"use client";

import React, { useState } from "react";
import { Upload, FileText, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { toast } from "sonner";
import { IngestResponse } from "../../types/compliance";
import { API_BASE_URL } from "@/lib/apiConfig";

export function IngestionView() {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [ingestData, setIngestData] = useState<IngestResponse | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setIsUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_BASE_URL}/compliance/ingest`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Upload failed");

      const data = await response.json();
      setIngestData(data);
      toast.success("Document ingested successfully. Review rules below.");
    } catch (error) {
      console.error(error);
      toast.error("Failed to ingest document");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="flex flex-col gap-6 p-6 h-full">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Rule Extraction Studio</h1>
        <div className="flex items-center gap-4">
          <input
            type="file"
            id="pdf-upload"
            className="hidden"
            accept=".pdf"
            onChange={handleFileChange}
          />
          <Button
            variant="outline"
            onClick={() => document.getElementById("pdf-upload")?.click()}
          >
            <Upload className="mr-2 h-4 w-4" />
            {file ? file.name : "Select BEP (PDF)"}
          </Button>
          <Button disabled={!file || isUploading} onClick={handleUpload}>
            {isUploading ? (
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            ) : (
              <FileText className="mr-2 h-4 w-4" />
            )}
            Extract Rules
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6 flex-1 min-h-0">
        <Card className="flex flex-col overflow-hidden">
          <CardHeader className="border-b bg-muted/50">
            <CardTitle className="text-sm font-medium">Document Preview</CardTitle>
          </CardHeader>
          <CardContent className="flex-1 p-0 bg-secondary/20">
            <div className="h-full flex items-center justify-center text-muted-foreground italic p-12 text-center">
              {file ? (
                `PDF Visualization for ${file.name} would be rendered here in a production environment.`
              ) : (
                "Upload a PDF to see it here."
              )}
            </div>
          </CardContent>
        </Card>

        <Card className="flex flex-col overflow-hidden">
          <CardHeader className="border-b bg-muted/50">
            <CardTitle className="text-sm font-medium">Extracted Rules (AI Candidates)</CardTitle>
          </CardHeader>
          <CardContent className="flex-1 p-0">
            <ScrollArea className="h-full">
              <div className="p-4 flex flex-col gap-4">
                {!ingestData ? (
                  <div className="text-center text-muted-foreground py-12">
                    Start extraction to see identified rules.
                  </div>
                ) : (
                  ingestData.rules.map((rule) => (
                    <Card key={rule.temp_id} className="border-l-4 border-l-blue-500 overflow-hidden">
                      <CardContent className="p-4 flex flex-col gap-2">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-bold uppercase tracking-wider text-muted-foreground">
                            {rule.type}
                          </span>
                          <span className="text-xs font-medium text-blue-600 bg-blue-50 px-2 py-0.5 rounded">
                            {Math.round(rule.confidence * 100)}% Confidence
                          </span>
                        </div>
                        <p className="text-sm font-semibold">{rule.category} Constraint</p>
                        <p className="text-sm text-muted-foreground italic border-l-2 pl-3 py-1 bg-muted/30">
                          &quot;{rule.source_text}&quot;
                        </p>
                        <pre className="text-xs bg-muted p-2 rounded overflow-x-auto">
                          {JSON.stringify(rule.logic, null, 2)}
                        </pre>
                        <div className="flex justify-end gap-2 mt-2">
                          <Button variant="outline" size="sm">Edit</Button>
                          <Button size="sm">Approve</Button>
                        </div>
                      </CardContent>
                    </Card>
                  ))
                )}
              </div>
            </ScrollArea>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
