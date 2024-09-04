import random

class RandomProfile:
    def __init__(self, profiles):
        self.profiles = profiles
        self.copy_profiles = profiles[:]  # create a copy of the list

    def random_profile(self):
        if not self.copy_profiles:
            self.copy_profiles = self.profiles[:]  # create a new copy of the list
        idx = random.randint(0, len(self.copy_profiles) - 1)  # generate a random index
        profile = self.copy_profiles.pop(idx)  # remove and return the profile at the random index
        return profile
    
    