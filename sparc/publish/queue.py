import transaction
from ZODB.POSException import ConflictError
from zope.component import adapts
from zope.component import queryAdapter
from zope.event import notify
from zope.interface import implements
from zc.queue.interfaces import IQueue
from sparc.publish import RecoverablePublishingError
from sparc.publish import IPublisher
from sparc.publish import IPublisherQueue
from sparc.publish.events import PublisherQueuePublishedEvent

from sparc.logging import logging
logger = logging.getLogger(__name__)

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
            transaction.commit()
        except ConflictError,e : # queue concurrency exception...expected
            if logger.getEffectiveLevel() == logging.DEBUG:
                logger.exception("ConflictError while publishing queue, " +\
                        "transaction aborted.  This error is an expected " +\
                        "runtime condition and does not necessarily " +\
                        "indicate an application issue")
            transaction.abort() # exception means item is already queued...nothing to do
            raise e

    def publish(self):
        """Publish each queued object and empty queue"""
        _return = []
        while self.context:
            try:
                item = self.context.pull()
                transaction.commit()
            except ConflictError: # queue concurrency exception...expected
                if logger.getEffectiveLevel() == logging.DEBUG:
                    logger.exception("ConflictError while publishing queue, " +\
                        "transaction aborted.  This error is an expected " +\
                        "runtime condition and does not necessarily " +\
                        "indicate an application issue")
                transaction.abort()
                """If we plan on reusing this database session we must create a new transaction"""
                self.connection.newTransaction()
                continue # skip to next loop
            # TODO: Add tests for re-queing on publishing errors
            try:
                IPublisher(item).publish()
                _return.append(item)
            except RecoverablePublishingError:
                if item:
                    self.enqueue(item) # add item back into queue for publishing exceptions
                logger.exception("A recoverable publishing error has occured "+\
                                 "for queued item %s.  The item will be " +\
                                 "added back in the publishing queue." )
        notify(PublisherQueuePublishedEvent(self))
        return _return
