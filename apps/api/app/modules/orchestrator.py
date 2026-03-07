from .module1_doc_reader import Module1_DocReader
from .module2_ifc_read import Module2_IFCRead
from .module3_rule_builder import Module3_RuleBuilder
from .module4_comparator import Module4_Comparator
from .module5_reporter import Module5_Reporter

class BIMGuard_App:
    """
    Workflow Orchestrator
    Manages the overall workflow connecting frontend requests to backend modules.
    """
    def __init__(self):
        self.doc_reader = Module1_DocReader()
        self.ifc_reader = Module2_IFCRead()
        self.rule_builder = Module3_RuleBuilder()
        self.comparator = Module4_Comparator()
        self.reporter = Module5_Reporter()

    def run_dashboard(self):
        """Run the main dashboard process."""
        pass

    def orchestrate_workflow(self):
        """Orchestrate the validation workflow across modules."""
        pass
