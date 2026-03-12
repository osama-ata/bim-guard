import { create } from "zustand";
import { ComplianceIssue, ComplianceResults } from "../features/compliance/types/compliance";

export interface SpatialTreeNode {
  globalId: string | null;
  name: string;
  type: string;
  children: SpatialTreeNode[];
}

interface BIMState {
  uploadedFile: File | null;
  setUploadedFile: (file: File | null) => void;
  spatialTree: SpatialTreeNode | null;
  setSpatialTree: (tree: SpatialTreeNode | null) => void;
  // Compliance State
  complianceResults: ComplianceResults | null;
  setComplianceResults: (results: ComplianceResults | null) => void;
  selectedIssue: ComplianceIssue | null;
  setSelectedIssue: (issue: ComplianceIssue | null) => void;
  complianceCheckStatus: "idle" | "processing" | "completed" | "failed";
  setComplianceCheckStatus: (status: "idle" | "processing" | "completed" | "failed") => void;
}

export const useBIMStore = create<BIMState>((set) => ({
  uploadedFile: null,
  setUploadedFile: (file) => set({ uploadedFile: file }),
  spatialTree: null,
  setSpatialTree: (tree) => set({ spatialTree: tree }),
  // Compliance Implementation
  complianceResults: null,
  setComplianceResults: (results) => set({ complianceResults: results }),
  selectedIssue: null,
  setSelectedIssue: (issue) => set({ selectedIssue: issue }),
  complianceCheckStatus: "idle",
  setComplianceCheckStatus: (status) => set({ complianceCheckStatus: status }),
}));
