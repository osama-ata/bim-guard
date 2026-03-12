import json
import os
from pathlib import Path
from uuid import UUID
from typing import Optional, List
from ..models.compliance_models import ComplianceCheck

RESULTS_DIR = Path(__file__).parent.parent / "data" / "results"

class ResultStore:
    def __init__(self, storage_dir: Path = RESULTS_DIR):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    def save_result(self, result: ComplianceCheck):
        file_path = self.storage_dir / f"{result.id}.json"
        with open(file_path, "w") as f:
            f.write(result.model_dump_json())

    def get_result(self, check_id: UUID) -> Optional[ComplianceCheck]:
        file_path = self.storage_dir / f"{check_id}.json"
        if not file_path.exists():
            return None
        with open(file_path, "r") as f:
            data = json.load(f)
            return ComplianceCheck(**data)

    def list_results(self, limit: int = 20, offset: int = 0) -> List[dict]:
        results = []
        files = sorted(self.storage_dir.glob("*.json"), key=os.path.getmtime, reverse=True)
        for i in range(offset, min(offset + limit, len(files))):
            with open(files[i], "r") as f:
                data = json.load(f)
                # Return summary view
                results.append({
                    "id": data["id"],
                    "filename": data["filename"],
                    "status": data["status"],
                    "created_at": data["created_at"],
                    "compliance_score": data.get("summary", {}).get("passed", 0) / max(1, (data.get("summary", {}).get("critical", 0) + data.get("summary", {}).get("warnings", 0) + data.get("summary", {}).get("passed", 0))) * 100 if data.get("summary") else 0
                })
        return results
