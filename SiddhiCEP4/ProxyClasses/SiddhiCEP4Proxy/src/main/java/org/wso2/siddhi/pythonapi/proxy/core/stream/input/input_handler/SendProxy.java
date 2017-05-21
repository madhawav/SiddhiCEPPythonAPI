package org.wso2.siddhi.pythonapi.proxy.core.stream.input.input_handler;

/**
 * Created by madhawa on 5/21/17.
 */
public class SendProxy{
    /**
     * Proxy class used to interface with InputHandler.send method
     */

    private Object[] data;
    private int index = 0;
    public SendProxy(int size)
    {
        data = new Object[size];
    }
    public void putLong(long l)
    {
        data[index++] = l;
    }
    public void putInt(int i)
    {
        data[index++] = i;
    }

    public void putString(String s){
        data[index++] = s;
    }
    public void putFloat(float f){
        data[index++] = f;
    }

    public void putDouble(double d){
        data[index++] = d;
    }

    public void send(org.wso2.siddhi.core.stream.input.InputHandler inputHandler) throws InterruptedException {
        inputHandler.send(data);
    }
}