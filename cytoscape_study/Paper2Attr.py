# 通过 文章->属性 相关方法
import json
from urllib import parse
from flask import Flask, request, render_template, Blueprint, session
from py2neo import Graph

paper2attr = Blueprint('paper2attr', __name__)  # 创建蓝图


# 保存前端传入的论文题目 处理数据 储存数据在session中
@paper2attr.route('/paper2attr/data_p2a',methods=['GET','POST'])
def data_p2a():

    req = parse.unquote(json.dumps(request.get_data(as_text=True)))
    p2a_name = req.split("=", -1)[1].split('"', -1)[0]
    print(p2a_name)

    graph = Graph("http://localhost:7474", auth=("neo4j", "xhyzsq123"))
    paperList = graph.run("MATCH (n:Paper)  where n.title='{0}' RETURN n".format(p2a_name)).data()

    n1_ = json.dumps(paperList[0], ensure_ascii=False)
    n1 = json.loads(n1_)

    p_data = n1['n']
    print('data_p2a方法')
    print(type(p_data))
    print(p_data)

    # 将对象保存在session中
    # session.clear()
    session.permanent = True
    session['id'] = p_data['id']
    session['p_time'] = p_data['p_time']
    session['journal'] = p_data['journal']
    session['quote'] = p_data['quote']
    session['author'] = p_data['author']
    session['link'] = p_data['link']
    session['title'] = p_data['title']
    session['keyword'] = p_data['keyword']
    session['downnum'] = p_data['downnum']

    return '1'


@paper2attr.route('/paper2attr/index_p2a')
def index_p2a():
    p_data = {'p_time': session.get('p_time'), 'journal': session.get('journal'), 'quote': session.get('quote'), 'author': session.get('author'), 'link': session.get('link'),
             'id': session.get('id'), 'title': session.get('title'), 'keyword': session.get('keyword'), 'downnum': session.get('downnum')}
    print('index_p2a方法')
    print(p_data)
    print(type(p_data))

    return render_template("index_p2a.html",p_data = p_data)
