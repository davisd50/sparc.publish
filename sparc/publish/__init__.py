from interfaces import IPublisher
from interfaces import IPublisherQueue
from interfaces import IPublisherQueuePublishedEvent
from interfaces import IPublishEvent

class PublishingError(Exception):
    """A standard error in publishing"""

class RecoverablePublishingError(PublishingError):
    """A publishing error that can be recovered from later"""