import pytest


def test_can_import_account_manager():
    """Test that we can import the AccountManager class."""
    try:
        from classes.AccountManager import AccountManager
        assert AccountManager is not None
    except ImportError as e:
        pytest.fail(f"Could not import AccountManager: {e}")


def test_account_manager_instantiation():
    """Test that we can create an AccountManager instance."""
    from classes.AccountManager import AccountManager
    
    try:
        manager = AccountManager()
        assert manager is not None
    except Exception as e:
        pytest.fail(f"Could not instantiate AccountManager: {e}")
