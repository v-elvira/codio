from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class AnonSustainedThrottle(AnonRateThrottle):
    scope = "anon_sustained"


class AnonBurstThrottle(AnonRateThrottle):
    scope = "anon_burst"


class UserSustainedThrottle(UserRateThrottle):
    scope = "user_sustained"


class UserBurstThrottle(UserRateThrottle):
    scope = "user_burst"



# Overwritting throttling rules example (redefine allow_request() => True/False):

# import random

# class RandomRateThrottle(throttling.BaseThrottle):
#     def allow_request(self, request, view):
#         return random.randint(1, 10) != 1