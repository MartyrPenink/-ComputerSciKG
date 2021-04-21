# 通过 文章->关系 进一步预设是从文章查找二次关系
import json
from urllib import parse
from flask import Flask, request, render_template, Blueprint
from py2neo import Graph

paper2rela = Blueprint('paper2rela', __name__)  # 创建蓝图


# 处理数据 写入json文件
@paper2rela.route('/data_p2r',methods=['GET','POST'])
def data_p2r():
    #用于判断重复节点
    node_set = set()
    #用于计算边数
    edge_num = 0
    req = parse.unquote(json.dumps(request.get_data(as_text=True)))
    p2r_name = req.split("=", -1)[1].split('"', -1)[0]

    # 输出该文章所有的作者和关键词
    graph = Graph("http://localhost:7474", auth=("neo4j", "xhyzsq123"))
    paperList = graph.run("MATCH (n1)-[r]->(n:Paper) where n.title='{0}' RETURN n,r,n1".format(p2r_name)).data()
    print(paperList)

    # 先处理n点 因为都一样
    n_ = json.dumps(paperList[0]['n'], ensure_ascii=False)  # 变成str
    n = json.loads(n_)  # 变成dict/json
    print(n)
    print(type(n))
    print('n是dict字典类型，没有中括号')

    # 实体转json 将他变为符合格式
    node_json = '['
    edge_json = '['
    flag = 0

    # 处理n点
    n_pre = ({'id': str(n['id']),'idInt':int(n['id']), 'name': n['title'], 'keyword': n['keyword'], 'author': n['author'], 'category': 0})
    print(n_pre)
    print(type(n['id']))
    node_set.add(n['id'])

    node_json = node_json + json.dumps(n_pre, ensure_ascii=False)
    print(node_json)

    n1_ = json.dumps(paperList[0]['n1'], ensure_ascii=False)
    n1 = json.loads(n1_)
    print(n1)
    print(n1.get('name', 'not_author'))
    print(n1.get('keyword', -1))

    for three_pre in paperList:

        # 处理n1
        n1_ = json.dumps(three_pre['n1'], ensure_ascii=False)
        n1 = json.loads(n1_)
        if(n1['id'] in node_set):
            continue
        # 判断 是关键词则进入
        if n1.get('name', 'not_author') == 'not_author':
            n1_pre = ({'id': str(n1['id']),'idInt':int(n1['id']), 'name': n1['keyword'], 'category': 1})
            rela = 'Keyword'
        else:
            n1_pre = ({'id': str(n1['id']),'idInt':int(n1['id']), 'name': n1['name'], 'category': 2})
            rela = 'Author'

        # 处理r关系
        r_pre = ({'source': str(n1['id']), 'target': str(n['id']), 'id': 'e' + str(edge_num + 1), 'name': rela})
        edge_num = edge_num + 1

        # 往集合里加
        node_json = node_json + ',' + json.dumps(n1_pre, ensure_ascii=False)

        if flag == 0:
            edge_json = edge_json + json.dumps(r_pre, ensure_ascii=False)
        else:
            edge_json = edge_json + ',' + json.dumps(r_pre, ensure_ascii=False)

        #再往下搜索一层

        if rela == 'Keyword':
            graphlist_2 = graph.run("MATCH (n2)-[r]->(n:Paper) where n2.keyword='{0}' RETURN n,r,n2".format(n1['keyword'])).data()
            for three_pre_2 in graphlist_2:
                n2_ = json.dumps(three_pre_2['n'], ensure_ascii=False)
                n2 = json.loads(n2_)
                print(n2)
                if (n2['id'] in node_set):
                    continue
                n2_pre = ({'id': str(n2['id']),'idInt':int(n2['id']), 'name': n2['title'], 'keyword': n2['keyword'], 'author': n2['author'], 'category': 3})
                node_json = node_json + ',' +json.dumps(n2_pre, ensure_ascii=False)
                r2_pre = ({'source': str(n2['id']), 'target': str(n1['id']), 'id': 'e' + str(edge_num+1), 'name': rela})
                edge_num = edge_num + 1
                edge_json = edge_json + ',' + json.dumps(r2_pre, ensure_ascii=False)

        if rela == 'Author':
            graphlist_2 = graph.run("MATCH (n:Paper) where n.author='{0}' RETURN n".format(n1['name'])).data()
            print('------shuju------------')
            print(graphlist_2)
            print('-----------------------')
            for three_pre_2 in graphlist_2:

                n2_ = json.dumps(three_pre_2['n'], ensure_ascii=False)
                n2 = json.loads(n2_)
                print(n2)
                if (n2['id'] in node_set):
                    continue
                n2_pre = ({'id': str(n2['id']),'idInt':int(n2['id']), 'name': n2['title'], 'keyword': n2['keyword'], 'author': n2['author'], 'category': 3})
                node_json = node_json + ',' +json.dumps(n2_pre, ensure_ascii=False)
                r2_pre = ({'source': str(n2['id']), 'target': str(n1['id']), 'id': 'e' + str(edge_num+1), 'name': rela})
                edge_num = edge_num + 1
                edge_json = edge_json + ',' + json.dumps(r2_pre, ensure_ascii=False)

        flag = flag + 1

    node_json = node_json + ']'
    edge_json = edge_json + ']'

    print(node_json)
    print(type(node_json))
    print(edge_json)
    print(type(edge_json))

    category = '[' + json.dumps(({'name': '您查询的文章'}),ensure_ascii=False) + ',' \
                   + json.dumps(({'name': '关键词'}),ensure_ascii=False) + ',' \
                   + json.dumps(({'name': '作者'}), ensure_ascii=False) + ',' \
                   + json.dumps(({'name': '文章'}), ensure_ascii=False) + ']'

    # 拼接整个json
    json_all = '{"nodes":' + node_json + ',' + '"links":' + edge_json + ',' + '"categories":' + category + '}'  # 字符串类型

    # 写入文件
    with open('./templates/p2r.json', 'w', encoding='utf-8') as f:
        json.dump(json.loads(json_all), f, ensure_ascii=False)

    print('.json already created.')

    return '1'


# 跳转到 知识图谱 页面
@paper2rela.route('/paper2rela/index_p2r')
def index_p2r():
    return render_template("index_p2r.html")

@paper2rela.route('/paper2rela/getjson')
def getjson():
    return render_template('p2r.json')