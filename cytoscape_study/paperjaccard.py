# 查询两篇文章相似度 4.17
import json
from urllib import parse
from flask import Flask, request, flash, render_template, jsonify, url_for
from py2neo import Graph, Node, Relationship, NodeMatcher
from flask_cors import CORS, cross_origin
app = Flask(__name__,template_folder='templates')
cors = CORS(app, resources={r"/YOURAPP/*": {"origins": "*"}})
# 数据库密码记得改
app.config['JSON_AS_ASCII'] = False
graph = Graph("http://localhost:7474",auth=("neo4j","xhyzsq123"))
app.config['SECRET_KEY'] = 'SECRET_KEY'


global fir,sec # 全局变量保存文章题目


@app.route('/base')
def base():
    return render_template('base.html')


# 转到前端查询页面
@app.route('/paperjaccard')
def paperjaccard():
    return render_template('paperjaccard.html')


# 返回查询的两篇文章标题，用全局变量保存
@app.route('/paperjac_title',methods=['GET','POST'])
def paperjac_title():

    req = parse.unquote(json.dumps(request.get_data(as_text=True)))
    fir = req.split("&", -1)[0].split("=", -1)[1]
    sec = req.split("&", -1)[1].split("=", -1)[1].split('"', -1)[0]
    print(fir)
    print(sec)
    return '1'


@app.route('/p2r')
def p2r():

    print('进入到主方法')
    print(fir)
    print(sec)

    # 计算输出两个文章之间的jaccard相似度
    paperList = graph.run("".format()).data()

    p_from = 'fir文章'
    p_to = 'sec文章'
    jaccardsim = 0.0542


if __name__ == '__main__':
    app.run()