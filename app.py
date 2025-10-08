import streamlit as st
import pandas as pd
import json
import time
from knowledge_graph import KnowledgeGraphBuilder
from ai_analyzer import AIAnalyzer
from data_processor import DataProcessor
import plotly.express as px
import plotly.graph_objects as go

# 页面配置
st.set_page_config(
    page_title="企业智镜 - 智能信贷决策平台",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .risk-high { color: #d62728; }
    .risk-medium { color: #ff7f0e; }
    .risk-low { color: #2ca02c; }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

class EnterpriseMirrorApp:
    def __init__(self):
        self.data_processor = DataProcessor()
        self.graph_builder = KnowledgeGraphBuilder()
        self.ai_analyzer = AIAnalyzer()
        
    def render_sidebar(self):
        """渲染侧边栏"""
        st.sidebar.title("🔮 企业智镜")
        st.sidebar.markdown("---")
        
        # 企业搜索
        company_name = st.sidebar.text_input(
            "🏢 输入企业名称",
            value="华为技术有限公司",
            help="输入要分析的目标企业名称"
        )
        
        # 行业筛选
        industry = st.sidebar.selectbox(
            "📊 行业分类",
            ["全部", "科技", "制造", "金融", "消费", "医疗", "能源"]
        )
        
        # 分析深度
        analysis_depth = st.sidebar.slider(
            "🔍 分析深度",
            min_value=1,
            max_value=3,
            value=2,
            help="1: 基础分析, 2: 标准分析, 3: 深度分析"
        )
        
        return company_name, industry, analysis_depth
    
    def render_company_overview(self, company_data):
        """渲染企业概览信息"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("企业规模", company_data.get("scale", "大型企业"))
        with col2:
            st.metric("成立年限", f"{company_data.get('establish_years', 10)}年")
        with col3:
            st.metric("信用评级", company_data.get("credit_rating", "A"))
        with col4:
            risk_level = company_data.get("risk_level", "medium")
            risk_color = {"high": "🔴", "medium": "🟡", "low": "🟢"}
            st.metric("风险等级", f"{risk_color[risk_level]} {risk_level.upper()}")
    
    def render_knowledge_graph(self, graph_data, company_name):
        """渲染知识图谱"""
        st.subheader("🔗 产业链知识图谱")
        
        # 使用PyVis生成交互式图谱
        graph_html = self.graph_builder.create_interactive_graph(graph_data, company_name)
        
        # 在Streamlit中显示图谱
        st.components.v1.html(graph_html, height=600, scrolling=True)
        
        # 图谱统计信息
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("关联企业", len([n for n in graph_data['nodes'] if n['group'] == 'company']))
        with col2:
            st.metric("关键人物", len([n for n in graph_data['nodes'] if n['group'] == 'person']))
        with col3:
            st.metric("产业链关系", len([e for e in graph_data['edges'] if e.get('type') == 'supply_chain']))
    
    def render_ai_analysis(self, company_data, graph_data):
        """渲染AI分析报告"""
        st.subheader("🤖 AI智能分析报告")
        
        with st.spinner("AI正在深度分析企业数据..."):
            analysis_result = self.ai_analyzer.generate_credit_report(company_data, graph_data)
        
        # 展示分析结果
        if analysis_result:
            self._display_analysis_sections(analysis_result)
        else:
            st.error("AI分析失败，请稍后重试")
    
    def _display_analysis_sections(self, analysis_result):
        """展示分析报告的各个部分"""
        
        # 产业链地位分析
        with st.expander("📈 产业链地位分析", expanded=True):
            st.write(analysis_result.get("industry_chain_analysis", ""))
            
            # 可视化产业链位置
            self._create_supply_chain_chart(analysis_result)
        
        # 核心风险提示
        with st.expander("🚨 核心风险提示"):
            risks = analysis_result.get("core_risks", [])
            for i, risk in enumerate(risks, 1):
                st.error(f"{i}. {risk}")
        
        # 财务健康度
        with st.expander("💹 财务健康度评估"):
            financial_health = analysis_result.get("financial_health", {})
            self._create_financial_radar_chart(financial_health)
        
        # 信贷建议
        with st.expander("💡 智能信贷建议"):
            suggestions = analysis_result.get("credit_suggestions", [])
            for suggestion in suggestions:
                st.success(f"✅ {suggestion}")
            
            # 信贷额度估算
            credit_limit = analysis_result.get("estimated_credit_limit", "需进一步评估")
            st.info(f"**建议授信额度**: {credit_limit}")
    
    def _create_supply_chain_chart(self, analysis_result):
        """创建产业链位置图表"""
        try:
            positions = analysis_result.get("supply_chain_position", {})
            if positions:
                fig = go.Figure(go.Bar(
                    x=list(positions.values()),
                    y=list(positions.keys()),
                    orientation='h',
                    marker_color='#1f77b4'
                ))
                fig.update_layout(
                    title="产业链环节强度分析",
                    xaxis_title="强度评分",
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning("产业链数据可视化暂不可用")
    
    def _create_financial_radar_chart(self, financial_data):
        """创建财务雷达图"""
        try:
            categories = ['偿债能力', '盈利能力', '运营能力', '成长能力', '现金流']
            values = [financial_data.get(cat, 0.7) for cat in ['solvency', 'profitability', 'operation', 'growth', 'cash_flow']]
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=values + [values[0]],
                theta=categories + [categories[0]],
                fill='toself',
                name='财务健康度'
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )),
                showlegend=False,
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning("财务雷达图数据暂不可用")
    
    def run(self):
        """运行主应用"""
        st.markdown('<h1 class="main-header">🔮 企业智镜 - 智能信贷决策平台</h1>', 
                   unsafe_allow_html=True)
        
        # 渲染侧边栏并获取参数
        company_name, industry, analysis_depth = self.render_sidebar()
        
        # 分析按钮
        if st.sidebar.button("🚀 开始智能分析", type="primary"):
            with st.spinner("正在获取企业数据并构建知识图谱..."):
                # 获取企业数据
                company_data = self.data_processor.get_company_data(company_name)
                
                if company_data:
                    # 显示企业概览
                    self.render_company_overview(company_data)
                    
                    # 构建知识图谱
                    graph_data = self.graph_builder.build_knowledge_graph(company_data)
                    
                    # 创建两列布局
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        # 显示知识图谱
                        self.render_knowledge_graph(graph_data, company_name)
                    
                    with col2:
                        # 显示AI分析报告
                        self.render_ai_analysis(company_data, graph_data)
                else:
                    st.error("❌ 未能找到该企业的相关信息，请检查企业名称或尝试其他企业")
        
        # 在侧边栏显示使用说明
        st.sidebar.markdown("---")
        st.sidebar.info("""
        **使用说明：**
        1. 输入目标企业名称
        2. 选择行业分类（可选）
        3. 设置分析深度
        4. 点击"开始智能分析"
        
        **支持分析：**
        - 华为技术有限公司
        - 腾讯科技有限公司  
        - 阿里巴巴集团
        - 字节跳动有限公司
        - 小米科技有限公司
        """)

# 运行应用
if __name__ == "__main__":
    app = EnterpriseMirrorApp()
    app.run()