import unittest
from datetime import datetime
from time import sleep


# Credits : https://www.youtube.com/watch?v=mhUQe4BKZXs&t=956s

class Record:
    def __init__(self, last_request_time: datetime, tokens: int):
        """
        :param last_request_time: Datetime of last request by a user
        :param tokens: Available requests for this user
        """
        self.last_request_time = last_request_time
        self.tokens = tokens


class TokenBucketAPI:
    def __init__(self, rps):
        """
        :param rps: # The maximum allowable requests per second for a customer
        """
        self.rps = rps
        self.customer_record = dict()  # Keep a cache of {"customer_id": Record(datetime, tokens)}

    def request(self, customer_id: str) -> bool:
        """
        Determines if a request should be served
        :param customer_id: a string to uniquely identify each customer
        :return: a boolean to indicate if a request should be served
        """
        request_time = datetime.now()  # record the request time the moment it hits our servers
        record = self.customer_record.get(customer_id) or Record(request_time, self.rps)  # fetch record, or create new

        print(f"Customer       : {customer_id}")
        print(f"Request Time   : {request_time.strftime('%H:%M:%S')}")
        print(f"Current Record : {record.last_request_time.strftime('%H:%M:%S')}, {record.tokens}")

        return self.process_record(customer_id, request_time, record)

    def process_record(self, customer_id: str, request_time: datetime, record: Record) -> bool:
        """
        :param customer_id: a string to uniquely identify each customer
        :param request_time: time at which the request arrived
        :param record: the record object belonging to the customer
        :return: a boolean to indicate if a request should be served
        """
        time_diff = self.get_time_diff_in_seconds(request_time, record.last_request_time)
        print(f"Time Diff      : {time_diff}s")

        if time_diff == 0:  # request came in the same second as the last request
            if record.tokens == 0:  # this customer has no more available requests in this second
                print(f"REQUEST FORBIDDEN ❌\n")
                return False
            record.tokens -= 1  # remember, we can only accommodate up to self.rps requests in each second

        else:
            record.last_request_time = request_time  # update the last request time
            record.tokens = self.rps - 1  # refresh the number of tokens we can have, minus 1 for the current token used

        print(f"New Record     : {record.last_request_time.strftime('%H:%M:%S')}, {record.tokens}")
        print(f"REQUEST ALLOWED ✔\n")
        self.customer_record[customer_id] = record
        return True

    def get_time_diff_in_seconds(self, t1: datetime, t2: datetime) -> int:
        """
        Returns the absolute time difference between 2 time stamps, rounded down to the nearest second
        :param t1: first timing
        :param t2: second timing
        :return: absolute time difference, in seconds
        """
        return abs(int((t1 - t2).total_seconds()))


class Test(unittest.TestCase):
    def test_api(self):
        REQUESTS_PER_SECOND = 5 // 2
        api = TokenBucketAPI(REQUESTS_PER_SECOND)
        self.assertEqual(True, api.request("Google"))
        self.assertEqual(True, api.request("Google"))
        self.assertEqual(False, api.request("Google"))
        print(f"------------SLEEP(2)---------------------\n")
        sleep(2)
        self.assertEqual(True, api.request("Google"))
        self.assertEqual(True, api.request("Google"))
        self.assertEqual(False, api.request("Google"))


if __name__ == "__main__":
    unittest.main()
