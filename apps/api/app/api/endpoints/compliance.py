from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
import json
from uuid import uuid4, UUID
from pathlib import Path
import os
from app.models.compliance_models import ComplianceCheck, IssueStatus
from app.services.result_store import ResultStore
from app.modules.module1_doc_reader import DocReader
from apps.api.app.modules.module3_rule_builder.module3_rule_builder_mock import RuleBuilder

from app.services.compliance_engine import ComplianceEngine
from app.models.rule_models import Rule, RuleType

from app.services.bcf_exporter import BCFExporter
from fastapi.responses import Response
from pydantic import BaseModel

router = APIRouter(prefix="/compliance", tags=["compliance"])
result_store = ResultStore()
doc_reader = DocReader()
rule_builder = RuleBuilder()
compliance_engine = ComplianceEngine()
bcf_exporter = BCFExporter()


class IssueStatusUpdatePayload(BaseModel):
    status: IssueStatus


@router.get("/checks/{check_id}/bcf")
async def export_check_bcf(check_id: UUID):
    check = result_store.get_result(check_id)
    if not check or not check.issues:
        raise HTTPException(status_code=404, detail="Compliance check or issues not found")
    
    xml_content = bcf_exporter.generate_bcf_xml(check.issues)
    return Response(content=xml_content, media_type="application/xml", headers={
        "Content-Disposition": f"attachment; filename=compliance-{check_id}.bcf"
    })

@router.patch("/checks/{check_id}/issues/{issue_id}")
async def update_issue_status(check_id: UUID, issue_id: str, payload: IssueStatusUpdatePayload):
    check = result_store.get_result(check_id)
    if not check or not check.issues:
        raise HTTPException(status_code=404, detail="Compliance check not found")

    status = payload.status
    
    for issue in check.issues:
        if issue.id == issue_id:
            issue.status = status
            result_store.save_result(check)
            return issue
            
    raise HTTPException(status_code=404, detail="Issue not found")

@router.post("/check", response_model=ComplianceCheck)
async def run_compliance_check(
    file: UploadFile = File(...),
    rule_set_ids: str = Form(...)
):
    try:
        json.loads(rule_set_ids)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid rule_set_ids format. Expected JSON array.")

    # Save file temporarily
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    temp_path = temp_dir / file.filename
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        # Mocking rule retrieval - in real app, fetch from DB by rule_ids
        # For US2 demo, we'll create a few rules based on the ids
        mock_rules = [
            Rule(
                id=uuid4(),
                document_id=uuid4(),
                category="IfcWall",
                type=RuleType.NOMENCLATURE,
                logic={"pattern": "^W-.*"},
                confidence=1.0,
                is_approved=True
            )
        ]

        check_result = compliance_engine.run_check(temp_path, mock_rules)
        check_result.filename = file.filename
        result_store.save_result(check_result)
        return check_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Compliance check failed: {str(e)}")
    finally:
        if temp_path.exists():
            os.remove(temp_path)

@router.get("/checks", response_model=List[dict])
async def list_checks(limit: int = 20, offset: int = 0):
    return result_store.list_results(limit=limit, offset=offset)

@router.get("/checks/{check_id}", response_model=ComplianceCheck)
async def get_check_details(check_id: UUID):
    check = result_store.get_result(check_id)
    if not check:
        raise HTTPException(status_code=404, detail="Compliance check not found")
    return check

@router.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    # Local path for processing
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    safe_suffix = Path(os.path.basename(file.filename or "")).suffix or ""
    temp_path = temp_dir / f"{uuid4()}{safe_suffix}"
    
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    
    try:
        text = doc_reader.extract_text(temp_path)
        rules = rule_builder.extract_rules_mock(text)
        return {
            "document_id": str(uuid4()),
            "rules": rules
        }
    finally:
        if temp_path.exists():
            os.remove(temp_path)
