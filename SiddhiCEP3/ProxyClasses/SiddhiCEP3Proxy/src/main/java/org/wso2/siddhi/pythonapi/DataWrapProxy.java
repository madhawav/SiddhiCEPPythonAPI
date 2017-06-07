package org.wso2.siddhi.pythonapi;

/**
 * Created by madhawa on 6/1/17.
 */
public class DataWrapProxy {
    /**
     * Wrapper on Data sent between Python and Java. This wrapper is needed due to following reasons
     * - Python doesnt support long datatype
     * - Pyjnius require uniform data type objects in arrays
     */
    private Object data;
    public DataWrapProxy(int data)
    {
        this.data = data;
    }
    public DataWrapProxy(float data)
    {
        this.data = data;
    }
    public DataWrapProxy(String data)
    {
        this.data = data;
    }
    public DataWrapProxy(int data, boolean isLong)
    {
        this.data = (long)data;
    }
    public boolean isLong(){
        return this.data instanceof Long;
    }
    public boolean isInt(){
        return this.data instanceof Integer;
    }
    public boolean isFloat(){
        return this.data instanceof Float;
    }
    public boolean isString(){
        return this.data instanceof String;
    }

    public Object getData()
    {
        return data;
    }

    public static DataWrapProxy[] wrapArray(Object[] data)
    {
        DataWrapProxy[] results = new DataWrapProxy[data.length];
        for(int i = 0;i < data.length; i++)
            results[i] = DataWrapProxy.wrap(data[i]);
        return results;
    }

    public static DataWrapProxy wrap(Object data) {
        if(data instanceof Integer)
            return new DataWrapProxy((Integer)data);
        else if(data instanceof Long)
            return new DataWrapProxy((Long)data);
        else if(data instanceof String)
            return new DataWrapProxy((String)data);
        else if(data instanceof Float)
            return new DataWrapProxy((Float)data);
        throw new RuntimeException("Unsupported Data Type");
    }

    public static Object[] unwrapArray(DataWrapProxy[] data)
    {
        Object[] results = new Object[data.length];
        for(int i = 0;i < data.length; i++)
            results[i] = data[i].getData();
        return results;
    }


}
