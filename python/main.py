import paho.mqtt.client as paho
import paho.mqtt as mqtt
import time

HOST = "test.mosquitto.org"
CLIENTID = "mqttPaho"
TOPIC = "/$_fluzzy$$cadabra/Nö/Temperature";
MIN_VALUE = -50
MAX_VALUE = 50

def _do_publish(c):
    """Internal function"""
    m = c._userdata.pop()
    if type(m) is dict:
        topic = m['topic']
        try:
            payload = m['payload']
        except KeyError:
            payload = None
        try:
            qos = m['qos']
        except KeyError:
            qos = 0
        try:
            retain = m['retain']
        except KeyError:
            retain = False
    elif type(m) is tuple:
        (topic, payload, qos, retain) = m
    else:
        raise ValueError('message must be a dict or a tuple')

    c.publish(topic, payload, qos, retain)


def _on_connect(c, userdata, flags, rc):
    """Internal callback"""
    if rc == 0:
        _do_publish(c)
    else:
        raise mqtt.MQTTException(paho.connack_string(rc))


def _on_publish(c, userdata, mid):
    """Internal callback"""
    if len(userdata) == 0:
        c.disconnect()
    else:
        _do_publish(c)


def multiple(msgs, hostname="localhost", port=1883, client_id="", keepalive=60,
             will=None, auth=None, tls=None, protocol=paho.MQTTv311, transport="tcp"):
    """Publish multiple messages to a broker, then disconnect cleanly.

    This function creates an MQTT client, connects to a broker and publishes a
    list of messages. Once the messages have been delivered, it disconnects
    cleanly from the broker.

    msgs : a list of messages to publish. Each message is either a dict or a
           tuple.

           If a dict, only the topic must be present. Default values will be
           used for any missing arguments. The dict must be of the form:

           msg = {'topic':"<topic>", 'payload':"<payload>", 'qos':<qos>,
           'retain':<retain>}
           topic must be present and may not be empty.
           If payload is "", None or not present then a zero length payload
           will be published.
           If qos is not present, the default of 0 is used.
           If retain is not present, the default of False is used.

           If a tuple, then it must be of the form:
           ("<topic>", "<payload>", qos, retain)
    hostname : a string containing the address of the broker to connect to.
               Defaults to localhost.
    port : the port to connect to the broker on. Defaults to 1883.
    client_id : the MQTT client id to use. If "" or None, the Paho library will
                generate a client id automatically.
    keepalive : the keepalive timeout value for the client. Defaults to 60
                seconds.
    will : a dict containing will parameters for the client: will = {'topic':
           "<topic>", 'payload':"<payload">, 'qos':<qos>, 'retain':<retain>}.
           Topic is required, all other parameters are optional and will
           default to None, 0 and False respectively.
           Defaults to None, which indicates no will should be used.
    auth : a dict containing authentication parameters for the client:
           auth = {'username':"<username>", 'password':"<password>"}
           Username is required, password is optional and will default to None
           if not provided.
           Defaults to None, which indicates no authentication is to be used.
    tls : a dict containing TLS configuration parameters for the client:
          dict = {'ca_certs':"<ca_certs>", 'certfile':"<certfile>",
          'keyfile':"<keyfile>", 'tls_version':"<tls_version>",
          'ciphers':"<ciphers">}
          ca_certs is required, all other parameters are optional and will
          default to None if not provided, which results in the client using
          the default behaviour - see the paho.mqtt.client documentation.
          Defaults to None, which indicates that TLS should not be used.
    transport : set to "tcp" to use the default setting of transport which is
          raw TCP. Set to "websockets" to use WebSockets as the transport.
    """

    if type(msgs) is not list:
        raise ValueError('msgs must be a list')

    client = paho.Client(client_id=client_id,
                         userdata=msgs, protocol=protocol, transport=transport)
    client.on_publish = _on_publish
    client.on_connect = _on_connect

    if auth is not None:
        username = auth['username']
        try:
            password = auth['password']
        except KeyError:
            password = None
        client.username_pw_set(username, password)

    if will is not None:
        will_topic = will['topic']
        try:
            will_payload = will['payload']
        except KeyError:
            will_payload = None
        try:
            will_qos = will['qos']
        except KeyError:
            will_qos = 0
        try:
            will_retain = will['retain']
        except KeyError:
            will_retain = False

        client.will_set(will_topic, will_payload, will_qos, will_retain)

    if tls is not None:
        ca_certs = tls['ca_certs']
        try:
            certfile = tls['certfile']
        except KeyError:
            certfile = None
        try:
            keyfile = tls['keyfile']
        except KeyError:
            keyfile = None
        try:
            tls_version = tls['tls_version']
        except KeyError:
            tls_version = None
        try:
            ciphers = tls['ciphers']
        except KeyError:
            ciphers = None
        client.tls_set(ca_certs, certfile, keyfile, tls_version=tls_version,
                       ciphers=ciphers)

    client.connect(hostname, port, keepalive)
    client.loop_forever()


def single(topic, payload=None, qos=0, retain=False, hostname="localhost",
           port=1883, client_id="", keepalive=60, will=None, auth=None,
           tls=None, protocol=paho.MQTTv311, transport="tcp"):
    """Publish a single message to a broker, then disconnect cleanly.

    This function creates an MQTT client, connects to a broker and publishes a
    single message. Once the message has been delivered, it disconnects cleanly
    from the broker.

    topic : the only required argument must be the topic string to which the
            payload will be published.
    payload : the payload to be published. If "" or None, a zero length payload
              will be published.
    qos : the qos to use when publishing,  default to 0.
    retain : set the message to be retained (True) or not (False).
    hostname : a string containing the address of the broker to connect to.
               Defaults to localhost.
    port : the port to connect to the broker on. Defaults to 1883.
    client_id : the MQTT client id to use. If "" or None, the Paho library will
                generate a client id automatically.
    keepalive : the keepalive timeout value for the client. Defaults to 60
                seconds.
    will : a dict containing will parameters for the client: will = {'topic':
           "<topic>", 'payload':"<payload">, 'qos':<qos>, 'retain':<retain>}.
           Topic is required, all other parameters are optional and will
           default to None, 0 and False respectively.
           Defaults to None, which indicates no will should be used.
    auth : a dict containing authentication parameters for the client:
           auth = {'username':"<username>", 'password':"<password>"}
           Username is required, password is optional and will default to None
           if not provided.
           Defaults to None, which indicates no authentication is to be used.
    tls : a dict containing TLS configuration parameters for the client:
          dict = {'ca_certs':"<ca_certs>", 'certfile':"<certfile>",
          'keyfile':"<keyfile>", 'tls_version':"<tls_version>",
          'ciphers':"<ciphers">}
          ca_certs is required, all other parameters are optional and will
          default to None if not provided, which results in the client using
          the default behaviour - see the paho.mqtt.client documentation.
          Defaults to None, which indicates that TLS should not be used.
    transport : set to "tcp" to use the default setting of transport which is
          raw TCP. Set to "websockets" to use WebSockets as the transport.
    """

    msg = {'topic':topic, 'payload':payload, 'qos':qos, 'retain':retain}
    multiple([msg], hostname, port, client_id, keepalive, will, auth, tls, protocol, transport)

if __name__ == "__main__":
    while True:
        # get user input from commandline
        print("Enter new temperature between -50 and 50: ")
        inp = input()

        # exit programm
        if inp == 'exit':
            exit()
        
        # check if user has typed in a valid value
        try:
            value = int(inp)

            if value < -50 or value > 50:
                raise ValueError

            # send publish message
            single(topic=TOPIC, payload=value, qos=2, hostname=HOST, client_id=CLIENTID)
        except ValueError:
            print('Not a valid temparature! Has to be a value between %d and %d' % (MIN_VALUE, MAX_VALUE))
            
        time.sleep(2)