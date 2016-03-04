from zope.interface import Interface
from zope.interface.interfaces import IObjectEvent

class IPublishEvent(IObjectEvent):
    """Publish an object"""

class IPublishable(Interface):
    """A object that can be published"""
    def publish():
        """Dispatch IPublishEvent for object and set as published"""
    def published():
        """True indicates the object has been published"""

class IPublisherQueue(Interface):
    """A queue of objects that can be published"""
    def enqueue(IPublishable):
        """Add object into the queue"""
    def publish():
        """Publish each queued object and empty queue"""
