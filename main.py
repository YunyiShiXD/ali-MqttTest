from linkkit import linkkit
import time, logging, random  # 应对异步调用


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
lk.thing_setup(r"C:\Users\Moria\Desktop\ali-MqttTest\MQTT.json")  # 物模型路径


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


# 上报属性
def on_thing_prop_post(request_id, code, data, message, userdata):
    print("on_thing_prop_post request id:%s, code:%d, data:%s message:%s" %
          (request_id, code, str(data), message))


def on_thing_prop_changed(message, userdata):
    if "messSend" in message.keys():
        prop_data["messSend"] = message["messSend"]
    lk.thing_post_property(message)


def on_thing_enable(userdata):
    print("用户可以进行属性上报")


def on_thing_disable(userdata):
    print("on_thing_disable")


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

lk.on_thing_prop_changed = on_thing_prop_changed
# 注册上报云端消息的方法
lk.on_thing_prop_post = on_thing_prop_post
lk.on_thing_enable = on_thing_enable
lk.on_thing_disable = on_thing_disable

# 连接阿里云的数据（异步调用）
lk.connect_async()
# 异步调用需设置延时函数
time.sleep(2)
# 订阅主题
rc, mid = lk.subscribe_topic(lk.to_full_topic("user/get"))


# 模拟设备属性
# prop_data = {"Mqtt_Test:SendResult": 0}


# 上报信息至云平台
countFlag = 10
while countFlag > 1:
    prop_data = {"Mqtt_Test:SendResult": 0}
    rc, request_id = lk.thing_post_property({**prop_data})
    if rc == 0:
        logging.info("thing_post_property success:%r,mid:%r,\npost_data:%s" % (rc, request_id, prop_data))
    else:
        logging.warning("thing_post_property failed:%d" % rc)
    events = ("Error", {"ErrorCode": random.randint(0, 5)})
    rc1, request_id1 = lk.thing_trigger_event(events)
    if rc1 == 0:
        logging.info("thing_trigger_event success:%r,mid:%r,\npost_data:%s" % (rc1, request_id1, events))
    else:
        logging.warning("thing_trigger_event failed:%d" % rc)
    time.sleep(60)
    countFlag -= 1


