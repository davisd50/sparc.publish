from zope.component import adapts
from zope.component import queryAdapter
from zope.event import notify
from zope.interface import implements
from zc.queue.interfaces import IQueue
from sparc.publish import IPublisher
from sparc.publish import IPublisherQueue
from sparc.publish.events import PublisherQueuePublishedEvent

class PublisherQueueForZCQueue(object):
    """A queue of objects that can be published"""
    implements(IPublisherQueue)
    adapts(IQueue)
    
    def __init__(self, context):
        self.context = context # concurrency-safe persistent queue implementation
    
    # IPublisherQueue
    def enqueue(self, item):
        """Add object into the queue"""
        if not queryAdapter(item, IPublisher):
            raise TypeError('could not adapt.  expected item to be adaptable to IPublisher')
        self.context.put(item)

    def publish(self):
        """Publish each queued object and empty queue"""
        while self.context:
            item = self.context.pull()
            IPublisher(item).publish()
        notify(PublisherQueuePublishedEvent(self))
