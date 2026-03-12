import xml.etree.ElementTree as ET
from datetime import datetime
from uuid import uuid4
from typing import List
from app.models.compliance_models import ComplianceIssue

class BCFExporter:
    """
    Service to export compliance issues as BCF 2.1 (BIM Collaboration Format).
    """
    def generate_bcf_xml(self, issues: List[ComplianceIssue]) -> str:
        # Simplified BCF XML generation (Markup.bcf)
        # In a real app, this would be a zip file with multiple components (Viewpoints, Snapshots)
        
        root = ET.Element("Markup")
        header = ET.SubElement(root, "Header")
        file_node = ET.SubElement(header, "File")
        file_node.set("IfcGuid", "Multiple")
        ET.SubElement(file_node, "Date").text = datetime.now().isoformat()

        for issue in issues:
            topic = ET.SubElement(root, "Topic")
            topic.set("Guid", str(uuid4()))
            topic.set("TopicType", issue.type)
            topic.set("TopicStatus", issue.status)
            
            ET.SubElement(topic, "Title").text = f"{issue.type} on {issue.element_id}"
            ET.SubElement(topic, "Description").text = issue.description
            ET.SubElement(topic, "CreationDate").text = datetime.now().isoformat()
            ET.SubElement(topic, "CreationUser").text = "BIMGuard-AI"

        return ET.tostring(root, encoding="unicode")
