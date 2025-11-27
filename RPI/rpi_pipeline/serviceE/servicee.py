import os,time,requests
from fastapi import FastAPI

SERVICE_NAME="Service E"
PORT=8005
NEXT_SERVICE=None
NEXT_PORT=None
IN_DOCKER=os.environ.get("IN_DOCKER","0")=="1"

app=FastAPI()

def bubble_sort_step(data):
    n=len(data)
    for i in range(n-1):
        if data[i]>data[i+1]: data[i],data[i+1]=data[i+1],data[i]
    return data

@app.get("/health")
def health(): return {"status":"ok","service":SERVICE_NAME}

@app.post("/process")
def process(payload:dict):
    input_data=payload.get("data",[])
    start_ns=time.time_ns()
    processed=bubble_sort_step(input_data.copy())
    time.sleep(0.01)
    work_ns=time.time_ns()-start_ns
    output={"service":SERVICE_NAME,"input":input_data,"data":processed,"processing_ns":work_ns}
    print(f"[{SERVICE_NAME}] processed: {processed} (Work Time: {work_ns} ns)")
    return output

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=PORT)
