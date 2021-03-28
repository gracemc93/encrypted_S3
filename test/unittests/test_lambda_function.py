# Grace McNamara
# 28/03/2021

import pytest
from typing import Dict


# ======================================================================================================================
# Test Fixtures
#
# Re-usable code inputs for tests.
# ======================================================================================================================


def event_with_one_bucket() -> Dict[str, any]:
    """
    Returns an event with bucket names specifed.
    """
    return {
        "buckets": ["test_bucket_1"]
    }


def event_with_multiple_buckets() -> Dict[str, any]:
    """
    Returns an event with bucket names specifed.
    """
    return {
        "buckets": ["test_bucket_1", "test_bucket_2"]
    }


def event_with_no_buckets() -> Dict[str, any]:
    """
    Returns an event with no bucket names.
    """
    return {
        "buckets": []
    }


def event_with_no_bucket_field() -> Dict[str, any]:
    """
    Returns an event with no bucket field.
    """
    return {}


# ======================================================================================================================
# Tests
# ======================================================================================================================

def test_buckets_specified():
    pass
