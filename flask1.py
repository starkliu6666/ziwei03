
# Flask api，终于调试成功了，用了7.29一天！！！！
# 非常奇怪，不加def get_astro()这段，就会报错！！！！！后来发现了，全局初始化 可能不行，def get_chart():里加这段就可以了
# try:
#             from py_iztro import Astro
#             astro = Astro()
#         except Exception as e:
#             return jsonify({"success": False, "error": f"Astro初始化失败: {e}"}), 500
#

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def get_astro():
    try:
        from py_iztro import Astro
        return Astro()
    except ImportError:
        raise Exception("py_iztro 库未正确安装")


@app.route('/ziwei/chart', methods=['POST'])
def get_chart():
    try:

        data = request.get_json()

        solar_date_str = data.get("solar_date_str")
        time_index = data.get("time_index")
        gender = data.get("gender")

        # 计算紫微斗数
        astro = get_astro()
        result = astro.by_solar(solar_date_str, time_index, gender)
        return jsonify({"success": True, "data": result.model_dump()})
        # model_dump_json(by_alias = True, indent = 4)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)