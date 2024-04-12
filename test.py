import requests
import socketclient

r = requests.get("http://localhost:8000/test") # server prints "test"
cl = socket.Client()
cl2 = socket.Client()


@cl.on("event_name")
def foo(data):
    print(f"client 1 {data}")


@cl2.on("event_name")
def foo2(data):
    print(f"client 2 {data}")


cl.connect("http://localhost:8000/") # server prints "on connect"
cl2.connect("http://localhost:8000/")
cl.emit("direct", "msg_1") # prints client 1 msg_1
cl2.emit("broadcast", "msg_2") # prints client 2 msg_2 and client 1 msg_2