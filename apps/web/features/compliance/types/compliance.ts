export type RuleType = "METADATA" | "SPATIAL" | "NOMENCLATURE";
export type IssueStatus = "OPEN" | "RESOLVED" | "FALSE_POSITIVE";
export type DocumentType = "BEP" | "BUILDING_CODE" | "CLIENT_STANDARD";

export interface Document {
  id: string;
  name: string;
  type: DocumentType;
  raw_text?: string;
  uploaded_at: string;
}

export interface Rule {
  id: string;
  document_id: string;
  category: string;
  type: RuleType;
  logic: Record<string, unknown>;
  confidence: number;
  source_text?: string;
  is_approved: boolean;
}

export interface ComplianceIssue {
  id: string;
  type: string;
  element_id: string;
  description: string;
  viewpoint: {
    position: [number, number, number];
    target: [number, number, number];
  };
  status: IssueStatus;
}

export interface ComplianceSummary {
  critical: number;
  warnings: number;
  passed: number;
}

export interface ComplianceResults {
  summary: ComplianceSummary;
  issues: ComplianceIssue[];
}

export interface IngestResponse {
  document_id: string;
  rules: {
    temp_id: string;
    category: string;
    type: RuleType;
    logic: Record<string, unknown>;
    confidence: number;
    source_text: string;
  }[];
}
