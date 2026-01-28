"use client";

import React, { useRef } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { useBIMContext } from "@/lib/BIMContext";
import { Upload } from "lucide-react";

export function IFCUploadButton() {
    const fileInputRef = useRef<HTMLInputElement>(null);
    const { setUploadedFile } = useBIMContext();
    const router = useRouter();

    const handleButtonClick = () => {
        fileInputRef.current?.click();
    };

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            setUploadedFile(file);
            router.push("/viewer");
        }
    };

    return (
        <div className="flex flex-col items-center gap-2">
            <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileChange}
                accept=".ifc"
                className="hidden"
            />
            <Button
                onClick={handleButtonClick}
                size="lg"
                className="flex h-12 w-full items-center justify-center gap-2 rounded-full px-8 transition-all hover:scale-105 active:scale-95"
            >
                <Upload className="h-5 w-5" />
                Upload & View IFC
            </Button>
        </div>
    );
}
