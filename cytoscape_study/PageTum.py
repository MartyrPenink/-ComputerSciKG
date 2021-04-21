# 保存简单的页面跳转的路由

from flask import Blueprint, render_template

pagetum = Blueprint('pagetum', __name__)  # 创建蓝图


# 主页面
@pagetum.route('/pagetum/base')
def base():
    return render_template('base.html')


# 通过作者查询文章 查询界面
@pagetum.route('/pagetum/inquery_a2p')
def inquery_a2p():
    return render_template('inquery_a2p.html')


# 通过关键词查询文章 查询界面
@pagetum.route('/pagetum/inquery_k2p')
def inquery_k2p():
    return render_template('inquery_k2p.html')


# 通过文章查询属性 查询界面
@pagetum.route('/pagetum/inquery_p2a')
def inquery_p2a():
    return render_template('inquery_p2a.html')


 # 通过文章查询关系 查询界面
@pagetum.route('/pagetum/inquery_p2r')
def inquery_p2r():
    return render_template('inquery_p2r.html')


