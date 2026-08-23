"""Vendor-neutral teaching implementation of the accountable factory.

© 2026 John Briggs — MIT licensed; see ../LICENSE-CODE.
"""

from .contracts import ArtifactError, sha256_digest, validate_artifact
from .factory import ContractViolation, Factory, WorkOrder
from .policy import PolicyEngine

__all__ = [
    "ArtifactError",
    "ContractViolation",
    "Factory",
    "PolicyEngine",
    "WorkOrder",
    "sha256_digest",
    "validate_artifact",
]
