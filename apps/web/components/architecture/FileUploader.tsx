import React from 'react';

/**
 * File Uploader (PDF Standards, BEPs, IFC Models)
 * Maps to the "File Uploader" block in the architecture diagram.
 */
export function FileUploader() {
    return (
        <div className="border rounded p-4 text-center">
            <h3>File Uploader</h3>
            <p className="text-sm text-gray-500">Upload PDF Standards, BEPs, and IFC Models here.</p>
            {/* TODO: Implement upload logic */}
            <input type="file" multiple className="mt-2" />
        </div>
    );
}
