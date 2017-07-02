import logging

import sys

import SiddhiCEP4

siddhi_api_core = None
siddhi_api_core_inst = None

_java_method = None
_PythonJavaClass = None
_JavaClass = None

if not "siddhi_api_configured" in globals():
    logging.info("Siddhi API Unable to resume")
else:
    global t_siddhi_api_core, t_siddhi_api_core_inst, t_java_method, t_PythonJavaClass, t_JavaClass

    siddhi_api_core = t_siddhi_api_core
    siddhi_api_core_inst = t_siddhi_api_core_inst
    _java_method = t_java_method
    _PythonJavaClass = t_PythonJavaClass
    _JavaClass = t_JavaClass

def resumeLibrary():
    if not "siddhi_api_configured" in globals():
        logging.info("Siddhi API Unable to resume")
        return
    global t_siddhi_api_core, t_siddhi_api_core_inst, t_java_method, t_PythonJavaClass, t_JavaClass
    global siddhi_api_core, siddhi_api_core_inst, _java_method, _PythonJavaClass, _JavaClass

    siddhi_api_core = t_siddhi_api_core
    siddhi_api_core_inst = t_siddhi_api_core_inst
    _java_method = t_java_method
    _PythonJavaClass = t_PythonJavaClass
    _JavaClass = t_JavaClass


def loadLibrary():
    # Test whether Java Library is already loaded
    if "siddhi_api_configured" in globals():
        logging.info("Siddhi API already loaded")
        if globals()["siddhi_api_configured"] != 4:
            raise ImportError("Unable to use multiple versions of Siddhi CEP Library")
        resumeLibrary()
        return


    # Add Java library to class path of jvm
    import jnius_config

    # NOTE: The following code-line is required on Linux Kernel 4.4.0-81-generic and above to avoid segmentation fault at
    # initialization of pyjnius
    jnius_config.add_options('-Xss1280k')

    jnius_config.add_options('-Djava.library.path=' + SiddhiCEP4.source_path + "/")
    jnius_config.set_classpath('.', SiddhiCEP4.source_path + '/ProxyClasses/SiddhiCEP4Proxy/target/lib/*',
                               SiddhiCEP4.source_path + '/ProxyClasses/SiddhiCEP4Proxy/target/*')

    global siddhi_api_configured
    siddhi_api_configured = 4

    logging.info("Classpath Configured")

    # Start JVM
    from jnius import autoclass, java_method, PythonJavaClass, JavaClass

    # Retrieve access
    global t_siddhi_api_core, t_siddhi_api_core_inst, t_java_method, t_PythonJavaClass, t_JavaClass
    t_siddhi_api_core = autoclass("org.wso2.siddhi.pythonapi.proxy.core.SiddhiAPICoreProxy")
    t_siddhi_api_core_inst = t_siddhi_api_core(sys.version_info[0], sys.version_info[1])
    t_java_method = java_method
    t_PythonJavaClass = PythonJavaClass
    t_JavaClass = JavaClass
    resumeLibrary()

def loadType(type_name):
    loadLibrary()
    from jnius import autoclass
    return autoclass(type_name)