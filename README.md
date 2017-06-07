# Siddhi CEP Python API
The scope of this project is to develop a Python Wrapper on Siddhi CEP Library. Additionally, the Python API would support Siddhi Configuration on WSO2 Data Analytics Server (DAS). The Python wrapper would support Siddhi 3.1, Siddhi 4.0, WSO2 DAS 3.1 and WSO2 DAS 4.0. 

This is currently a work in progress, as a project for Google Summer of Code 2017 Program.

Project Goals
-----
1) Develop a Python Wrapper on Siddhi Java Library 3.1 and 4.0.
2) Extend Python API in (1) to support interactions with WSO2 Data Analytics Server 3.1 and 4.0.
3) Testing, Documentation and Deployment

Current Progress
-----
Currently, the project is in very early stage with discussions on the scope. 
- [x] Wrapping basic features of Siddhi CEP Core 3.1 and 4.0
- [x] Wrapping Siddhi Debugger
- [ ] Wrapping Events Class
- [ ] Unit Tests on Siddhi Debugger - Test 4 Not Passing

Running the Tests
-----
1. Install following pre-requisites
    - Python 3.x
    - Cython (`sudo apt-get install cython`)
    - Pyjnius (`sudo pip install pyjnius`)
    - Python3 Developer Package (`sudo apt-get install python3-dev`)
    - Maven
2. Compile Java Libraries
    - Navigate to `SiddhiCEPPythonAPI/SiddhiCEP3/ProxyClasses/SiddhiCEP3Proxy` and run `mvn install`
    - Navigate to `SiddhiCEPPythonAPI/SiddhiCEP4/ProxyClasses/SiddhiCEP4Proxy` and run `mvn install`
    - Navigate to ``SiddhiCEPPythonAPI/SiddhiCEP4/ProxyClasses/SiddhiCEP3Proxy/c_code` and run `build.sh`*
    - Navigate to ``SiddhiCEPPythonAPI/SiddhiCEP4/ProxyClasses/SiddhiCEP4Proxy/c_code` and run `build.sh`*
    - Run the tests cases in `SiddhiCEPPythonAPI/Tests` directory

*If build.sh throws errors, check the paths provided for imports of Python3 Developer Headers

Background
-----
Siddhi CEP is a Query Language and a Library for Realtime Streaming Complex Event Processing developed by WSO2 Inc. Siddhi CEP is currently used in WSO2 Data Analytics Server, an Enterprise Level Open Source Data Analytics Solution. 

Further information on above products are available in the links below.

- Siddhi 4.0 Library (In Development Version)
    - GitHub - https://github.com/wso2/siddhi
- Siddhi 3.1 Library (Stable Release)
    - GitHub - https://github.com/wso2/siddhi/tree/3.1.x
    - Documentation - https://docs.wso2.com/display/CEP420/SiddhiQL+Guide+3.1
- WSO2 Data Analytics Server 4.0 (In Development Version)
    - GitHub - https://github.com/wso2/product-das
    - Documentation - https://docs.wso2.com/display/DAS400/Quick+Start+Guide
- WSO2 Data Analytics Server 3.1 (Stable Release)
    - Release - http://wso2.com/smart-analytics
    - GitHub - https://github.com/wso2/product-das/tree/release-3.1.0-RC3
    - Documentation - https://docs.wso2.com/display/DAS310/WSO2+Data+Analytics+Server+Documentation

Contact
-----
Madhawa - madhawavidanapathirana@gmail.com

#GSoC2017 #WSO2
