from django.test import TestCase
from channels.testing import HttpCommunicator
from DhametCode.game_consumers import GameConsumer

#A test case for the async 
class MyTests(TestCase):
    async def test_my_consumer(self):
        communicator = HttpCommunicator(GameConsumer, "GET", "/test/")
        response = await communicator.get_response()
        self.assertEqual(response["body"], b"test response")
        self.assertEqual(response["status"], 200)
# Create your tests here.
