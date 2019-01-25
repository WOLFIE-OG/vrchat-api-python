import re

from vrchat_api.enum import DeveloperType, Status, ReleaseStatus, ModerationType
from vrchat_api.util import strptime

class JsonObject():
    """
    A wrapper class for a JSON dictionaly.
    Each value of the dictionaly is registered as a property of the object.
    Registration of some values might be overriden for the purpose of proper type conversions.
    """

    def __init__(self, j):
        for k, v in j.items():
            if not hasattr(self, k):
                setattr(self, k, v)

        self.attributes = set(j.keys())

class User(JsonObject):
    def __init__(self, j):
        if "developerType" in j.keys():
            setattr(self, "developerType", DeveloperType.fromString(j["developerType"]))

        if "status" in j.keys():
            setattr(self, "status", Status.fromString(j["status"]))

        if "location" in j.keys():
            setattr(self, "location", WorldLocation(j["location"]))

        super().__init__(j)

class Avatar(JsonObject):
    def __init__(self, j):
        setattr(self, "releaseStatus", ReleaseStatus.fromString(j["releaseStatus"]))
        setattr(self, "unityPackages", [UnityPackage(x) for x in j["unityPackages"]])
        super().__init__(j)

class Moderation(JsonObject):
    def __init__(self, j):
        setattr(self, "type", ModerationType.fromString(j["type"]))
        setattr(self, "created", strptime(j["created"]))
        super().__init__(j)

class World(JsonObject):
    def __init__(self, j):
        setattr(self, "releaseStatus", ReleaseStatus.fromString(j["releaseStatus"]))
        setattr(self, "unityPackages", [UnityPackage(x) for x in j["unityPackages"]])
        setattr(self, "instances", [InstanceStat(x) for x in j["instances"]])
        super().__init__(j)

class Instance(JsonObject):
    def __init__(self, j):
        setattr(self, "friends", [User(x) for x in j["friends"]] if j["friends"] != False else [])
        setattr(self, "users", [User(x) for x in j["users"]] if j["users"] != False else [])
        super().__init__(j)

class UnityPackage(JsonObject):
    def __init__(self, j):
        setattr(self, "created_at", strptime(j["created_at"]))
        super().__init__(j)

class WorldLocation():
    def __init__(self, location):
        self.offline = (location == "offline")
        self.private = (location == "private")
        self.worldId = None
        self.instanceId = None
        if not self.offline and not self.private:
            self.worldId, self.instanceId = re.compile("([\w-]+):(.+)").match(location).groups()

class InstanceStat():
    def __init__(self, j):
        setattr(self, "id", j[0])
        setattr(self, "users", j[1])
