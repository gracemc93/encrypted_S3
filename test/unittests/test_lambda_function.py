# Grace McNamara
# 28/03/2021

import pytest
from unittest.mock import patch
from typing import Dict, List

from botocore.exceptions import ClientError
# SUT : System Under Test
import encryption_checker_lambda.lambda_function as sut


# ======================================================================================================================
# Test Fixtures
#
# Re-usable code inputs for tests.
# ======================================================================================================================


@pytest.fixture
def patch_path() -> str:
    """Returns the module path for mock patching."""
    return "encryption_checker_lambda.lambda_function"


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
        "Buckets": one_bucket
    }


@pytest.fixture
def event_with_multiple_buckets(multiple_buckets: List[str]) -> Dict[str, any]:
    """
    Returns an event with bucket names specifed.
    """
    return {
        "Buckets": multiple_buckets
    }


@pytest.fixture
def event_with_no_buckets() -> Dict[str, any]:
    """
    Returns an event with no bucket names.
    """
    return {
        "Buckets": []
    }


@pytest.fixture
def event_with_no_bucket_field() -> Dict[str, any]:
    """
    Returns an event with no bucket field.
    """
    return {}


@pytest.fixture
def aws_bucket_dict(multiple_buckets) -> callable:
    """
    Returns a AWS bucket schema.
    """

    def generator(names: List[str] = None) -> Dict[str, List[Dict[str, str]]]:
        """
        Creates a Buckets dictionary with multiple bucket items.

        Amount of bucket names depends on the names List passed in.

        :param names: The names to give the buckets in the returned dict.
        :return: A AWS Buckets dictionary, containing as many buckets as items in the 'names' argument.
        """
        if names is None:
            names = multiple_buckets

        return {
            "Buckets": [{"Name": name} for name in names]
        }

    return generator


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
        "Buckets": {
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
                                                          patch_path, monkeypatch):
    """
    GIVEN: A list with multiple buckets.
    WHEN:  Retrieving the encryption status for the buckets.
    THEN:  Verify the return format is as expected.
    """
    # The expected result of the function under test.
    expected = {
        "Buckets": {
            "test_bucket_1": encryption_status_1,
            "test_bucket_2": encryption_status_2
        }
    }

    # Mock internal function calls with expected return values.
    return_values = [encryption_status_1, encryption_status_2]
    with patch(f"{patch_path}.retrieve_encryption_status", side_effect=return_values):
        actual = sut.get_specified_bucket_status(multiple_buckets)

        assert actual == expected


@pytest.mark.parametrize("encryption_status_1",
                         [
                             ("Encrypted"),
                         ])
def test_get_specified_bucket_status_with_one_bucket(encryption_status_1, one_bucket,
                                                     patch_path, monkeypatch):
    """
    GIVEN: A list with one buckets
    WHEN:  Retrieving the encryption status for one bucket.
    THEN:  Verify the return format is as expected.
    """

    expected = {
        "Buckets": {
            "test_bucket_1": encryption_status_1
        }
    }

    return_values = [encryption_status_1]
    with patch(f"{patch_path}.retrieve_encryption_status",
               side_effect=return_values):
        actual = sut.get_specified_bucket_status(one_bucket)

        assert actual == expected


def test_get_specified_bucket_status_does_not_exist(one_bucket, monkeypatch):
    """
    GIVEN: A bucket that does not exist on the AWS service account.
    WHEN:  Checking for the encryption status of specific buckets.
    THEN:  Verify the current 'does not exist' string is returned.
    """
    expected = {
        'Buckets': {
            'test_bucket_1': "Bucket doesn't exist"
        }
    }

    monkeypatch.setattr(sut, "retrieve_encryption_status", lambda _: None)

    assert sut.get_specified_bucket_status(one_bucket) == expected


# ----------------------------------------------------------------------------------------------------------------------
# get_all_buckets_status tests
# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.parametrize("encryption_status_1, encryption_status_2",
                         [
                             ("Not Encrypted", "Not Encrypted"),
                             ("Not Encrypted", "Encrypted"),
                             ("Encrypted", "Not Encrypted"),
                             ("Encrypted", "Encrypted")
                         ])
def test_get_specified_bucket_status(encryption_status_1, encryption_status_2, multiple_buckets,
                                     patch_path, monkeypatch):
    """
    GIVEN: A list with multiple buckets.
    WHEN:  Retrieving the encryption status for the buckets.
    THEN:  Verify the return format is as expected.
    """
    # The expected result of the function under test.
    expected = {
        "Buckets": {
            "test_bucket_1": encryption_status_1,
            "test_bucket_2": encryption_status_2
        }
    }

    # Mock internal function calls with expected return values.
    return_values = [encryption_status_1, encryption_status_2]
    with patch(f"{patch_path}.retrieve_encryption_status", side_effect=return_values):
        actual = sut.get_specified_bucket_status(multiple_buckets)

        assert actual == expected


# ----------------------------------------------------------------------------------------------------------------------
# get_all_buckets tests
# ----------------------------------------------------------------------------------------------------------------------

def test_get_all_buckets(aws_bucket_dict, monkeypatch):
    """
    GIVEN: Nothing.
    WHEN:  Querying for all S3 buckets on the AWS account.
    THEN:  Verify the function returns the expected result.
    """
    expected = aws_bucket_dict()

    # Mock boto client.list_buckets call.
    monkeypatch.setattr(sut.client, "list_buckets", lambda: expected)

    actual = sut.get_all_buckets()

    assert actual == expected


def test_get_all_buckets_status(aws_bucket_dict, patch_path, multiple_buckets, monkeypatch):
    """
    GIVEN: A dictionary following the AWS bucket schema.
    WHEN:  Checking the encryption status of the buckets.
    THEN:  Verify the correct dictionary output is returned showing the bucket names and its encryption status.
    """
    expected = {
        'Buckets': {
            'test_bucket_1': 'Encrypted',
            'test_bucket_2': 'Not Encrypted'
        }
    }

    mock_encryption_statuses = ["Encrypted", "Not Encrypted"]
    with patch(f"{patch_path}.retrieve_encryption_status", side_effect=mock_encryption_statuses) as mock:
        assert sut.get_all_buckets_status(aws_bucket_dict()) == expected


def test_retrieve_encryption_status(monkeypatch):
    """
    GIVEN: A bucket name.
    WHEN:  Checking the encryption status of the given bucket.
    THEN:  Check if the correct 'Encrypted' response is returned.
    """
    monkeypatch.setattr(sut.client, "get_bucket_encryption", lambda Bucket: None)

    actual = sut.retrieve_encryption_status(bucket_name="TEST")

    assert actual == "Encrypted"


def test_retrieve_encryption_status_fail(monkeypatch):
    """
    GIVEN: A bucket name.
    WHEN:  Checking the encryption status of the given bucket.
    THEN:  Check if the correct 'Not Encrypted' response is returned.
    """

    def raise_ClientError() -> None:
        """Creates a Synthetic client error to test exception handling code."""
        # Create a ClientError
        err = ClientError({}, {})
        err.response["Error"] = {}
        err.response["Error"]["Code"] = 'ServerSideEncryptionConfigurationNotFoundError'

        raise err

    # Mock Boto.client.get_bucket_encryption method.
    monkeypatch.setattr(sut.client, "get_bucket_encryption", lambda Bucket: raise_ClientError())

    actual = sut.retrieve_encryption_status(bucket_name="TEST")

    assert actual == "Not Encrypted"


# ----------------------------------------------------------------------------------------------------------------------
# lambda_handler tests
# ----------------------------------------------------------------------------------------------------------------------


def test_lambda_handler(patch_path):
    """
    GIVEN: An event with specified bucket names.
    WHEN:  Executing the lambda.
    THEN:  Check if the lambda executed as expected.
    """
    return_value = "test_body"

    expected_value = {
        'statusCode': 200,
        'body': return_value
    }

    mock_event = {
        "Buckets": "mock_bucket"
    }

    # Mock all internal function calls and test they were called with the correct parameters.
    with patch(f"{patch_path}.buckets_specified_in", return_value=True) as mock_buckets_specified_in:
        with patch(f"{patch_path}.get_specified_bucket_status", return_value=return_value) as mock_get_specified_bucket_status:
            assert sut.lambda_handler(mock_event, None) == expected_value

        mock_get_specified_bucket_status.assert_called_with(buckets=mock_event["Buckets"])

    mock_buckets_specified_in.assert_called_with(mock_event)


def test_lambda_handler_all_buckets(patch_path, multiple_buckets):
    """
    GIVEN: An event with no specified event names.
    WHEN:  Executing the lambda.
    THEN:  Check if the lambda executed as expected.
    """
    return_value = "test_body"

    expected_value = {
        'statusCode': 200,
        'body': return_value
    }

    mock_event = {
        "Buckets": "mock_bucket"
    }

    # Mock all internal function calls and test they were called with the correct parameters.
    with patch(f"{patch_path}.buckets_specified_in", return_value=False) as mock_buckets_specified_in:
        with patch(f"{patch_path}.get_all_buckets", return_value=multiple_buckets) as mock_get_all_buckets:
            with patch(f"{patch_path}.get_all_buckets_status", return_value=return_value) as mock_get_all_buckets_status:
                assert sut.lambda_handler(mock_event, None) == expected_value

            mock_get_all_buckets_status.assert_called_with(buckets=multiple_buckets)

        mock_get_all_buckets.assert_called_with()

    mock_buckets_specified_in.assert_called_with(mock_event)
