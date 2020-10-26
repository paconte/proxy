import requests
import unittest
import proxy.settings as settings


URL = settings.PROXY_URL + ":" + str(settings.PROXY_PORT)
ENDPOINT = settings.PROXY_ENDPOINT
STATUS_URL = URL + settings.PROXY_STATUS_PATH
TEST_DEBUG = settings.TEST_DEBUG


def debug_response(r, status=True, content=True, headers=True):
    print('###### start ######')
    print(r.url)
    if status:
        print(str(r.status_code))
    if content:
        print(str(r.content))
    if headers:
        print(str(r.headers))
    print('###### end ######')


class TestProxy(unittest.TestCase):

    def test_endpoint_reqresin_post(self):
        url1a = ENDPOINT + "/api/users"
        url1b = URL + "/api/users"
        url2a = ENDPOINT + "/api/register"
        url2b = URL + "/api/register"
        payload1 = {
            "name": "paul rudd",
            "movies": ["I Love You Man", "Role Models"]}
        payload2 = {
            "email": "paul rudd",
            "password": ["I Love You Man", "Role Models"]}
        payload3 = {"email": "eve.holt@reqres.in", "password": "pistol"}

        results_a = []
        requests_a = [
            (url1a, payload1, 201),
            (url2a, payload2, 400),
            (url2a, payload3, 200)
        ]
        results_b = []
        requests_b = [
            (url1b, payload1, 201),
            (url2b, payload2, 400),
            (url2b, payload3, 200)
        ]

        for (url, payload, result) in requests_a:
            headers = {
                'Content-Type': 'application/json',
                'Content-Length': str(len(payload))}
            r = requests.post(url=url, json=payload, headers=headers)
            self.assertEqual(r.status_code, result)
            results_a.append((r.status_code, r.content))

        for (url, payload, result) in requests_b:
            headers = {
                'Content-Type': 'application/json',
                'Content-Length': str(len(payload))}
            r = requests.post(url=url, json=payload)
            self.assertEqual(r.status_code, result)
            results_b.append((r.status_code, r.content))

        for i in range(len(results_a)):
            print(results_a[i][0], results_b[i][0])
            print(results_a[i][1], results_b[i][1])
            self.assertEquals(results_a[i][0], results_b[i][0])
            if i != 0:  # content with CreatedAt
                self.assertEquals(results_a[i][1], results_b[i][1])
            # else:
            #    self.assertEquals(
            #    results_a[i][1]["id"], results_b[i][1]["id"])

    def test_endpoint_reqresin_get(self):
        url3a = ENDPOINT + "/api/users?page=2"
        url3b = URL + "/api/users?page=2"
        url4a = ENDPOINT + "/api/users/2"
        url4b = URL + "/api/users/2"
        test_requests = [
            (url3a, 200),
            (url3b, 404),
            (url4a, 200),
            (url4b, 404)
        ]
        for (url, result) in test_requests:
            r = requests.get(url=url)
            if TEST_DEBUG:
                debug_response(r, headers=False)
            self.assertEqual(r.status_code, result)

    def test_proxy_get_status(self):
        r = requests.get(STATUS_URL)
        self.assertEqual(r.status_code, 200)
        self.assertIn("Requests:", r.content.decode('utf-8'))
        self.assertIn("Running since:", r.content.decode('utf-8'))
        if TEST_DEBUG:
            debug_response(r, headers=False)


if __name__ == "__main__":
    unittest.main()
