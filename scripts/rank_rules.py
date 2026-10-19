"""`/rank` 与网站“为我推荐”共用的排序规则（同一份规则，两处实现：scripts/rank.py 与 assets/rank.js）。

build_site.py 每次生成首页时把这里导出为 assets/rank-rules.json，浏览器端读那份 JSON；
改规则只改这个文件，然后跑 `python -m pytest -q tests/test_rank.py`（里面有 Python 与 JS 结果一致的测试）。

研究方向词表 GROUPS：每组是同义词（中英文），命中任一词即算命中该组；组前的学科代码用于从关键词推断学科（空表示不对应某个学科）。
词的写法：
    英文按整词匹配，不区分大小写；结尾带 * 表示前缀（neuro* 匹配 neuroscience）；
    全大写且不超过 4 个字母的缩写（AI、NLP、MRI）区分大小写；
    中文按子串匹配。
"""
from __future__ import annotations

GROUPS: list[tuple[str, str]] = [
    # 人工智能
    ("ai", "机器学习|machine learning|ML|statistical learning|统计学习"),
    ("ai", "深度学习|deep learning|neural network*|神经网络"),
    ("ai", "人工智能|artificial intelligence|AI"),
    ("ai", "计算机视觉|computer vision|图像识别|image recognition|image analysis|图像分析|图像处理|image processing"),
    ("ai", "自然语言处理|natural language processing|natural language|NLP|computational linguistic*|语言模型|language model*|LLM|LLMs|大模型|large language model*"),
    ("ai", "强化学习|reinforcement learning"),
    ("ai", "生成模型|generative model*|generative AI|diffusion model*|扩散模型|生成式"),
    ("ai", "图神经网络|graph neural network*|GNN|GNNs|graph learning"),
    ("ai", "可信人工智能|trustworthy AI|AI safety|AI 安全|explainab*|interpretab*|可解释|fairness|公平性"),
    ("ai", "多模态|multimodal|multi-modal"),
    ("ai", "联邦学习|federated learning"),
    ("ai", "语音识别|语音处理|speech recognition|speech processing|speech|audio|音频"),
    # 计算机
    ("cs", "数据科学|data science|data-driven|big data|大数据"),
    ("cs", "网络安全|信息安全|cybersecurity|cyber security|cyber|cryptograph*|密码学|privacy|隐私"),
    ("cs", "分布式系统|distributed system*|cloud computing|云计算|edge computing|边缘计算"),
    ("cs", "软件工程|software engineering|program analysis|程序分析|formal verification|形式化验证|formal method*"),
    ("cs", "人机交互|human-computer interaction|human–computer interaction|HCI|user experience|交互设计"),
    ("cs", "计算机图形学|computer graphics|graphics|rendering|渲染"),
    ("cs", "高性能计算|high-performance computing|high performance computing|HPC|parallel computing|并行计算"),
    ("cs", "数据库|database*|data management"),
    ("cs", "理论计算机|theoretical computer science|algorithm*|算法|computational complexity"),
    ("cs", "区块链|blockchain"),
    ("physics", "量子计算|quantum computing|quantum computer*|quantum algorithm*|quantum information|量子信息"),
    ("engineering", "无线通信|通信网络|wireless|communication network*|telecommunication*|6G|5G|IoT|internet of things|物联网"),
    ("bio", "生物信息|bioinformatic*|computational biology|计算生物学"),
    # 数学
    ("math", "统计学|统计|statistic*|biostatistic*|生物统计"),
    ("math", "最优化|运筹学|运筹|optimization|optimisation|operations research"),
    ("math", "应用数学|applied math*|偏微分方程|partial differential equation*|PDE|PDEs|numerical analysis|数值分析|scientific computing|科学计算"),
    ("math", "概率论|概率|probabilit*|stochastic*|随机过程"),
    ("math", "纯数学|pure math*|algebra*|代数|geometry|几何|topology|拓扑|number theory|数论"),
    # 物理
    ("physics", "量子物理|量子|quantum physics|quantum optic*|quantum material*|quantum technolog*|quantum"),
    ("physics", "凝聚态|condensed matter|超导|superconduct*"),
    ("physics", "光学|光子|激光|optic*|photonic*|laser*"),
    ("physics", "天体物理|天文|宇宙学|astrophysic*|astronom*|cosmolog*|galax*|星系"),
    ("physics", "粒子物理|高能物理|particle physics|high energy physics|high-energy physics|collider*|hadron*|neutrino*|中微子"),
    ("physics", "等离子体|核聚变|plasma*|fusion"),
    ("physics", "引力波|gravitational wave*"),
    # 化学与材料
    ("chem", "材料科学|材料|materials science|material*"),
    ("chem", "电池|储能|电化学|锂电|battery|batteries|energy storage|electrochem*|lithium"),
    ("chem", "催化|cataly*"),
    ("chem", "高分子|聚合物|polymer*"),
    ("chem", "有机化学|有机合成|organic chemistry|organic synthesis|synthetic chemistry"),
    ("chem", "计算化学|分子动力学|computational chemistry|DFT|density functional|molecular dynamics|molecular simulation*"),
    ("chem", "纳米|nano*"),
    ("chem", "二维材料|石墨烯|2D material*|graphene"),
    ("chem", "钙钛矿|太阳能电池|光伏|perovskite*|solar cell*|photovoltaic*"),
    # 生物
    ("bio", "分子生物学|molecular biology"),
    ("bio", "细胞生物学|cell biology"),
    ("bio", "基因组|遗传学|遗传|genom*|genetic*"),
    ("bio", "蛋白质|结构生物学|冷冻电镜|protein*|structural biology|cryo-EM|cryo-electron"),
    ("bio", "微生物|细菌|microb*|bacteri*"),
    ("bio", "免疫|immun*"),
    ("bio", "植物|作物|农业|plant*|crop*|agricultur*"),
    ("bio", "合成生物学|synthetic biology"),
    ("bio", "发育生物学|干细胞|developmental biology|stem cell*"),
    ("bio", "病毒|virus*|viral|virolog*"),
    ("bio", "生物化学|biochem*"),
    ("bio", "表观遗传|epigenetic*"),
    # 生态
    ("eco", "生态|生物多样性|保护生物学|ecolog*|biodiversit*|conservation"),
    ("eco", "进化|evolution*"),
    # 神经
    ("neuro", "神经科学|神经|脑科学|neuroscien*|neuro*|brain"),
    ("neuro", "认知|cogniti*"),
    # 地学与环境
    ("geo", "气候|climate"),
    ("geo", "海洋|ocean*|marine"),
    ("geo", "地质|地球科学|地球物理|geolog*|earth science*|geophysic*"),
    ("geo", "环境科学|环境|污染|environment*|pollution"),
    ("geo", "水文|水资源|hydrolog*|water resource*"),
    ("geo", "遥感|地理信息|remote sensing|GIS"),
    ("geo", "大气|气象|atmospher*|meteorolog*"),
    ("engineering", "能源|可再生能源|氢能|energy|renewable*|hydrogen"),
    # 工程
    ("engineering", "机械工程|mechanical engineering|mechanical"),
    ("engineering", "电气工程|电力系统|电力电子|electrical engineering|power system*|power electronic*"),
    ("engineering", "土木工程|结构工程|civil engineering|structural engineering|geotechnic*"),
    ("engineering", "机器人|自动驾驶|robot*|autonomous system*|autonomous driving|autonomous vehicle*"),
    ("engineering", "控制工程|控制理论|自动化|control theory|control system*|control engineering"),
    ("engineering", "航空航天|航空|航天|aerospace|aeronautic*"),
    ("engineering", "化学工程|化工|chemical engineering|process engineering"),
    ("engineering", "生物医学工程|biomedical engineering|medical device*"),
    ("engineering", "半导体|微电子|集成电路|芯片|semiconductor*|microelectronic*|integrated circuit*|VLSI|chip design"),
    ("engineering", "信号处理|signal processing"),
    ("engineering", "增材制造|制造|additive manufacturing|3D printing|manufactur*"),
    ("engineering", "流体力学|湍流|fluid dynamics|fluid mechanics|CFD|turbulen*"),
    ("engineering", "交通运输|交通|transport*|mobility"),
    # 医学
    ("med", "医学影像|医学图像|medical imag*|biomedical imaging|clinical imaging|ultrasound imaging|radiolog*|MRI|fMRI|PET imaging|CT imaging|tomograph*|ultrasound|断层成像|超声"),
    ("", "成像|显微成像|imaging|microscopy|显微镜"),
    ("med", "癌症|肿瘤|cancer*|oncolog*|tumor*|tumour*"),
    ("med", "流行病学|公共卫生|epidemiolog*|public health"),
    ("med", "药学|药物|药物发现|pharma*|drug discovery|drug*"),
    ("med", "心血管|cardio*|cardiac|heart"),
    ("med", "临床医学|临床|clinical"),
    ("med", "精神病学|心理健康|psychiatr*|mental health"),
    ("med", "衰老|老龄|ageing|aging"),
    ("med", "传染病|感染|抗生素耐药|infectious disease*|infection*|antimicrobial*|antibiotic*"),
    ("med", "营养学|营养|nutrition*"),
    ("med", "康复|rehabilit*"),
    # 社会科学
    ("social", "心理学|心理|psycholog*"),
    ("social", "教育学|教育研究|education|educational"),
    ("social", "社会学|sociolog*"),
    ("social", "政治学|国际关系|公共政策|political science|politics|political|international relations|public policy|policy"),
    ("social", "人类学|anthropolog*"),
    ("social", "传播学|新闻学|communication studies|media studies|journalism"),
    ("social", "城市规划|城市研究|human geography|urban*"),
    ("social", "法学|法律|law|legal"),
    # 人文
    ("humanities", "历史学|历史|histor*"),
    ("humanities", "哲学|philosoph*"),
    ("humanities", "语言学|linguistic*"),
    ("humanities", "文学|literature|literary"),
    ("humanities", "考古|archaeolog*"),
    ("humanities", "艺术史|音乐|art history|music*|musicolog*"),
    ("humanities", "宗教|神学|religio*|theolog*"),
    ("humanities", "数字人文|digital humanities"),
    # 经济与商科
    ("econ", "经济学|经济|econom*"),
    ("econ", "金融|financ*"),
    ("econ", "计量经济|econometric*"),
    ("business", "管理学|management|organisational|organizational"),
    ("business", "市场营销|营销|marketing"),
    ("business", "会计|accounting"),
    ("business", "创业|创新管理|entrepreneur*|innovation management"),
    ("business", "供应链|物流|supply chain*|logistic*"),
]

# 各项满分（总分 100）。研究匹配占大头：方向不对的机会，资助再好也不该排在前面。
WEIGHTS = {
    "kw": [25, 12, 8],      # 命中第 1/2/3 个关键词的分（按命中强度从高到低排）
    "kw_cap": 45,
    "title": 1.0,           # 关键词出现在岗位标题
    "body": 0.6,            # 只出现在简介 / 机构名
    "disc": 8,              # 每个相同学科（交叉方向两个学科都对上时更可信）
    "disc_cap": 15,
    "all_disc": 5,          # 不限学科的项目（只有在关键词也命中时才加）
    "funding": {"full": 15, "salary": 15, "stipend": 8, "partial": 8, "varies": 7, "tuition": 4, "unknown": 4, "": 4},
    "deadline": 10,
    "region_prefer": 8, "region_ok": 5, "region_other": 3,
    "elig": {"yes": 7, "partial": 4, "check": 2, "": 2},
    "screen_sensitive": -15,  # 公告提到安全审查，且申请者方向敏感
    "screen": -5,             # 公告提到安全审查
    "atas": -5,               # 英国 + 敏感方向 + 理工科：ATAS 可能适用
}

# 资助底线：min_coverage → 明确低于底线就排除（官网未写明的不排除，只降分；confirmed 才要求写明）
COVERAGE_OK = {
    "any": None,
    "partial": ["full", "salary", "partial", "stipend", "tuition", "varies", "unknown", ""],
    "full": ["full", "salary", "varies", "unknown", ""],
    "confirmed": ["full", "salary"],
}

# 近似汇率（折算成欧元，只用于“最低资助”比较，宁可宽松）
FX = {"EUR": 1, "GBP": 1.17, "USD": 0.92, "CHF": 1.05, "SEK": 0.087, "NOK": 0.085, "DKK": 0.134,
      "HKD": 0.118, "SGD": 0.69, "AUD": 0.6, "CAD": 0.67, "JPY": 0.0062, "NZD": 0.55}

# 限本土 / 本国学生的写法（只查岗位标题与申请须知原文）
RESTRICT = (r"(UK|Home|EU|European|US|U\.S\.|Australian|Canadian|Domestic)(/UK)? (students|applicants|nationals|citizens) only"
            r"|only (open|available|eligible) to (UK|home|EU|EEA|US|U\.S\.|domestic|Australian|Canadian)"
            r"|must (be|hold) (a |an )?(UK|US|U\.S\.|EU|Swiss|Norwegian|Australian|Canadian) (citizen|national|citizenship)"
            r"|U\.?S\. citizenship (is )?required|(citizens|nationals) (and|or) permanent residents only"
            r"|EU/EEA (citizens|nationals) only|仅限(本国|本土|英国|美国|欧盟|澳大利亚|加拿大)")

# 德语岗位：标题是德语，或写明工作语言只有德语 / 要求德语
GERMAN = (r"Doktorand|Wissenschaftliche[rs]? Mitarbeiter|Promotionsstelle|Promotion |Stellenausschreibung"
          r"|Deutschkenntnisse|fluent (in )?German|German language skills (are )?(required|essential)|工作语言：(German|Deutsch)$|工作语言：(German|Deutsch)；")

EU = ["AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IE", "IT", "LV", "LT", "LU", "MT",
      "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE"]

# 敏感方向在这些学科里时，英国岗位提示 ATAS
ATAS_DISC = ["physics", "engineering", "chem", "cs", "ai", "math"]

LEVELS = {"bachelor": 1, "master": 2, "phd": 3}
CEFR = {"A1": 1, "A2": 2, "B1": 3, "B2": 4, "C1": 5, "C2": 6, "native": 6}


def rules(disc_words: dict[str, str] | None = None) -> dict:
    """导出给浏览器的规则（JSON 可序列化）。"""
    if disc_words is None:
        from build_site import DISC_WORDS as disc_words
    return {"groups": [{"d": d, "t": t.split("|")} for d, t in GROUPS], "weights": WEIGHTS, "coverage_ok": COVERAGE_OK,
            "fx": FX, "restrict": RESTRICT, "german": GERMAN, "eu": EU, "atas_disc": ATAS_DISC, "levels": LEVELS,
            "cefr": CEFR, "disc_words": disc_words}
