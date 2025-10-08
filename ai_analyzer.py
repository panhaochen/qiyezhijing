import json
import random
from typing import Dict, Any, List

class AIAnalyzer:
    def __init__(self):
        # 在实际应用中，这里会初始化大模型API客户端
        # 目前使用模拟分析逻辑
        self.analysis_templates = self._load_analysis_templates()
    
    def _load_analysis_templates(self) -> Dict[str, Any]:
        """加载分析模板"""
        return {
            "industry_analysis": [
                "该企业在{industry}行业中处于{position}地位，具有较强的{strengths}。",
                "作为{industry}领域的{scale}企业，在技术研发和市场拓展方面表现{performance}。",
                "企业在产业链中的位置较为{position}，对上下游具有一定的{bargaining_power}。"
            ],
            "risk_analysis": [
                "主要风险包括：{risks}。建议重点关注{key_risks}。",
                "企业面临{risk_level}级别的风险，主要体现在{risk_areas}。",
                "风险控制方面，需要加强{improvement_areas}的管理。"
            ],
            "credit_suggestions": [
                "建议授予{credit_level}级别的信贷额度，额度范围在{amount_range}。",
                "考虑到企业的{positive_factors}，建议采取{credit_strategy}的信贷策略。",
                "授信条件建议：{conditions}。"
            ]
        }
    
    def generate_credit_report(self, company_data: Dict[str, Any], graph_data: Dict[str, Any]) -> Dict[str, Any]:
        """生成信用分析报告"""
        
        # 分析产业链地位
        industry_analysis = self._analyze_industry_position(company_data, graph_data)
        
        # 识别核心风险
        core_risks = self._identify_core_risks(company_data)
        
        # 评估财务健康度
        financial_health = self._assess_financial_health(company_data)
        
        # 生成信贷建议
        credit_suggestions = self._generate_credit_suggestions(company_data, industry_analysis, core_risks)
        
        return {
            "industry_chain_analysis": industry_analysis,
            "core_risks": core_risks,
            "financial_health": financial_health,
            "credit_suggestions": credit_suggestions,
            "supply_chain_position": self._analyze_supply_chain_strength(company_data),
            "estimated_credit_limit": self._estimate_credit_limit(company_data)
        }
    
    def _analyze_industry_position(self, company_data: Dict[str, Any], graph_data: Dict[str, Any]) -> str:
        """分析产业链地位"""
        company_name = company_data["name"]
        industry = company_data.get("industry", "相关")
        scale = company_data.get("scale", "")
        
        positions = ["领先", "重要", "关键", "核心"]
        strengths = ["技术优势", "市场优势", "品牌优势", "供应链优势"]
        
        analysis = f"""
        {company_name}作为{industry}行业的{scale}企业，在产业链中处于{random.choice(positions)}位置。
        企业凭借其在{random.choice(strengths)}方面的积累，建立了较为完善的产业生态。
        
        从知识图谱分析来看，企业拥有{len([n for n in graph_data['nodes'] if n['group'] == 'company'])}家关联企业，
        {len([e for e in graph_data['edges'] if 'supply' in e.get('title', '')])}条供应链关系，
        显示出较强的产业整合能力。
        """
        
        return analysis
    
    def _identify_core_risks(self, company_data: Dict[str, Any]) -> List[str]:
        """识别核心风险"""
        base_risks = [
            "宏观经济波动对行业的影响",
            "行业政策变化风险", 
            "技术迭代带来的竞争压力",
            "原材料价格波动风险",
            "市场需求变化风险"
        ]
        
        # 添加企业特定风险
        specific_risks = company_data.get("risk_factors", [])
        
        # 根据企业特征调整风险
        all_risks = base_risks + specific_risks
        
        # 返回前3-5个主要风险
        return random.sample(all_risks, min(4, len(all_risks)))
    
    def _assess_financial_health(self, company_data: Dict[str, Any]) -> Dict[str, float]:
        """评估财务健康度"""
        # 基于企业数据模拟财务指标
        scale_factor = 1.0 if company_data.get("scale") == "大型企业" else 0.7
        credit_factor = {"AAA": 1.0, "AA": 0.9, "A": 0.8, "BBB": 0.7}.get(
            company_data.get("credit_rating", "BBB"), 0.7
        )
        
        return {
            "solvency": round(0.6 + 0.3 * scale_factor * credit_factor, 2),  # 偿债能力
            "profitability": round(0.5 + 0.4 * scale_factor, 2),  # 盈利能力
            "operation": round(0.7 + 0.2 * scale_factor, 2),  # 运营能力
            "growth": round(0.6 + 0.3 * credit_factor, 2),  # 成长能力
            "cash_flow": round(0.65 + 0.25 * scale_factor, 2)  # 现金流
        }
    
    def _analyze_supply_chain_strength(self, company_data: Dict[str, Any]) -> Dict[str, float]:
        """分析供应链强度"""
        supply_chain = company_data.get("supply_chain", {})
        
        return {
            "上游整合能力": round(0.3 + 0.5 * len(supply_chain.get("upstream", [])) / 10, 2),
            "下游渠道控制": round(0.4 + 0.4 * len(supply_chain.get("downstream", [])) / 10, 2),
            "供应链稳定性": 0.75,
            "成本控制能力": 0.68,
            "技术创新依赖": 0.82
        }
    
    def _generate_credit_suggestions(self, company_data: Dict[str, Any], 
                                   industry_analysis: str, core_risks: List[str]) -> List[str]:
        """生成信贷建议"""
        suggestions = []
        
        # 基础建议
        base_suggestions = [
            "建立定期的贷后监控机制，重点关注企业经营状况变化",
            "建议与企业建立战略合作关系，获取更多经营数据",
            "关注行业政策动向，及时调整信贷策略"
        ]
        
        # 根据风险等级调整建议
        risk_level = company_data.get("risk_level", "medium")
        if risk_level == "low":
            suggestions.extend([
                "可考虑提高授信额度，支持企业扩大再生产",
                "建议提供优惠利率，巩固银企合作关系",
                "可开展供应链金融合作，拓展业务范围"
            ])
        elif risk_level == "medium":
            suggestions.extend([
                "建议采取适度的信贷额度，控制风险敞口",
                "要求提供足额抵押或担保措施",
                "加强贷前审查和贷后管理频率"
            ])
        else:
            suggestions.extend([
                "建议谨慎授信，严格控制风险敞口",
                "要求提供强担保措施，并设置严格的用款条件",
                "建立风险预警机制，定期评估企业状况"
            ])
        
        return suggestions[:3]  # 返回前3条建议
    
    def _estimate_credit_limit(self, company_data: Dict[str, Any]) -> str:
        """估算信贷额度"""
        scale = company_data.get("scale", "")
        credit_rating = company_data.get("credit_rating", "BBB")
        
        limits = {
            ("大型企业", "AAA"): "5-10亿元",
            ("大型企业", "AA"): "3-8亿元", 
            ("大型企业", "A"): "1-5亿元",
            ("中型企业", "AAA"): "1-3亿元",
            ("中型企业", "AA"): "5000万-2亿元",
            ("中型企业", "A"): "3000万-1亿元"
        }
        
        return limits.get((scale, credit_rating), "3000万-8000万元")