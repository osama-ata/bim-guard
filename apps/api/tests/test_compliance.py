import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
REPO_ROOT = Path(__file__).resolve().parents[3]
SAMPLE_IFC = REPO_ROOT / "IFC-Sample-Test-Files/IFC 4.0.2.1 (IFC 4)/ISO Spec - ReferenceView_V1.2/wall-with-opening-and-window.ifc"


def test_ingest_pdf(tmp_path):
    # create a tiny PDF using reportlab if available, else fallback to blank content
    pdf_path = tmp_path / "test.pdf"
    try:
        from reportlab.pdfgen import canvas

        c = canvas.Canvas(str(pdf_path))
        c.drawString(100, 750, "This is a sample naming convention: W-123")
        c.save()
    except ImportError:
        pdf_path.write_bytes(b"%PDF-1.4\n%%EOF")

    with open(pdf_path, "rb") as f:
        response = client.post(
            "/api/v1/compliance/ingest",
            files={"file": ("test.pdf", f, "application/pdf")},
        )
    assert response.status_code == 200
    data = response.json()
    assert "document_id" in data
    assert "rules" in data


def test_compliance_check(tmp_path):
    sample_ifc = SAMPLE_IFC
    assert sample_ifc.exists(), "Sample IFC file must exist for test"

    with sample_ifc.open("rb") as f:
        response = client.post(
            "/api/v1/compliance/check",
            data={"rule_set_ids": json.dumps(["iso_19650"])},
            files={"file": ("model.ifc", f, "application/octet-stream")},
        )
    assert response.status_code == 200
    data = response.json()
    assert "issues" in data
    assert data["filename"] == "model.ifc"


def test_bcf_export_and_patch(tmp_path):
    # run a check first
    sample_ifc = SAMPLE_IFC
    with sample_ifc.open("rb") as f:
        resp = client.post(
            "/api/v1/compliance/check",
            data={"rule_set_ids": json.dumps(["iso_19650"])},
            files={"file": ("model.ifc", f, "application/octet-stream")},
        )
    assert resp.status_code == 200
    check = resp.json()
    check_id = check["id"]
    issues = check.get("issues", [])
    if not issues:
        pytest.skip("No issues generated from mock evaluator")

    issue_id = issues[0]["id"]
    # patch issue status
    resp = client.patch(
        f"/api/v1/compliance/checks/{check_id}/issues/{issue_id}",
        json={"status": "RESOLVED"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "RESOLVED"

    # export bcf
    resp = client.get(f"/api/v1/compliance/checks/{check_id}/bcf")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/xml"
    assert "<Markup" in resp.text


def test_list_and_get_details():
    resp = client.get("/api/v1/compliance/checks")
    assert resp.status_code == 200
    listings = resp.json()
    assert isinstance(listings, list)

    if listings:
        first = listings[0]
        detail_resp = client.get(f"/api/v1/compliance/checks/{first['id']}")
        assert detail_resp.status_code == 200
        detail = detail_resp.json()
        assert detail["id"] == first["id"]
