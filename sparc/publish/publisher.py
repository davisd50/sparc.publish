from BTrees.OOBTree import OOBTree
from zope.annotation.interfaces import IAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.component import adapts
from zope.event import notify
from zope.interface import implements

from events import PublishEvent
from interfaces import IPublisher

class PublisherForAnnotableObjects(object):
    """A object that can be published"""
    implements(IPublisher)
    adapts(IAttributeAnnotatable)
    
    def __init__(self, context):
        self.context = context
        self.annotations = IAnnotations(context).\
                                setdefault('IPublisher', OOBTree())
        if 'published' not in self.annotations:
            self.annotations['published'] = False
    
    def publish(self):
        """Dispatch IPublishEvent for object and set as published"""
        notify(PublishEvent(self.context))
        self.annotations['published'] = True
    
    def published(self):
        """True indicates the object has been published"""
        return self.annotations['published']