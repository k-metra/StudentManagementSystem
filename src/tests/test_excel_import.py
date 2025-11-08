import tempfile
import os
from unittest.mock import Mock, patch

import pytest


def test_can_import_excel_utility():
    """Test that we can import the excel import utility."""
    try:
        from utils.excel_import import import_students_from_excel
        assert callable(import_students_from_excel)
    except ImportError as e:
        pytest.fail(f"Could not import excel utility: {e}")


@patch('utils.misc.enter_to_continue')
def test_excel_module_import(mock_input):
    """Test that the excel import module can be imported."""
    mock_input.return_value = None
    try:
        import utils.excel_import
        assert True
    except ImportError:
        pytest.fail("Could not import utils.excel_import module")


@patch('utils.misc.enter_to_continue')
def test_excel_function_exists(mock_input):
    """Test that the import function exists."""
    mock_input.return_value = None
    import utils.excel_import
    assert hasattr(utils.excel_import, 'import_students_from_excel')
