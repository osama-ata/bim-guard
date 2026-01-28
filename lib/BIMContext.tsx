"use client";

import React, { createContext, useContext, useState, ReactNode } from "react";

interface BIMContextType {
    uploadedFile: File | null;
    setUploadedFile: (file: File | null) => void;
}

const BIMContext = createContext<BIMContextType | undefined>(undefined);

export function BIMProvider({ children }: { children: ReactNode }) {
    const [uploadedFile, setUploadedFile] = useState<File | null>(null);

    return (
        <BIMContext.Provider value={{ uploadedFile, setUploadedFile }}>
            {children}
        </BIMContext.Provider>
    );
}

export function useBIMContext() {
    const context = useContext(BIMContext);
    if (context === undefined) {
        throw new Error("useBIMContext must be used within a BIMProvider");
    }
    return context;
}
