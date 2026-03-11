import { create } from "zustand";

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
}

export const useBIMStore = create<BIMState>((set) => ({
  uploadedFile: null,
  setUploadedFile: (file) => set({ uploadedFile: file }),
  spatialTree: null,
  setSpatialTree: (tree) => set({ spatialTree: tree }),
}));
