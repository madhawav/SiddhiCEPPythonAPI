import logging
import os

logging.basicConfig(level=logging.INFO)

source_path = os.path.dirname(os.path.abspath(__file__))
print("Source Path:",source_path)
#Add Java library to class path of jvm
import jnius_config
print("Options")
print(jnius_config.get_options())

jnius_config.set_classpath('.', source_path + '/ProxyClasses/SiddhiCEP3Proxy/target/lib/*',source_path + '/ProxyClasses/SiddhiCEP3Proxy/target/*')

logging.info("Classpath Configured")

#Start JVM
from jnius import autoclass