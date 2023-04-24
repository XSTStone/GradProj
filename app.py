from flask import Flask
from flask import render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


# 模型评估
@app.route('/test', methods=['POST', 'GET'])
def judge():
    data = request.args.to_dict()
    factors = []
    for key in data:
        factors.append(data[key])
    print(factors)

    return render_template('test.html', content=data)


# 葡萄酒相关目录
@app.route('/wine-self')
def wine_index():
    return render_template('')


# 葡萄酒品种
@app.route('/wine-self/cate')
def wine_cate():
    return render_template('')


# 葡萄酒特点
@app.route('/wine-self/feature')
def wine_feature():
    return render_template('')


# 偏门知识
@app.route('/wine-self/fun')
def wine_fun():
    return render_template('')


# 质量概述，影响因素
@app.route('/quality')
def quality_index():
    return render_template('')


# 因素详情
@app.route('/quality/<factor>')
def quality_factor(factor):
    return render_template('%s.html' % factor)

#
# @app.route('/test', methods=['POST', 'GET'])
# def test():
#     data = request.args.to_dict()
#     try:
#         return render_template('test.html', content=data)
#     except:
#         data = '空'
#         return render_template('test.html', content=data)


if __name__ == '__main__':
    app.run()
