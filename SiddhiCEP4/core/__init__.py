import SiddhiCEP4

#Start JVM
from jnius import autoclass

#Retrieve access
siddhi_api_core = autoclass("org.wso2.siddhi.pythonapi.proxy.core.SiddhiAPICoreProxy")
siddhi_api_core_inst = siddhi_api_core()
