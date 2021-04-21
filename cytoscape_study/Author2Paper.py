# 作者->文章 相关方法
import json
from urllib import parse
from flask import Flask, request, render_template, Blueprint,session
from py2neo import Graph, Node, Relationship, NodeMatcher

author2paper = Blueprint('author2paper', __name__)  # 创建蓝图 蓝图名不能和存在的视图函数重名，不然会冲突

# 接下来三个文件在code.js中被使用

# 返回cytoscape.js的节点json文件
@author2paper.route('/author2paper/nodejson')
def nodejson():
    print('nodejson方法')
    return render_template("node.json")


# 返回cytoscape.js的边json文件
@author2paper.route('/author2paper/edgejson')
def edgejson():
    return render_template("edge.json")


# 返回cytoscape.js的样式json文件
@author2paper.route('/author2paper/cystylejson')
def cystylejson():
    return render_template("cy-style.json")


# 保存前端传入的作者名称 处理数据 储存数据
@author2paper.route('/author2paper/data_a2p',methods=['GET','POST'])
def data_a2p():

    req = parse.unquote(json.dumps(request.get_data(as_text=True)))
    a2p_name = req.split("=", -1)[1].split('"', -1)[0]
    print('data_a2p')
    print(a2p_name)

    # 连接和查询数据库
    graph = Graph("http://localhost:7474", auth=("neo4j", "xhyzsq123"))
    paperList = graph.run("MATCH (n1:Author)-[r:Author]->(n:Paper) where n1.name='{0}' return n1,r,n".format(a2p_name)).data()
    print('得到数据')
    print(paperList)

    # 实体转json 将他变为符合要求的格式
    node_json = '['
    edge_json = '['
    flag = 0
    num = 0
    print(111111111111111111111111)
    for three_pre in paperList:
        # 处理第一个点
        num = num+1
        n1_ = json.dumps(three_pre['n1'], ensure_ascii=False)
        n1 = json.loads(n1_)
        n1_pre = (
        {'data': {'id': n1['id'], 'idInt': int(n1['id']), 'name': n1['name']}, 'group': 'nodes', 'removed': False,
         'selected': False, 'selectable': True, 'locked': False, 'grabbed': False, 'grabbable': True, })
        print(n1_pre)
        # 处理第二个点
        n_ = json.dumps(three_pre['n'], ensure_ascii=False)
        n = json.loads(n_)
        n_pre = ({'data': {'id': n['id'], 'idInt': int(n['id']), 'name': n['title']}, 'group': 'nodes'})
        print(n_pre)
        # 加边
        r_pre = ({'data': {'source': n1['id'], 'target': n['id'], 'id': 'e' + str(flag + 1), 'weight': 0.019493334, },
                  'group': 'edges', 'removed': False, 'selected': False, 'selectable': True, 'locked': False,
                  'grabbed': False, 'grabbable': True, })

        # 往集合里加
        if flag == 0:
            node_json = node_json + json.dumps(n1_pre, ensure_ascii=False) + ',' + json.dumps(n_pre, ensure_ascii=False)  # 这个地方会加很多次相同的n1点 因为n1是作者
            edge_json = edge_json + json.dumps(r_pre, ensure_ascii=False)
        else:
            node_json = node_json + ',' + json.dumps(n1_pre, ensure_ascii=False) + ',' + json.dumps(n_pre, ensure_ascii=False)
            edge_json = edge_json + ',' + json.dumps(r_pre, ensure_ascii=False)

        flag = flag + 1

    node_json = node_json + ']'
    edge_json = edge_json + ']'
    print(num)
    print(11111111111111111)
    # 拼接点和边 将其写入文件中
    with open('./templates/node.json', 'w') as f:
        json.dump(json.loads(node_json), f)
    with open('./templates/edge.json', 'w') as f:
        json.dump(json.loads(edge_json), f)

    session.permanent = True
    session['relanum']= num

    return '1'


# 跳转到 知识图谱 页面
@author2paper.route('/author2paper/index_a2p')
def index_a2p():
    rela_num = {'num' : session.get('relanum')}
    print(rela_num)
    return render_template("index_a2p.html",rela_num = rela_num)

