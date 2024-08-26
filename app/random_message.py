import random

class RandomMessage:
    def __init__(self, messages):
        self.messages = messages
        self.copy_messages = messages[:]  # create a copy of the list

    def random_message(self):
        if not self.copy_messages:
            self.copy_messages = self.messages[:]  # create a new copy of the list
        idx = random.randint(0, len(self.copy_messages) - 1)  # generate a random index
        message = self.copy_messages.pop(idx)  # remove and return the message at the random index
        return message