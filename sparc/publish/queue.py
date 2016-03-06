import transaction
from ZODB.POSException import ConflictError
from zope.component import adapts
from zope.component import queryAdapter
from zope.event import notify
from zope.interface import implements
from zc.queue.interfaces import IQueue
from sparc.publish import IPublisher
from sparc.publish import IPublisherQueue
from sparc.publish.events import PublisherQueuePublishedEvent

class PublisherQueueForZCQueue(object):
    """A queue of objects that can be published
    
    This adapter allows for a thread-safe, concurrent-safe ZODB-based queue
    """
    implements(IPublisherQueue)
    adapts(IQueue)
    
    def __init__(self, context):
        self.context = context # concurrency-safe persistent queue implementation
    
    # IPublisherQueue
    def enqueue(self, item):
        """Add object into the queue"""
        if not queryAdapter(item, IPublisher):
            raise TypeError('could not adapt.  expected item to be adaptable to IPublisher')
        try:
            self.context.put(item)
            transaction.savepoint() #subtransaction to verify item could be added
        except ConflictError:
            pass # item is already in queue...so we'll silently ignore

    def publish(self):
        """Publish each queued object and empty queue"""
        while self.context:
            try:
                item = self.context.pull()
                transaction.savepoint()
                IPublisher(item).publish()
            except ConflictError:
                pass # item was already pulled...so we'll silently ignore
        notify(PublisherQueuePublishedEvent(self))
