from linkkit import linkkit
import time  # 应对异步调用
import sys
import logging


# config log
__log_format = '%(asctime)s-%(process)d-%(thread)d - %(name)s:%(module)s:%(funcName)s - %(levelname)s - %(message)s'
logging.basicConfig(format=__log_format)


# 设置连接参数，方法为“一机一密”型
# 设置“一机一密”型设备连接参数
HostName = "cn-shanghai"
ProductKey = "hha9ADVAKLS"
DeviceName = "test_01"
DeviceSecret = "ce6d83a0e423a765e9d92c17fae27c81"


lk = linkkit.LinkKit(
    host_name=HostName,  # mqttHostUrl
    product_key=ProductKey,
    device_name=DeviceName,
    device_secret=DeviceSecret
)

lk.enable_logger(logging.DEBUG)
lk.thing_setup('https://iotx-tsl.oss-ap-southeast-1.aliyuncs.com/schema.json')  # 物模型路径


# 连接阿里云
def on_connect(session_flag, rc, userdata):
    print("on_connect:%d, rc:%d, userdata:" % (session_flag, rc))
    pass


# 断开阿里云连接
def on_disconnect(rc, userdata):
    print("on_disconnect:rc:%d,userdata:" % rc)


# 订阅topic
def on_subscribe_topic(mid, granted_qos, userdata):
    print("on_subscribe_topic mid:%d, granted_qos:%s" %
          (mid, str(','.join('%s' % it for it in granted_qos))))
    pass


# 中止订阅云端数据
def on_unsubscribe_topic(mid, userdata):
    print("on_unsubscribe_topic mid:%d" % mid)
    pass


# 接收云端数据 ★
def on_topic_message(topic, payload, qos, userdata):
    print("on_topic_message:" + topic + " payload:" + str(payload) + " qos:" + str(qos))
    pass


# 调用发布函数，判断发布消息是否成功
def on_publish_topic(mid, userdata):
    print("on_publish_topic mid:%d" % mid)


# # 上报属性
# def on_thing_prop_post(request_id, code, data, message, userdata):
#     logging.info("on_thing_prop_post request id:%s, code:%d message:%s, data:%s,userdata:%s" %
#                  (request_id, code, message, data, userdata))


# 注册接收到云端数据的方法
lk.on_connect = on_connect
# 注册取消接收到云端数据的方法
lk.on_disconnect = on_disconnect
# 注册云端订阅的方法
lk.on_subscribe_topic = on_subscribe_topic
# 注册当接受到云端发送的数据的时候的方法
lk.on_topic_message = on_topic_message
# 注册向云端发布数据的时候顺便所调用的方法
lk.on_publish_topic = on_publish_topic
# 注册取消云端订阅的方法
lk.on_unsubscribe_topic = on_unsubscribe_topic
# 注册上报云端消息的方法
lk.on_thing_prop_post = on_thing_prop_post

# 连接阿里云的数据（异步调用）
lk.connect_async()
# 异步调用需设置延时函数
time.sleep(2)
# 订阅主题
rc, mid = lk.subscribe_topic(lk.to_full_topic("user/get"))

# 发布主题
while True:
    result={
         "result": "ok"
    }
    rc, mid = lk.publish_topic(lk.to_full_topic("user/update"), str(result))
    print("111")
    time.sleep(2)
    pass
