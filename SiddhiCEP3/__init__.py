import logging
import os

source_path = os.path.dirname(os.path.abspath(__file__))

#Test whether Java Library is already loaded
if "siddhi_api_configured" in globals():
    logging.info("Siddhi API already loaded")
    if globals()["siddhi_api_configured"] != 3:
        raise ImportError("Unable to use multiple versions of Siddhi CEP Library")

#Add Java library to class path of jvm
import jnius_config

#NOTE: The following code-line is required on Linux Kernel 4.4.0-81-generic and above to avoid segmentation fault at
#initialization of pyjnius
jnius_config.add_options('-Xss1280k')
jnius_config.add_options('-Djava.library.path=' + source_path + "/")
jnius_config.set_classpath('.', source_path + '/ProxyClasses/SiddhiCEP3Proxy/target/lib/*',source_path + '/ProxyClasses/SiddhiCEP3Proxy/target/*')

global siddhi_api_configured
siddhi_api_configured = 4

logging.info("Classpath Configured")

#Start JVM
from jnius import autoclass