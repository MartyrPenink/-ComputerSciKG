# 关键词->文章 相关方法 目前只能查一个关键词 和上一个功能几乎一样 考虑是否可以合并
import json
from urllib import parse
from flask import render_template, Blueprint, request
from py2neo import Graph

keyword2paper = Blueprint('keyword2paper', __name__)  # 创建蓝图


@keyword2paper.route('/keyword2paper/nodejson')
def nodejson():
    return render_template("node.json")


@keyword2paper.route('/keyword2paper/edgejson')
def edgejson():
    return render_template("edge.json")


@keyword2paper.route('/keyword2paper/cystylejson')
def cystylejson():
    return render_template("cy-style.json")


@keyword2paper.route('/keyword2paper/data_k2p',methods=['GET','POST'])
def data_k2p():
    req = parse.unquote(json.dumps(request.get_data(as_text=True)))
    k2p_name = req.split("=", -1)[1].split('"', -1)[0]
    print('data_k2p')
    print(k2p_name)

    graph = Graph("http://localhost:7474", auth=("neo4j", "xhyzsq123"))
    paper = graph.run("MATCH (n:Keyword)-[r:Keyword]->(n1:Paper) where n.keyword={0} RETURN n,r,n1".format('"'+k2p_name+'"')).data()

    print('==========从neo4j取出的数据==========')
    print(paper)
    print('====================')

    print('==========取出关键词节点==========')
    n1_pre = json.loads(json.dumps(paper[0]['n'], ensure_ascii=False)) #变成str
    n1 = ({'data': {'id': n1_pre['id'], 'idInt': int(n1_pre['id']), 'name': n1_pre['keyword']}, 'group': 'nodes'})
    n1_ = json.dumps(n1, ensure_ascii=False) #变成str
    print(n1)
    print('====================')

    node_json = '['
    edge_json = '['
    flag = 0

    for three_pre in paper:

        n_ = json.dumps(three_pre['n1'], ensure_ascii=False)
        print(n_)
        n = json.loads(n_)
        n_pre = (
            {'data': {'id': n['id'], 'idInt': int(n['id']), 'name': n['title']}, 'group': 'nodes', 'removed': False,
         'selected': False, 'selectable': True, 'locked': False, 'grabbed': False, 'grabbable': True})
        r_pre = ({'data': {'source': n1['data']['id'], 'target': n['id'], 'id': 'e' + str(flag + 1),'name':'Keyword','weight': 0.019493334}, 'group': 'edges','removed': False, 'selected': False, 'selectable': True, 'locked': False,
                  'grabbed': False, 'grabbable': True})
        print(r_pre)

        if flag == 0:
            node_json = node_json + json.dumps(n1, ensure_ascii=False) + ',' + json.dumps(n_pre, ensure_ascii=False)
            edge_json = edge_json + json.dumps(r_pre, ensure_ascii=False)
        else:
            node_json = node_json + ',' + json.dumps(n1, ensure_ascii=False) + ',' + json.dumps(n_pre, ensure_ascii=False)
            edge_json = edge_json + ',' + json.dumps(r_pre, ensure_ascii=False)

        flag = flag + 1

    node_json = node_json + ']'
    edge_json = edge_json + ']'
    print(node_json)
    print(edge_json)

    # 拼接点和边 将其写入文件中
    with open('./templates/node.json', 'w') as f:
        json.dump(json.loads(node_json), f)
    with open('./templates/edge.json', 'w') as f:
        json.dump(json.loads(edge_json), f)

    return '1'


# 跳转到 知识图谱 页面
@keyword2paper.route('/keyword2paper/index_k2p')
def index_k2p():
    return render_template("index_k2p.html")