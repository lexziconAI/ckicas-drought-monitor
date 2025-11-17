"""Test suite for results.py
Generated: 2025-11-09T14:41:14.251676
Source: C:\Users\regan\ID SYSTEM\axiom-x\.venv\Lib\site-packages\pyparsing\results.py
Worker ID: test-01
"""

import pytest
from pathlib import Path

# Add imports for the module being tested
# import sys
# sys.path.append(str(Path(__file__).parent.parent))

```python
# test_results.py
"""
Comprehensive pytest test suite for pyparsing.results module.

This test suite covers:
- ParseResults class functionality
- _ParseResultsWithOffset class
- List/dict-like behavior
- Attribute access patterns
- Edge cases and error handling
- Performance characteristics
"""

import pytest
import sys
import copy
import pickle
from typing import Any
from collections.abc import MutableMapping, Mapping, MutableSequence

# Import the module under test
try:
    from pyparsing.results import (
        ParseResults,
        _ParseResultsWithOffset,
    )
    from pyparsing import Word, nums, alphas, Literal
except ImportError:
    pytest.skip("pyparsing not available", allow_module_level=True)


# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture
def empty_parse_results():
    """Create an empty ParseResults object."""
    return ParseResults([])


@pytest.fixture
def simple_parse_results():
    """Create a simple ParseResults with list items."""
    return ParseResults(["value1", "value2", "value3"])


@pytest.fixture
def named_parse_results():
    """Create ParseResults with named items."""
    pr = ParseResults(["value1", "value2"])
    pr["name1"] = "value1"
    pr["name2"] = "value2"
    return pr


@pytest.fixture
def nested_parse_results():
    """Create nested ParseResults."""
    inner = ParseResults(["inner1", "inner2"])
    inner["inner_name"] = "inner_value"
    outer = ParseResults(["outer1", inner, "outer2"])
    outer["nested"] = inner
    return outer


@pytest.fixture
def complex_parse_results():
    """Create complex ParseResults with mixed content."""
    pr = ParseResults(["a", "b", "c"])
    pr["key1"] = "value1"
    pr["key2"] = ParseResults(["nested1", "nested2"])
    pr["key3"] = [1, 2, 3]
    return pr


# =============================================================================
# _ParseResultsWithOffset TESTS
# =============================================================================


class TestParseResultsWithOffset:
    """Tests for _ParseResultsWithOffset helper class."""

    def test_initialization(self, simple_parse_results):
        """Test creating _ParseResultsWithOffset."""
        offset = _ParseResultsWithOffset(simple_parse_results, 5)
        assert offset.tup[0] == simple_parse_results
        assert offset.tup[1] == 5

    def test_getitem_access(self, simple_parse_results):
        """Test index access to tuple."""
        offset = _ParseResultsWithOffset(simple_parse_results, 10)
        assert offset[0] == simple_parse_results
        assert offset[1] == 10

    def test_getstate(self, simple_parse_results):
        """Test pickle state serialization."""
        offset = _ParseResultsWithOffset(simple_parse_results, 15)
        state = offset.__getstate__()
        assert state == (simple_parse_results, 15)

    def test_setstate(self, simple_parse_results):
        """Test pickle state deserialization."""
        offset = _ParseResultsWithOffset(ParseResults([]), 0)
        offset.__setstate__((simple_parse_results, 20))
        assert offset.tup[0] == simple_parse_results
        assert offset.tup[1] == 20

    def test_pickle_roundtrip(self, simple_parse_results):
        """Test pickling and unpickling."""
        offset = _ParseResultsWithOffset(simple_parse_results, 25)
        pickled = pickle.dumps(offset)
        unpickled = pickle.loads(pickled)
        assert unpickled[0] == simple_parse_results
        assert unpickled[1] == 25


# =============================================================================
# ParseResults INITIALIZATION TESTS
# =============================================================================


class TestParseResultsInitialization:
    """Tests for ParseResults object creation."""

    def test_empty_initialization(self):
        """Test creating empty ParseResults."""
        pr = ParseResults([])
        assert len(pr) == 0
        assert list(pr) == []

    def test_list_initialization(self):
        """Test initialization with list."""
        pr = ParseResults(["a", "b", "c"])
        assert len(pr) == 3
        assert list(pr) == ["a", "b", "c"]

    def test_tuple_initialization(self):
        """Test initialization with tuple."""
        pr = ParseResults(("x", "y", "z"))
        assert len(pr) == 3
        assert list(pr) == ["x", "y", "z"]

    def test_parseresults_initialization(self):
        """Test initialization from another ParseResults."""
        pr1 = ParseResults(["a", "b"])
        pr2 = ParseResults(pr1)
        assert list(pr2) == ["a", "b"]

    def test_initialization_with_name(self):
        """Test initialization with name parameter."""
        pr = ParseResults(["value"], name="test_name")
        assert pr.get_name() == "test_name"

    def test_initialization_preserves_types(self):
        """Test that initialization preserves various types."""
        data = [1, 2.5, "string", None, True]
        pr = ParseResults(data)
        assert list(pr) == data

    def test_initialization_with_nested_parseresults(self):
        """Test initialization with nested ParseResults."""
        inner = ParseResults(["inner"])
        pr = ParseResults([inner, "outer"])
        assert len(pr) == 2
        assert isinstance(pr[0], ParseResults)


# =============================================================================
# ParseResults LIST-LIKE BEHAVIOR TESTS
# =============================================================================


class TestParseResultsListBehavior:
    """Tests for list-like operations on ParseResults."""

    def test_len(self, simple_parse_results):
        """Test len() function."""
        assert len(simple_parse_results) == 3

    def test_getitem_positive_index(self, simple_parse_results):
        """Test positive index access."""
        assert simple_parse_results[0] == "value1"
        assert simple_parse_results[1] == "value2"
        assert simple_parse_results[2] == "value3"

    def test_getitem_negative_index(self, simple_parse_results):
        """Test negative index access."""
        assert simple_parse_results[-1] == "value3"
        assert simple_parse_results[-2] == "value2"
        assert simple_parse_results[-3] == "value1"

    def test_getitem_slice(self, simple_parse_results):
        """Test slice access."""
        result = simple_parse_results[0:2]
        assert isinstance(result, ParseResults)
        assert list(result) == ["value1", "value2"]

    def test_getitem_out_of_range(self, simple_parse_results):
        """Test index out of range raises IndexError."""
        with pytest.raises(IndexError):
            _ = simple_parse_results[10]

    def test_setitem_by_index(self, simple_parse_results):
        """Test setting item by index."""
        simple_parse_results[1] = "new_value"
        assert simple_parse_results[1] == "new_value"

    def test_delitem_by_index(self, simple_parse_results):
        """Test deleting item by index."""
        del simple_parse_results[1]
        assert len(simple_parse_results) == 2
        assert list(simple_parse_results) == ["value1", "value3"]

    def test_append(self, simple_parse_results):
        """Test append operation."""
        simple_parse_results.append("value4")
        assert len(simple_parse_results) == 4
        assert simple_parse_results[-1] == "value4"

    def test_extend(self, simple_parse_results):
        """Test extend operation."""
        simple_parse_results.extend(["value4", "value5"])
        assert len(simple_parse_results) == 5
        assert list(simple_parse_results)[-2:] == ["value4", "value5"]

    def test_insert(self, simple_parse_results):
        """Test insert operation."""
        simple_parse_results.insert(1, "inserted")
        assert simple_parse_results[1] == "inserted"
        assert len(simple_parse_results) == 4

    def test_pop_no_args(self, simple_parse_results):
        """Test pop without arguments."""
        value = simple_parse_results.pop()
        assert value == "value3"
        assert len(simple_parse_results) == 2

    def test_pop_with_index(self, simple_parse_results):
        """Test pop with index."""
        value = simple_parse_results.pop(1)
        assert value == "value2"
        assert len(simple_parse_results) == 2

    def test_iteration(self, simple_parse_results):
        """Test iteration over ParseResults."""
        items = [item for item in simple_parse_results]
        assert items == ["value1", "value2", "value3"]

    def test_reversed(self, simple_parse_results):
        """Test reversed iteration."""
        items = list(reversed(simple_parse_results))
        assert items == ["value3", "value2", "value1"]

    def test_contains(self, simple_parse_results):
        """Test 'in' operator."""
        assert "value1" in simple_parse_results
        assert "not_present" not in simple_parse_results

    def test_count(self, simple_parse_results):
        """Test count method."""
        simple_parse_results.append("value1")
        assert simple_parse_results.count("value1") == 2
        assert simple_parse_results.count("value2") == 1
        assert simple_parse_results.count("nonexistent") == 0