
from flask import Flask ,request
from flask_socketio import SocketIO  

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,cors_allowed_origins="*")

#所有的用户
users = {}

@app.route('/')
def index():
    return 'WebSocket Server Running'

@socketio.on('connect')
def handle_connect():
    print(f"Client connected:{request.sid}")

@socketio.on("register")
def handle_register(data):
    """ 客户端注册用户名 """
    username = data.get("username")
    if username:
        users[username] = request.sid
        print(f"User {username} registered with SID {request.sid}")

# 监听客户端断开
@socketio.on('disconnect')
def handle_disconnect():
    """ 移除用户映射 """
    username = None
    for user, sid in users.items():
        if sid == request.sid:
            username = user
            del users[user]
            print(f"Client {username} disconnected")
            break

@socketio.on('offer')
def handle_offer(data):
    """ 处理客户端发送的 offer 消息 """
    socketio.emit('offer1', data, room=None)

@socketio.on('answer')
def handle_answer(data):
    """ 处理客户端发送的 answer 消息 """
    socketio.emit('answer1', data, room=None)


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)  # ✅ 关闭 `debug=True`