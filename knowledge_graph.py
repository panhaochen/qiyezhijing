import networkx as nx
from pyvis.network import Network
import json
from typing import Dict, Any, List

class KnowledgeGraphBuilder:
    def __init__(self):
        self.graph = nx.Graph()
    
    def build_knowledge_graph(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """构建企业知识图谱"""
        self.graph.clear()
        
        company_name = company_data["name"]
        
        # 添加中心企业节点
        self._add_company_node(company_name, company_data)
        
        # 添加股东关系
        for shareholder in company_data.get("shareholders", []):
            self._add_shareholder_relation(company_name, shareholder)
        
        # 添加高管关系
        for executive in company_data.get("executives", []):
            self._add_executive_relation(company_name, executive)
        
        # 添加子公司关系
        for subsidiary in company_data.get("subsidiaries", []):
            self._add_subsidiary_relation(company_name, subsidiary)
        
        # 添加上下游供应链关系
        self._add_supply_chain_relations(company_name, company_data.get("supply_chain", {}))
        
        return self._convert_to_vis_format()
    
    def _add_company_node(self, company_name: str, data: Dict[str, Any]):
        """添加企业节点"""
        self.graph.add_node(
            company_name,
            label=company_name,
            group="company",
            title=f"""
            企业名称: {company_name}
            行业: {data.get('industry', '未知')}
            规模: {data.get('scale', '未知')}
            信用评级: {data.get('credit_rating', '未知')}
            """,
            size=40,
            color="#1f77b4"
        )
    
    def _add_shareholder_relation(self, company_name: str, shareholder: Dict[str, Any]):
        """添加股东关系"""
        shareholder_name = shareholder["name"]
        ratio = shareholder.get("ratio", "")
        
        self.graph.add_node(
            shareholder_name,
            label=shareholder_name,
            group="shareholder",
            title=f"持股比例: {ratio}",
            size=25,
            color="#ff7f0e"
        )
        
        self.graph.add_edge(
            company_name, shareholder_name,
            title=f"持股 {ratio}",
            value=2,
            color="#ff7f0e"
        )
    
    def _add_executive_relation(self, company_name: str, executive: Dict[str, Any]):
        """添加高管关系"""
        exec_name = executive["name"]
        position = executive["position"]
        
        self.graph.add_node(
            exec_name,
            label=exec_name,
            group="person",
            title=f"职务: {position}",
            size=20,
            color="#2ca02c"
        )
        
        self.graph.add_edge(
            company_name, exec_name,
            title=f"任职: {position}",
            value=1,
            color="#2ca02c"
        )
    
    def _add_subsidiary_relation(self, company_name: str, subsidiary: str):
        """添加子公司关系"""
        self.graph.add_node(
            subsidiary,
            label=subsidiary,
            group="company",
            title="子公司",
            size=30,
            color="#1f77b4"
        )
        
        self.graph.add_edge(
            company_name, subsidiary,
            title="控股子公司",
            value=3,
            color="#d62728"
        )
    
    def _add_supply_chain_relations(self, company_name: str, supply_chain: Dict[str, Any]):
        """添加供应链关系"""
        # 上游供应商
        for supplier in supply_chain.get("upstream", []):
            self.graph.add_node(
                supplier,
                label=supplier,
                group="supplier",
                title="上游供应商",
                size=20,
                color="#9467bd"
            )
            self.graph.add_edge(
                supplier, company_name,
                title="供应关系",
                value=2,
                color="#9467bd",
                dashes=True
            )
        
        # 下游客户
        for customer in supply_chain.get("downstream", []):
            self.graph.add_node(
                customer,
                label=customer,
                group="customer", 
                title="下游客户",
                size=20,
                color="#8c564b"
            )
            self.graph.add_edge(
                company_name, customer,
                title="客户关系", 
                value=2,
                color="#8c564b",
                dashes=True
            )
    
    def _convert_to_vis_format(self) -> Dict[str, Any]:
        """将NetworkX图转换为PyVis可用的格式"""
        nodes = []
        edges = []
        
        for node, node_data in self.graph.nodes(data=True):
            nodes.append({
                "id": node,
                "label": node_data.get("label", node),
                "group": node_data.get("group", "default"),
                "title": node_data.get("title", ""),
                "size": node_data.get("size", 10),
                "color": node_data.get("color", "#97C2FC")
            })
        
        for edge in self.graph.edges(data=True):
            edges.append({
                "from": edge[0],
                "to": edge[1],
                "title": edge[2].get("title", ""),
                "value": edge[2].get("value", 1),
                "color": edge[2].get("color", "#848484"),
                "dashes": edge[2].get("dashes", False)
            })
        
        return {"nodes": nodes, "edges": edges}
    
    def create_interactive_graph(self, graph_data: Dict[str, Any], company_name: str) -> str:
        """创建交互式图谱HTML"""
        net = Network(height="600px", width="100%", directed=True)
        
        # 设置图谱选项
        net.set_options("""
        {
            "physics": {
                "enabled": true,
                "stabilization": {"iterations": 100}
            },
            "interaction": {
                "hover": true,
                "tooltipDelay": 200
            },
            "layout": {
                "improvedLayout": true
            }
        }
        """)
        
        # 添加节点和边
        for node in graph_data["nodes"]:
            net.add_node(
                node["id"],
                label=node["label"],
                title=node["title"],
                group=node["group"],
                size=node["size"],
                color=node["color"]
            )
        
        for edge in graph_data["edges"]:
            net.add_edge(
                edge["from"],
                edge["to"],
                title=edge["title"],
                value=edge["value"],
                color=edge["color"],
                dashes=edge["dashes"]
            )
        
        # 生成HTML
        return net.generate_html()
