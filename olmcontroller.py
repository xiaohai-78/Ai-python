from flask import Flask, render_template, request, redirect, url_for, jsonify
from service import send

app = Flask(__name__)


@app.route('/post', methods=['POST'])
def post():
    data = request.get_json()
    print(data)
    return "success"


@app.route('/news/get', methods=['POST'])
def newsGet():
    # 尝试获取JSON数据
    data = request.json
    # 检查data是否是一个字典并且包含'context'键
    if data and isinstance(data, dict) and 'context' in data:
        context = data['context']
        # 打印context的内容
        print("requestStr: " + context)
        responseStr = send(context)
        print("responseStr: " + responseStr)
        # 返回成功的响应
        return jsonify({"message": "success", "context": responseStr})
    else:
        # 如果没有找到context参数，返回错误
        return jsonify({"error": "Invalid request, 'context' parameter not found."}), 400



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=7678)

