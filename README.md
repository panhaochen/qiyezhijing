# 企业智镜 - 智能信贷决策平台

## 项目简介

本项目为企业智能分析与信贷决策平台，集成了企业数据处理、知识图谱构建、AI智能分析与可视化展示等功能。用户可通过 Streamlit 网页界面输入企业名称，快速获得企业产业链地位、核心风险、财务健康度及信贷建议等智能报告。

## 项目结构

```
ai_analyzer.py         # AI智能分析模块，生成信用分析报告
app.py                # Streamlit主应用入口，负责页面渲染与交互
data_processor.py      # 企业数据处理与模拟数据管理
knowledge_graph.py     # 企业知识图谱构建与可视化
utils.py              # 工具函数（日志、结果保存等）
```

## 依赖安装

请确保已安装以下 Python 包：

- streamlit
- pandas
- plotly
- networkx
- pyvis

安装命令如下：

```sh
pip install streamlit pandas plotly networkx pyvis
```

## 快速启动

在项目根目录下运行：

```sh
streamlit run app.py
```

即可启动企业智镜平台，进入网页界面。

## 主要模块说明

- [`data_processor.DataProcessor`](data_processor.py)：企业数据获取与模拟，支持主流企业及通用模板。
- [`knowledge_graph.KnowledgeGraphBuilder`](knowledge_graph.py)：构建企业知识图谱，支持股东、高管、子公司、供应链等关系可视化。
- [`ai_analyzer.AIAnalyzer`](ai_analyzer.py)：基于企业数据与知识图谱，生成产业链分析、风险提示、财务评估与信贷建议。
- [`utils`](utils.py)：日志配置、分析结果保存等工具函数。
- [`app.EnterpriseMirrorApp`](app.py)：Streamlit应用主类，负责页面布局、交互逻辑与各模块调用。

## 使用方法

1. 启动应用后，在侧边栏输入企业名称（如“华为技术有限公司”）。
2. 可选择行业分类与分析深度。
3. 点击“开始智能分析”按钮，等待分析结果展示。
4. 页面将展示企业概览、知识图谱、AI分析报告及信贷建议等内容。

## 支持企业示例

- 华为技术有限公司
- 腾讯科技有限公司
- 阿里巴巴集团
- 字节跳动有限公司
- 小米科技有限公司

## 结果保存与日志

分析结果可通过 [`utils.save_analysis_result`](utils.py) 保存为 JSON 文件，日志自动记录于 `enterprise_mirror.log`。

## 配置文件

如需自定义 API 密钥或参数，可在根目录添加 `config.json`，并通过 [`utils.load_config`](utils.py) 加载。

## 备注

- 本项目部分数据为模拟，实际应用可对接第三方企业信息 API。
- 如需扩展企业类型或分析维度，可在 [`data_processor.py`](data_processor.py) 和 [`ai_analyzer.py`](ai_analyzer.py) 中补充相关逻辑。

