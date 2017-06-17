"""Sandbox App"""
import os
import socket
from flask import Flask
from redis import Redis, RedisError

# Connect to Redis
REDIS = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

APP = Flask(__name__)

@APP.route("/")
def hello():
    """Default route output"""
    try:
        visits = REDIS.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv("NAME", "world"),
                       hostname=socket.gethostname(), visits=visits)

if __name__ == "__main__":
    APP.run(host='0.0.0.0', port=80)
