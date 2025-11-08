import pytest


def test_can_import_audit_controller():
    """Test that we can import the AuditLogController."""
    try:
        from controllers.AuditLogController import AuditLogController
        assert AuditLogController is not None
    except ImportError as e:
        pytest.fail(f"Could not import AuditLogController: {e}")
