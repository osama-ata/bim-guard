import { useMutation } from "@tanstack/react-query";
import { ComplianceResults } from "../types/compliance";

interface ComplianceCheckVariables {
  file: File;
  ruleSetIds: string[];
}

export const useComplianceCheck = () => {
  return useMutation<ComplianceResults, Error, ComplianceCheckVariables>({
    mutationFn: async ({ file, ruleSetIds }) => {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("rule_set_ids", JSON.stringify(ruleSetIds));

      const response = await fetch("http://localhost:8000/api/v1/compliance/check", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to run compliance check");
      }

      return response.json();
    },
  });
};
