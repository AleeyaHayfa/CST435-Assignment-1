import time

def bubble_sort_one_pass(arr):
    n = len(arr)
    for j in range(0, n - 1):
        if arr[j] > arr[j+1]:
            arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def process_payload(payload, service_name):
    numbers = payload['data']
    p_start = time.time_ns()

    bubble_sort_one_pass(numbers)
    time.sleep(0.01) 

    p_end = time.time_ns()
    my_work = p_end - p_start
    
    payload['processing_ns'] += my_work
    
    step_details = {
        'service': service_name,
        'result_snapshot': list(numbers), 
        'work_time': my_work
    }
    payload['trace'].append(step_details)
    
    return payload
