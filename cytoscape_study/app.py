from flask import Flask
from cytoscape_study.PageTum import pagetum
from cytoscape_study.Author2Paper import author2paper
from cytoscape_study.Keyword2Paper import keyword2paper
from cytoscape_study.Paper2Attr import paper2attr
from cytoscape_study.Paper2Rela import paper2rela

app = Flask(__name__)
# 数据库密码记得改
app.config['JSON_AS_ASCII'] = False

app.config['SECRET_KEY'] = 'SECRET_KEY'

app.register_blueprint(pagetum)  # 添加 简单的页面跳转 蓝图
app.register_blueprint(author2paper)  # 添加 作者->文章 蓝图
app.register_blueprint(keyword2paper)  # 添加 关键词->文章 蓝图
app.register_blueprint(paper2attr)  # 添加 文章->属性 蓝图
app.register_blueprint(paper2rela)  # 添加 文章->关系 蓝图


# 入口
if __name__ == '__main__':
    app.run(debug=True)
