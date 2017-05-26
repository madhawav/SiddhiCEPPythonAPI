package org.wso2.siddhi.pythonapi.proxy.core;

import org.wso2.siddhi.core.ExecutionPlanRuntime;
import org.wso2.siddhi.core.SiddhiManager;
import org.wso2.siddhi.core.config.ExecutionPlanContext;
import org.wso2.siddhi.core.debugger.SiddhiDebugger;
import org.wso2.siddhi.core.event.Event;
import org.wso2.siddhi.core.query.output.callback.QueryCallback;
import org.wso2.siddhi.pythonapi.proxy.core.query.output.callback.query_callback.QueryCallbackProxy;
import org.wso2.siddhi.pythonapi.proxy.core.query.output.callback.query_callback.ReceiveCallbackProxy;
import org.wso2.siddhi.pythonapi.proxy.core.stream.output.callback.stream_callback.StreamCallbackProxy;

/**
 * Created by madhawa on 5/21/17.
 */
public class SiddhiAPICoreProxy {
    /**
     * Initiates a new Siddhi Manager and return instance to Python API
     * @return new SiddhiManager Instance
     */
    public SiddhiManager initSiddhiManager(){
        return new SiddhiManager();
    }

    public void addExecutionPlanRuntimeQueryCallback(ExecutionPlanRuntime executionPlanRuntime, String name, final QueryCallbackProxy queryCallbackProxy)
    {
        executionPlanRuntime.addCallback(name, queryCallbackProxy);


    }

    public void addExecutionPlanRuntimeStreamCallback(ExecutionPlanRuntime executionPlanRuntime, String name, final StreamCallbackProxy streamCallbackProxy)
    {
        executionPlanRuntime.addCallback(name, streamCallbackProxy);


    }
}
