import json
import uuid
import time


def body_to_dict(data):
    data = data.body
    if isinstance(data, bytes):
        data = data.decode('utf-8')
    if isinstance(data, str):
        data = json.loads(data)
    return data


def response_json():
    data = dict()
    data['code'] = 200
    data['data'] = []
    data['extra'] = {}
    data['message'] = ''
    data['request_id'] = str(uuid.uuid1())
    # data['request_time'] = time.time()
    # data['response_time'] = time.time()
    return data


def get_time_stamp(ctime):
    local_time = time.localtime(ctime)
    data_head = time.strftime("%Y-%m-%d_%H-%M-%S", local_time)
    data_secs = (ctime - int(ctime)) * 1000
    time_stamp = "%s-%03d" % (data_head, data_secs)
    return time_stamp
