import SiddhiCEP4
import sys

#Start JVM
from jnius import autoclass

#Retrieve access

siddhi_api_core = autoclass("org.wso2.siddhi.pythonapi.proxy.core.SiddhiAPICoreProxy")
siddhi_api_core_inst = siddhi_api_core(sys.version_info[0],sys.version_info[1])

#initEventPolling
from SiddhiCEP4 import EventPoller
event_polling_instance = EventPoller.EventPoller()
event_polling_instance.initEventPolling()