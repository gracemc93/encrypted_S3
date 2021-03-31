import pytest
from python_terraform import *
import requests


@pytest.fixture(scope="session")
def aws_resource_factory():
    def factory():
        return {
            'url_for_api': "",
            'encrypted_bucket': "",
            'non_encrypted_bucket': ""
        }

    return factory

@pytest.fixture(autouse=True, scope='session')
def setup_teardown_aws_resources(aws_resource_factory):
    """
    Deploys all the AWS resources required.
    Runs the tests.
    Destroys all AWS resources
    """
    tf = Terraform(working_dir='../terraform', var_file='test.tfvars')
    print("Creating resources in AWS, this may take a few minutes...")
    tf.apply(skip_plan=True, no_color=IsFlagged, input=False, capture_output=False)

    output = tf.cmd('show', '-json')
    aws_resource = aws_resource_factory()
    aws_resource["url_for_api"] = json.loads(output[1])['values']['outputs']['url_to_encryption_checker']['value']
    aws_resource["encrypted_bucket"] = json.loads(output[1])['values']['outputs']['encrypted_bucket']['value']
    aws_resource["non_encrypted_bucket"] = json.loads(output[1])['values']['outputs']['non_encrypted_bucket']['value']

    yield aws_resource
    print("Destroying AWS resources...")
    tf.destroy(input=False, capture_output=False)


def test_api_response_for_no_buckets_request(setup_teardown_aws_resources):
    """
    Tests if a request is sent with no buckets specified,
    all buckets are returned in the response
    and whether they are encrypted/not encrypted
    """
    aws_resource = setup_teardown_aws_resources
    payload = {}
    response = json.loads(requests.post(aws_resource["url_for_api"], payload).text)
    print("RESP", response)
    assert len(response['body']['Buckets']) > 0


def test_api_response_for_one_bucket_request(setup_teardown_aws_resources):
    """
    Tests if a request is sent with one bucket specified,
    this bucket is returned in the response
    and whether it is encrypted/not encrypted
    """
    aws_resource = setup_teardown_aws_resources
    payload = json.dumps({"Buckets": [aws_resource["encrypted_bucket"]]})
    expected = {
        "Buckets": {aws_resource["encrypted_bucket"]: "Encrypted"}
    }
    res = requests.post(url=aws_resource["url_for_api"], data=payload)
    actual = json.loads(res.text)

    assert actual['body'] == expected


def test_api_response_for_multiple_bucket_request(setup_teardown_aws_resources):
    """
    Tests if a request is sent with multiple buckets specified,
    all buckets in the account are returned in the response
    and whether they are encrypted/not encrypted
    """
    aws_resource = setup_teardown_aws_resources
    payload = json.dumps({"Buckets": [aws_resource["encrypted_bucket"],
                                      aws_resource["non_encrypted_bucket"]]})
    expected = {
        "Buckets": {aws_resource["encrypted_bucket"]: "Encrypted",
                    aws_resource["non_encrypted_bucket"]: "Not Encrypted"}
    }
    res = requests.post(url=aws_resource["url_for_api"], data=payload)
    actual = json.loads(res.text)

    assert actual['body'] == expected

def test_api_response_for_empty_buckets_list(setup_teardown_aws_resources):
    """
    Tests if a request is sent with an empty "Buckets" list,
    all buckets in the account are returned in the response
    and whether they are encrypted/not encrypted
    """
    aws_resource = setup_teardown_aws_resources
    payload = json.dumps({"Buckets": []})
    response = json.loads(requests.post(aws_resource["url_for_api"], payload).text)

    assert len(response['body']['Buckets']) > 0
