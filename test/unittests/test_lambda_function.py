# Grace McNamara
# 28/03/2021

import pytest
from unittest.mock import patch
from typing import Dict, List

# SUT : System Under Test
import encryption_checker_lambda.lambda_function as sut


# ======================================================================================================================
# Test Fixtures
#
# Re-usable code inputs for tests.
# ======================================================================================================================

@pytest.fixture
def one_bucket() -> List[str]:
    """
    Returns a list with a single bucket name.
    """
    return ["test_bucket_1"]


@pytest.fixture
def multiple_buckets() -> List[str]:
    """
    Returns a list with multiple bucket names.
    """
    return ["test_bucket_1", "test_bucket_2"]


@pytest.fixture
def event_with_one_bucket(one_bucket: List[str]) -> Dict[str, any]:
    """
    Returns an event with bucket names specifed.
    """
    return {
        "buckets": one_bucket
    }


@pytest.fixture
def event_with_multiple_buckets(multiple_buckets: List[str]) -> Dict[str, any]:
    """
    Returns an event with bucket names specifed.
    """
    return {
        "buckets": multiple_buckets
    }


@pytest.fixture
def event_with_no_buckets() -> Dict[str, any]:
    """
    Returns an event with no bucket names.
    """
    return {
        "buckets": []
    }


@pytest.fixture
def event_with_no_bucket_field() -> Dict[str, any]:
    """
    Returns an event with no bucket field.
    """
    return {}


# ======================================================================================================================
# Tests
# ======================================================================================================================

# ----------------------------------------------------------------------------------------------------------------------
# buckets_specified_in tests
# ----------------------------------------------------------------------------------------------------------------------

def test_buckets_specified_in_with_no_buckets(event_with_no_buckets):
    """
    GIVEN: An event with no buckets.
    WHEN:  Checking for bucket names.
    THEN:  Verify the function returns false.
    """
    assert sut.buckets_specified_in(event_with_no_buckets) == False


def test_bucket_specified_in_with_one_bucket(event_with_one_bucket):
    """
    GIVEN: A one bucket event.
    WHEN:  Checking for bucket names.
    THEN:  Verify the function return True
    """
    assert sut.buckets_specified_in(event_with_one_bucket) == True


def test_bucket_specified_in_with_multiple_buckets(event_with_multiple_buckets):
    """
    GIVEN: A event with multiple buckets.
    WHEN:  Checking for bucket names.
    THEN:  Verify the function returns True
    """
    assert sut.buckets_specified_in(event_with_multiple_buckets) == True


def test_bucket_specified_in_with_no_bucket_field(event_with_no_bucket_field):
    """
    GIVEN: A event with no bucket field.
    WHEN:  Checking for bucket names.
    THEN:  Verify the function returns False.
    """
    assert sut.buckets_specified_in(event_with_no_bucket_field) == False


# ----------------------------------------------------------------------------------------------------------------------
# get_specified_bucket_status tests
# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.parametrize("encryption_status",
                         [
                             "Not Encrypted",
                             "Encrypted"
                         ])
def test_get_specified_bucket_status_with_multiple_bucket(encryption_status, one_bucket, monkeypatch):
    """
    GIVEN: A list with a single bucket.
    WHEN:  Retrieving the encrption status for the bucket.
    THEN:  Verify the return format is as expected.
    """
    # The expected result of the function under test.
    expected = {
        "buckets": {
            "test_bucket_1": encryption_status
        }
    }

    # Mock internal function calls.
    monkeypatch.setattr(sut, "retrieve_encryption_status", lambda _: encryption_status)

    assert sut.get_specified_bucket_status(one_bucket) == expected


@pytest.mark.parametrize("encryption_status_1, encryption_status_2",
                         [
                             ("Not Encrypted", "Not Encrypted"),
                             ("Not Encrypted", "Encrypted"),
                             ("Encrypted", "Not Encrypted"),
                             ("Encrypted", "Encrypted")
                         ])
def test_get_specified_bucket_status_with_multiple_bucket(encryption_status_1, encryption_status_2, multiple_buckets,
                                                          monkeypatch):
    """
    GIVEN: A list with multiple buckets.
    WHEN:  Retrieving the encrption status for the buckets.
    THEN:  Verify the return format is as expected.
    """
    # The expected result of the function under test.
    expected = {
        "buckets": {
            "test_bucket_1": encryption_status_1,
            "test_bucket_2": encryption_status_2
        }
    }

    # Mock internal function calls with expected return values.
    return_values = [encryption_status_1, encryption_status_2]
    with patch("encryption_checker_lambda.lambda_function.retrieve_encryption_status", side_effect=return_values):
        actual = sut.get_specified_bucket_status(multiple_buckets)

        assert actual == expected
