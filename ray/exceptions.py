class RayError(Exception):
    pass


class InvalidBodyError(RayError):
    pass


class IntegrationError(RayError):
    pass


class CollisionError(RayError):
    pass


class ScenarioError(RayError):
    pass
