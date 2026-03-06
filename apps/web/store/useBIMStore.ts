import { create } from "zustand";

interface BIMState {
  uploadedFile: File | null;
  setUploadedFile: (file: File | null) => void;
}

export const useBIMStore = create<BIMState>((set) => ({
  uploadedFile: null,
  setUploadedFile: (file) => set({ uploadedFile: file }),
}));
