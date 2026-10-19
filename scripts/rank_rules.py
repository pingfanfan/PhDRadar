"""`/rank` 与网站“为我推荐”共用的排序规则（同一份规则，两处实现：scripts/rank.py 与 assets/rank.js）。

build_site.py 每次生成首页时把这里导出为 assets/rank-rules.json，浏览器端读那份 JSON；
改规则只改这个文件，然后跑 `python -m pytest -q tests/test_rank.py`（里面有 Python 与 JS 结果一致的测试）。

研究方向词表 GROUPS：每组是同义词（中英文），命中任一词即算命中该组；组前的学科代码用于从关键词推断学科（可写多个，逗号分隔；空表示不对应某个学科）。
岗位的学科不能和画像的学科冲突，关键词命中才算数；弱命中（只命中一部分、只在简介里、只命中更窄的词）要求学科明确对得上
（避免“immune memory”被推给做认知神经科学的人）。
每组写成“同义词 > 更窄的相关词”：关键词只按同义词归到组；匹配岗位时同义词和更窄的词都算（“医学影像”能匹配 MRI，“MRI”不会扩到超声）。
一个关键词归到多个组时（“量子光学”= 量子 + 光学），要各组都命中才算完全命中，只命中一部分记一半分；
关键词里有词表没覆盖的部分时（“robot learning”里的 learning），完全命中要求原词出现。
词的写法：
    英文按整词匹配，不区分大小写；结尾带 * 表示前缀（neuro* 匹配 neuroscience）；
    全大写且不超过 4 个字母的缩写（AI、NLP、MRI）区分大小写；
    中文按子串匹配；
    前面带 = 的词只用来把关键词归到组，不拿去匹配岗位（“控制”“环境”这类短词在简介里太常见）。
"""
from __future__ import annotations

GROUPS: list[tuple[str, str]] = [
    # 人工智能
    ("ai", "机器学习|machine learning|ML|statistical learning|统计学习"),
    ("ai", "深度学习|deep learning|neural network*|神经网络"),
    ("ai", "人工智能|artificial intelligence|AI"),
    ("ai", "计算机视觉|computer vision > 图像识别|image recognition|image analysis|图像分析|图像处理|image processing|object detection|目标检测"),
    ("ai", "图像分割|image segmentation|semantic segmentation|语义分割 > segmentation"),
    ("ai", "自然语言处理|natural language processing|NLP|computational linguistic* > natural language|language model*|LLM|LLMs|大模型|large language model*|语言模型|text mining|文本挖掘|machine translation|机器翻译"),
    ("ai", "大模型|大语言模型|large language model*|LLM|LLMs|foundation model*|基础模型"),
    ("ai", "强化学习|reinforcement learning"),
    ("ai,engineering", "机器人学习|具身智能|robot learning|embodied AI|embodied intelligence > robot manipulation|robotic manipulation|robotics|robotic|humanoid*|机器人"),
    ("ai", "生成模型|generative model*|generative AI|diffusion model*|扩散模型|生成式"),
    ("ai", "图神经网络|graph neural network*|GNN|GNNs|graph learning"),
    ("ai", "可信人工智能|trustworthy AI|AI safety|AI 安全|可解释|explainab*|interpretab* > fairness|公平性"),
    ("ai", "多模态|multimodal|multi-modal"),
    ("ai", "联邦学习|federated learning"),
    ("ai", "语音识别|语音处理|speech recognition|speech processing|speech technolog* > speech|spoken language"),
    # 计算机
    ("cs", "数据科学|data science|big data|大数据 > data-driven"),
    ("cs", "网络安全|信息安全|cybersecurity|cyber security|cyber-security > cyber|cryptograph*|密码学|privacy|隐私"),
    ("cs", "分布式系统|distributed system*|cloud computing|云计算|edge computing|边缘计算"),
    ("cs", "软件工程|software engineering > program analysis|程序分析|formal verification|形式化验证|formal method*"),
    ("cs", "人机交互|human-computer interaction|human–computer interaction|HCI > user experience|交互设计"),
    ("cs", "计算机图形学|computer graphics > graphics|rendering|渲染"),
    ("cs", "高性能计算|high-performance computing|high performance computing|HPC|parallel computing|并行计算"),
    ("cs", "数据库|database*|data management"),
    ("cs", "理论计算机|theoretical computer science|algorithm*|算法|computational complexity"),
    ("cs", "区块链|blockchain"),
    ("physics,cs", "量子计算|quantum computing|quantum computer*|quantum algorithm*|quantum information|量子信息 > qubit*|量子比特"),
    ("engineering", "无线通信|通信网络|wireless|communication network*|telecommunication*|6G|5G|IoT|internet of things|物联网"),
    ("bio,cs", "生物信息|bioinformatic*|computational biology|计算生物学"),
    # 数学
    ("math", "统计学|统计|statistics|statistician*|biostatistic*|生物统计 > statistical inference|statistical modelling|statistical modeling|statistical methods|statistical analysis|statistical genetics|spatial statistics"),
    ("math", "最优化|运筹学|运筹|optimization|optimisation|operations research"),
    ("math", "应用数学|applied math*|偏微分方程|partial differential equation*|PDE|PDEs|numerical analysis|数值分析|scientific computing|科学计算"),
    ("math", "概率论|概率|probabilit*|stochastic*|随机过程"),
    ("math", "纯数学|pure math* > algebra*|代数|geometry|几何|topology|拓扑|number theory|数论"),
    # 物理
    ("physics", "量子物理|量子|quantum physics|quantum > quantum optic*|quantum material*|quantum technolog*"),
    ("physics", "量子光学|quantum optic*|quantum photonic*"),
    ("physics", "凝聚态|condensed matter|超导|superconduct*"),
    ("physics", "光学|optic* > optical"),
    ("physics", "光子|光子学|photonic*|photon*|激光|laser*"),
    ("physics", "天体物理|天文|宇宙学|astrophysic*|astronom*|cosmolog* > galax*|星系|dark matter|暗物质|exoplanet*"),
    ("physics", "粒子物理|高能物理|particle physics|high energy physics|high-energy physics > collider*|hadron*|neutrino*|中微子"),
    ("physics", "等离子体|核聚变|plasma*|fusion"),
    ("physics", "引力波|gravitational wave*"),
    # 化学与材料
    ("chem", "材料科学|=材料|materials science|material*"),
    ("chem,engineering", "电池|储能|锂电|battery|batteries|energy storage|lithium-ion|lithium battery|sodium-ion > electrode*|cathode*|anode*|electrolyte*"),
    ("chem", "电化学|electrochem* > electrocataly*|electrolys*|fuel cell*|燃料电池"),
    ("chem", "催化|cataly*"),
    ("chem", "高分子|聚合物|polymer|polymers|polymeric|polymerisation|polymerization|macromolecul*"),
    ("chem", "有机化学|有机合成|organic chemistry|organic synthesis|synthetic chemistry"),
    ("chem", "计算化学|分子动力学|computational chemistry|DFT|density functional|molecular dynamics|molecular simulation*"),
    ("chem", "纳米|nano*"),
    ("chem", "二维材料|石墨烯|2D material*|graphene"),
    ("chem", "钙钛矿|太阳能电池|光伏|perovskite*|solar cell*|photovoltaic*"),
    # 生物
    ("bio", "分子生物学|molecular biology"),
    ("bio", "细胞生物学|cell biology"),
    ("bio", "基因组|基因组学|genom* > sequencing|测序"),
    ("bio", "遗传学|遗传|genetic*"),
    ("bio", "蛋白质|结构生物学|冷冻电镜|protein*|structural biology|cryo-EM|cryo-electron"),
    ("bio", "微生物|细菌|microb*|bacteri*"),
    ("bio", "免疫|免疫学|immun*"),
    ("bio", "植物|植物学|plant|plants|plant science*|plant biolog*"),
    ("bio", "作物|农业|crop|crops|agricultur*|agronom*"),
    ("bio", "合成生物学|synthetic biology"),
    ("bio", "发育生物学|干细胞|developmental biology|stem cell*"),
    ("bio", "病毒|病毒学|virus*|viral|virolog*"),
    ("bio", "生物化学|biochem*"),
    ("bio", "表观遗传|epigenetic*"),
    # 生态
    ("eco,bio", "生态|生态学|ecolog* > ecosystem*|生态系统"),
    ("eco,bio", "生物多样性|biodiversit* > species richness|conservation|保护生物学"),
    ("eco", "进化|evolution*"),
    # 神经
    ("neuro", "神经科学|脑科学|neuroscien*|neurobiolog* > neuro*|brain|neuron*|神经元|神经系统"),
    ("neuro,social", "认知神经科学|cognitive neuroscience > neuroimaging|fMRI|EEG|MEG|cognition|decision-making|decision making"),
    ("neuro", "认知科学|认知|cogniti*"),
    ("neuro,med", "fMRI|functional MRI|功能磁共振|neuroimaging|脑成像|脑影像"),
    # 地学与环境
    ("geo", "气候|气候变化|climate|climate change|global warming|全球变暖"),
    ("geo", "海洋|海洋学|ocean*|oceanograph*|物理海洋|physical oceanograph*"),
    ("eco,bio", "海洋生物|海洋生态|marine biolog*|marine ecolog*|marine > coral*|珊瑚|fisheries|渔业"),
    ("geo", "地质|地球科学|地球物理|geolog*|earth science*|geophysic*"),
    ("geo", "环境科学|=环境|污染|environment*|pollution"),
    ("geo", "水文|水资源|hydrolog*|water resource* > catchment*|river*|groundwater|地下水"),
    ("geo", "洪水|flood*|洪涝"),
    ("geo", "遥感|地理信息|remote sensing|GIS|earth observation|satellite"),
    ("geo", "大气|气象|atmospher*|meteorolog*"),
    ("engineering", "能源|可再生能源|氢能|energy|renewable*|hydrogen"),
    # 工程
    ("engineering", "机械工程|mechanical engineering|mechanical"),
    ("engineering", "电气工程|电力系统|电力电子|electrical engineering|power system*|power electronic*"),
    ("engineering", "土木工程|civil engineering|structural engineering|geotechnic* > bridge*|桥梁"),
    ("engineering", "混凝土|concrete|cement*"),
    ("engineering,ai", "机器人|robot*|robotics > autonomous system*|自主系统"),
    ("engineering,ai", "自动驾驶|无人驾驶|autonomous driving|autonomous vehicle*|self-driving > automated driving|connected vehicle*"),
    ("engineering", "控制工程|控制理论|=控制|control theory|control system*|control engineering|=自动化 > model predictive control|optimal control"),
    ("engineering", "航空航天|航空|航天|aerospace|aeronautic*"),
    ("engineering", "化学工程|化工|chemical engineering|process engineering"),
    ("engineering", "生物医学工程|biomedical engineering|medical device*"),
    ("engineering,physics", "半导体|semiconductor* > transistor*|晶体管|wafer*"),
    ("engineering", "集成电路|芯片设计|integrated circuit*|IC design|chip design|VLSI > CMOS|analog circuit*|mixed-signal|RF circuit*|circuit design"),
    ("engineering", "微电子|microelectronic*|nanoelectronic*"),
    ("engineering", "信号处理|signal processing"),
    ("engineering", "增材制造|=制造|additive manufacturing|3D printing|manufactur*"),
    ("engineering", "流体力学|湍流|fluid dynamics|fluid mechanics|CFD|turbulen*"),
    ("engineering", "交通运输|交通|transportation|transport planning|transport systems|transport policy|public transport|traffic|freight|urban mobility|mobility"),
    # 医学
    ("med,engineering", "医学影像|医学图像|medical imag*|biomedical imaging|clinical imaging|radiolog* > MRI|magnetic resonance imaging|CT imaging|computed tomography|PET imaging|ultrasound imaging|超声成像|磁共振成像|tomograph*"),
    ("med", "MRI|磁共振成像|magnetic resonance imaging"),
    ("med,engineering", "超声|ultrasound|ultrasonic*"),
    ("", "成像|imaging > microscopy|显微"),
    ("med", "癌症|肿瘤|cancer*|oncolog*|tumor*|tumour*"),
    ("med", "免疫治疗|免疫疗法|immunotherap* > CAR-T|checkpoint inhibitor*|cancer immunology|tumour immunology|tumor immunology"),
    ("med", "流行病学|epidemiolog* > public health|公共卫生|epidemic*|outbreak*"),
    ("med", "公共卫生|public health|global health|全球健康|population health"),
    ("med,bio", "传染病|infectious disease*|communicable disease* > epidemic*|pandemic*|zoonotic|zoonos*|outbreak*|transmission dynamics"),
    ("med,bio", "抗生素耐药|抗菌素耐药|antimicrobial resistance|antibiotic resistance|AMR > antimicrobial*|antibiotic*"),
    ("med", "药学|药物|药物发现|pharma*|drug discovery|drug*"),
    ("med,chem", "药物递送|纳米药物|drug delivery|nanomedicine|nanocarrier*|靶向递送|targeted delivery"),
    ("med", "心血管|cardio*|cardiac|heart"),
    ("med", "临床医学|临床|clinical"),
    ("med", "精神病学|心理健康|psychiatr*|mental health"),
    ("med", "衰老|老龄|ageing|aging"),
    ("med", "营养学|营养|nutrition*"),
    ("med", "康复|rehabilit*"),
    # 社会科学
    ("social,neuro", "心理学|心理|psycholog*"),
    ("social", "教育学|教育研究|education|educational > teacher*|pedagog*|curricul*|教师"),
    ("social", "学习科学|learning sciences|learning science"),
    ("social", "教育技术|educational technology|EdTech|technology-enhanced learning|learning analytics|学习分析 > e-learning|online learning|digital learning"),
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
    ("humanities", "二语习得|语言习得|second language acquisition|language acquisition|second language > language learning|bilingual*|multilingual*|双语"),
    ("humanities", "心理语言学|psycholinguistic*"),
    ("humanities", "文学|literature|literary"),
    ("humanities", "考古|archaeolog*"),
    ("humanities", "艺术史|音乐|art history|music*|musicolog*"),
    ("humanities", "宗教|神学|religio*|theolog*"),
    ("humanities", "数字人文|digital humanities"),
    # 经济与商科
    ("econ", "经济学|=经济|economics|economic|economist* > econometric*"),
    ("econ", "计量经济|econometric*"),
    ("econ", "劳动经济学|labour economics|labor economics > labour market*|labor market*|劳动力市场|employment|wage*"),
    ("econ", "金融|financ*"),
    ("econ", "农业经济|agricultural economics|agri-food economics|food economics > agricultural policy|economics|economic"),
    ("business", "管理学|management|organisational|organizational"),
    ("business", "运营管理|operations management|production management"),
    ("business", "市场营销|营销|marketing"),
    ("business", "会计|accounting"),
    ("business", "创业|创新管理|entrepreneur*|innovation management"),
    ("business", "供应链|物流|supply chain*|logistics"),
]

# 方法类的组：这些词常用在别的学科（“Machine Learning for Dark Matter”），岗位学科超出你的方向时只算一半
METHODS = ["机器学习", "深度学习", "人工智能", "数据科学", "统计学", "最优化"]
SIBLINGS = {"ai": ["cs"], "cs": ["ai"]}  # 判断“别的学科”时视为同一方向

# 关键词里不算概念的词（判断一个关键词是否被词表完整覆盖时忽略）
STOP = (r"[\s\-–,/&()（）、]+|(?<![A-Za-z])(and|of|for|in|the|with|on|to|based|using|applied|methods?|approach(es)?|learning)(?![A-Za-z])"
        r"|研究|科学|技术|方向|方法|应用|领域|的|与|和|及|学")


# 各项满分（总分 100）：研究匹配 70、资助 10、截止 8、地区 7、资格 5。研究匹配占大头：方向不对的机会，资助再好也不该排在前面。
WEIGHTS = {
    "kw": [28, 14, 9],      # 命中第 1/2/3 个关键词的分（按命中强度从高到低排）
    "kw_cap": 50,
    "partial": 0.5,         # 只命中关键词的一部分概念（这种弱命中和只在简介里出现的命中，要求学科也对得上才算）
    "spec": [1.3, 0.25, 0.6, 1.2],  # 关键词区分度：× (1.3 − 0.25 × log10(命中条数))，限制在 0.6–1.2
    "title": 1.0,           # 关键词出现在岗位标题
    "body": 0.6,            # 只出现在简介
    "disc": 20,             # 学科匹配：岗位学科里属于你方向的比例 × 20（“ML for dark matter”只算一半）
    "applied": 0.5,         # 方法类关键词命中、但岗位主要属于别的学科时的折扣
    "all_disc": 5,          # 不限学科的项目（只有在关键词也命中时才加）
    "funding": {"full": 10, "salary": 10, "stipend": 6, "partial": 6, "varies": 5, "tuition": 3, "unknown": 3, "": 3},
    # 截止：还有 21–75 天最合适；滚动 / 即将开放 / 未写明 / 太近 / 很远依次给分
    "deadline": {"best": 8, "far": 6, "very_far": 4, "close": 5, "rolling": 6, "upcoming": 5, "unknown": 2},
    "region_prefer": 7, "region_ok": 4, "region_other": 2,
    "elig": {"yes": 5, "partial": 3, "check": 1, "": 1},
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

# 北欧 / 荷兰语公告（只看标题）：用当地语言发布的岗位多半要求当地语言；画像 languages.other 里写了这些语言才保留
LOCAL_LANG = (r"(?<![A-Za-z])((Doktorgrads)?stipendiat|Postdoktor(?!and)|Doktorand (i|inom) |Doktorandtjänst"
              r"|ph\.d\.-stipendiat|ph\.d\.-studerende|Promovend|Promotieplaats)")

# 匹配前先去掉的机构 / 资助方名称：它们不代表岗位方向（“Economic and Social Research Council”不等于经济学）
NOISE = (r"Economic and Social (Science )?Research Council|Engineering and Physical Sciences Research Council"
         r"|Natural Environment Research Council|Biotechnology and Biological Sciences Research Council|Medical Research Council"
         r"|Arts and Humanities Research Council|Science and Technology Facilities Council|(National )?Institute of Education")
NOISE_BODY = r"(国立)?教育学院|研究理事会"  # 只在简介里去掉：信源名称里的“教育学院”就是教育学方向

# “PhD student in <系名>, focus on <方向>”：只用 focus on 后面的方向匹配（系名不代表岗位方向）
FOCUS = r"[,;:–-]\s*(with (a )?)?focus(ed)? on\s+"

EU = ["AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IE", "IT", "LV", "LT", "LU", "MT",
      "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE"]

# 敏感方向在这些学科里时，英国岗位提示 ATAS
ATAS_DISC = ["physics", "engineering", "chem", "cs", "ai", "math"]

LEVELS = {"bachelor": 1, "master": 2, "phd": 3}
LOCAL_LANGS = ["norwegian", "swedish", "danish", "dutch", "挪威语", "瑞典语", "丹麦语", "荷兰语", "no", "sv", "da", "nl"]
CEFR = {"A1": 1, "A2": 2, "B1": 3, "B2": 4, "C1": 5, "C2": 6, "native": 6}


def rules(disc_words: dict[str, str] | None = None) -> dict:
    """导出给浏览器的规则（JSON 可序列化）。"""
    if disc_words is None:
        from build_site import DISC_WORDS as disc_words
    groups = []
    for d, t in GROUPS:
        syn, _, narrow = t.partition(" > ")
        g = {"d": [x for x in d.split(",") if x], "t": syn.split("|"), "n": narrow.split("|") if narrow else []}
        if g["t"][0] in METHODS:
            g["m"] = 1
        groups.append(g)
    return {"groups": groups, "stop": STOP, "weights": WEIGHTS, "coverage_ok": COVERAGE_OK,
            "fx": FX, "restrict": RESTRICT, "german": GERMAN, "local_lang": LOCAL_LANG, "noise": NOISE, "siblings": SIBLINGS, "noise_body": NOISE_BODY, "focus": FOCUS, "eu": EU, "atas_disc": ATAS_DISC, "levels": LEVELS,
            "cefr": CEFR, "local_langs": LOCAL_LANGS, "disc_words": disc_words}
