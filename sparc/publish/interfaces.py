from zope.interface import Interface
from zope.interface.interfaces import IObjectEvent

class IPublishEvent(IObjectEvent):
    """Publish an object"""

class IPublisherQueuePublishedEvent(IObjectEvent):
    """A IPublisherQueue has been published"""

class IPublisher(Interface):
    """A object that can be published"""
    def publish():
        """Dispatch IPublishEvent for object and set as published"""
    def published():
        """True indicates the object has been published"""

class IPublisherQueue(Interface):
    """A queue of objects that can be published"""
    def enqueue(object_):
        """Add object into the queue.  Objects must be adaptable to IPublisher"""
    def publish():
        """Publish each queued object and empty queue.  Dispatches 
        IPublisherQueuePublishedEvent.  Returns sequence of items published"""
