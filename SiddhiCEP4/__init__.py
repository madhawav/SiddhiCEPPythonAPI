import logging
import os

logging.basicConfig(level=logging.INFO)

source_path = os.path.dirname(os.path.abspath(__file__))
print("Source Path:",source_path)
#Add Java library to class path of jvm
import jnius_config
print(jnius_config.get_options())
jnius_config.add_options('-Djava.library.path=' + source_path + "/")
jnius_config.set_classpath('.', source_path + '/ProxyClasses/SiddhiCEP4Proxy/target/lib/*',source_path + '/ProxyClasses/SiddhiCEP4Proxy/target/*')

logging.info("Classpath Configured")

#Start JVM
from jnius import autoclass