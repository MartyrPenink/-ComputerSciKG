# 从数据库中取数据 现已没用
from py2neo import Node, Graph, RelationshipMatcher, NodeMatcher


class getDatas():
    def __init__(self):
        self.graph = Graph("http://localhost//:7474", username="neo4j", password="2922610627")

    def creatIndex(self):
        self.graph.run('CREATE index on :`文章`(title)')
        self.graph.run('CREATE index on:`关键词`(name)')
        self.graph.run('CREATE index on:`作者`(name)')
        self.graph.run('CREATE index on:`来源单位`(name)')

    # 传入author作者名字
    def authorToPaper(self, author):
        # matcher = NodeMatcher(self.graph)
        # matcher.match('文章',author=author)
        paperList = self.graph.run(
            "MATCH (n1:`文章`)-[r:Author]->(n2:`作者`) where n2.name='{0}' RETURN  n1,r ,n2".format(author)).data()
        print(paperList)
        return paperList

    # 传入一个关键词列表，列表元素为关键词
    def keywordToPaper(self, list):
        paper = []
        lens = len(list)
        # nodeMatcher=NodeMatcher(self.graph)
        # reMatcher=RelationshipMatcher(self.graph)
        if lens == 1:
            # a=nodeMatcher.match('文章')
            # b=nodeMatcher.match('关键词',name=keyword)
            # reMatcher.match(r_type='Keyword')
            paper = self.graph.run(
                "MATCH p=(n:`文章`)-[r:Keyword]->(n1:`关键词`) where n1.name={0} RETURN n,r,n1".format(list[0])).data()

        # elif lens == 2:
        #     sql = "MATCH p=(n:`文章`)-[r:Keyword]->(n1:`关键词`) ,p2=(n:`文章`)-[r2:Keyword]->(n2:`关键词`) where " \
        #           "n1.name='{0}' and n2.name='{1}' RETURN p,p2".format(list[0], list[1])
        #     paper = self.graph.run(sql).data()
        # elif lens == 3:
        #     sql = "MATCH p=(n:`文章`)-[r:Keyword]->(n1:`关键词`) ,p2=(n:`文章`)-[r2:Keyword]->(n2:`关键词`),p3=(n:`文章`)-[r2:Keyword]->(n2:`关键词`) where " \
        #           "n1.name='{0}' and n2.name='{1}'and n3.name='{2}' RETURN p,p2,p3".format(list[0], list[1], list[2])


        return paper

    # 传入文章名字，查询文章属性
    def titleToPropety(self, title):
        sql = "MATCH (n:`文章`)  where n.title='{0}' RETURN n.author,n.keyword,n.organ".format(title)
        list = self.graph.run(sql).data()
        print(list)
        return list

    # 传入文章名字，返回文章关系图
    def paperToRelation(self,title):
        sql="MATCH (n:`文章`)-[r]->(n1) where n.title={0} RETURN n,r,n1".format(title)
        list = self.graph.run(sql).data()
        return list


    # 计算两个文章之间的jaccard相似度,
    def paperJaccardSimilarity(self, title):

        sql = '''
        MATCH (p1:`文章`)-[:Keyword]->(cuisine1)
        where p1.title='{0}'
        WITH p1, collect(id(cuisine1)) AS p1Cuisine
        MATCH (p2:`文章` )-[:Keyword]->(cuisine2)
        where p2.title='{1}'
        WITH p1, p1Cuisine, p2, collect(id(cuisine2)) AS p2Cuisine
        RETURN p1.title AS from,
        p2.title AS to,
        algo.similarity.jaccard(p1Cuisine, p2Cuisine) AS similarity
        '''.format(title[0], title[1])
        list = self.graph.run(sql).data()
        print(list)
        return list
    #def KeywordCentrality(self):


if __name__ == '__main__':
    author = '欧阳英'
    keywordList = ['政府治理', '人工智能']
    title = "智能革命与国家治理现代化初探"
    titles = ['论人工智能技术对人类社会发展的影响', '“人工智能+”时代的个性化学习理论重思与开解']
    getDatas().creatIndex()
    # getDatas().authorToPaper(author)
    # getDatas().keywordToPaper(keywordList)
    # getDatas().titleToPropety(title)
    #getDatas().paperJaccardSimilarity(titles)
