from zope.interface import implements
from zope.interface.interfaces import ObjectEvent
from interfaces import IPublishEvent
from interfaces import IPublisherQueuePublishedEvent

class PublishEvent(ObjectEvent):
    implements(IPublishEvent)

class PublisherQueuePublishedEvent(ObjectEvent):
    implements(IPublisherQueuePublishedEvent)