# Configuration (this package only)
from importlib import import_module
from sparc.configuration.zcml import Configure as SparcConfigure
def Configure():
    SparcConfigure([import_module(__name__),
                    import_module('zope.annotation')])
def ConfigureTest():
    SparcConfigure([import_module(__name__),
                    import_module('zope.annotation'),
                    import_module('sparc.entity')])

from interfaces import IPublisher
from interfaces import IPublisherQueue
from interfaces import IPublisherQueuePublishedEvent
from interfaces import IPublishEvent