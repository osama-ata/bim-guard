import { useMutation } from "@tanstack/react-query";
import { IngestResponse } from "../types/compliance";

export const useRuleIngestion = () => {
  return useMutation<IngestResponse, Error, File>({
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://localhost:8000/api/v1/compliance/ingest", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to ingest document");
      }

      return response.json();
    },
  });
};
