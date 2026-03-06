export interface RuleParameter {
    [key: string]: string | number | boolean;
}

export interface ComplianceRule {
    id: string;
    reference: string;
    description: string;
    parameters: RuleParameter;
    type: string;
    target_ifc_class: string;
}

export interface RuleCategory {
    id: string;
    name: string;
    rules: ComplianceRule[];
}

export interface RuleDocument {
    id: string;
    name: string;
    description: string;
    categories: RuleCategory[];
}
