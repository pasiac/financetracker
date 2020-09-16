from urllib.parse import urlparse


class TestUtilityMixin:
    STATUS_OK = 200
    STATUS_BAD_REQUEST = 200
    STATUS_FORBIDDEN = 302
    STATUS_REDIRECT = 302
    STATUS_NOT_FOUND = 404
    STATUS_UNAUTHORIZED = 401

    def was_redirected_to(self, expected_location, response):
        parsed_location = urlparse(response["location"])
        return expected_location == parsed_location.path

    def client_send_request_with_params(self, url, *args):
        self.client.login()
        return self.client.get(url, *args)

    def client_send_post_request(self, url, data):
        self.client.login()
        return self.client.post(url, data)
