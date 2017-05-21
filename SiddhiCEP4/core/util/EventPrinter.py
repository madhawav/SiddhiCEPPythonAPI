import SiddhiCEP4.core #Initializes Runtime
from jnius import autoclass

_event_printer_proxy = autoclass("org.wso2.siddhi.pythonapi.proxy.core.util.EventPrinterProxy")


def PrintEvent(timestamp, inEvents, outEvents):
    '''
    Prints Stream Event to Log
    :param timestamp:
    :param inEvents:
    :param outEvents:
    :return:
    '''

    _event_printer_proxy.printEvent(timestamp,inEvents,outEvents)

    # NOTE: We are unable to call org.wso2.siddhi.core.util.EventPrinter.print directly because print is a keyword of python