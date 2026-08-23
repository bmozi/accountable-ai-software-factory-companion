"""Compatibility import for the canonical accountable-factory package.

The v1.0 example had an independent data model. v1.1 deliberately exposes one
implementation so schemas, examples, CLI, tests, and reader journeys cannot
quietly disagree.

© 2026 John Briggs — MIT licensed; see ../../LICENSE-CODE.
"""

from accountable_factory import ContractViolation, Factory, PolicyEngine, WorkOrder

__all__ = ["ContractViolation", "Factory", "PolicyEngine", "WorkOrder"]
