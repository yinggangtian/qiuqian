from openai import OpenAI
import json
import time

client = OpenAI(
    api_key="",
    base_url=""
)

# ===== 6个签级 × 6种问题维度 = 完整覆盖测试用例 =====
test_cases = [
    # ── 1. 凶签 + 事业问题（中年男性，已婚）──
    {
        "label": "测试1：事业问题 + 凶签",
        "user_info": {"nickname": "老张", "gender": "男", "age_range": "30-40", "emotion_status": "已婚"},
        "user_question": "我想辞职创业，做餐饮行业，不知道时机对不对",
        "sign": {"sign_number": 7, "sign_level": "凶", "sign_title": "谋望大败",
            "sign_poem": "谋望之事必成空，千辛万苦付东风。早知今日空费力，不如当初守困穷。",
            "sign_interpretation": "财运：求财不得，反遭损失；事业：所有计划失败，努力白费；感情：求爱被拒、婚姻不成；健康：劳累过度、积劳成疾；今日建议：放弃所有目标，安心休息。", "weight": 30}
    },
    # ── 2. 小凶签 + 感情问题（年轻女性，恋爱中）──
    {
        "label": "测试2：感情问题 + 小凶签",
        "user_info": {"nickname": "小美", "gender": "女", "age_range": "25-35", "emotion_status": "恋爱中"},
        "user_question": "我最近和男朋友总是吵架，想问感情能不能走下去",
        "sign": {"sign_number": 39, "sign_level": "小凶", "sign_title": "感情不顺",
            "sign_poem": "感情不顺多风波，误会重重无奈何。冷静沟通莫急躁，否则恐有别离多。",
            "sign_interpretation": "财运：因感情小破财；事业：因感情分心、工作失误；感情：吵架、冷战、误会；健康：因感情心情不好、失眠；今日建议：冷静沟通，互相理解。", "weight": 30}
    },
    # ── 3. 次于中平签 + 健康问题（中年女性，已婚）──
    {
        "label": "测试3：健康问题 + 次于中平签",
        "user_info": {"nickname": "慧姐", "gender": "女", "age_range": "40-50", "emotion_status": "已婚"},
        "user_question": "最近总是失眠头疼，身体检查也没大问题，想问问健康运",
        "sign": {"sign_number": 75, "sign_level": "次于中平", "sign_title": "身体微恙",
            "sign_poem": "身体微恙小不适，注意休息莫操劳。保养调理无大碍，安稳安康自逍遥。",
            "sign_interpretation": "财运：无破财；事业：小影响；感情：无影响；健康：小感冒、疲劳；今日建议：注意休息，多喝水。", "weight": 20}
    },
    # ── 4. 中平签 + 人际问题（青年男性，单身）──
    {
        "label": "测试4：人际问题 + 中平签",
        "user_info": {"nickname": "小陈", "gender": "男", "age_range": "20-30", "emotion_status": "单身"},
        "user_question": "我刚换工作，跟新同事处不太好，有点被排挤的感觉，想知道人际关系会不会好转",
        "sign": {"sign_number": 87, "sign_level": "中平", "sign_title": "和合小吉",
            "sign_poem": "家庭和合少风波，感情平稳乐呵呵。莫为小事生争执，安稳安康福自多。",
            "sign_interpretation": "财运：家庭和睦则财旺；事业：家庭和睦则业兴；感情：家庭和睦则情顺；健康：家庭和睦则身健；今日建议：家庭和睦，不争吵。", "weight": 12}
    },
    # ── 5. 优于中平签 + 财运问题（中年男性，已婚）──
    {
        "label": "测试5：财运问题 + 优于中平签",
        "user_info": {"nickname": "大明", "gender": "男", "age_range": "30-40", "emotion_status": "已婚"},
        "user_question": "朋友拉我一起做外贸生意，投了二十万，想看看这笔投资能不能赚到钱",
        "sign": {"sign_number": 95, "sign_level": "优于中平", "sign_title": "贵人助力",
            "sign_poem": "贵人暗里助君行，谋望求财不用惊。谨慎前行无大险，平安顺利得功成。",
            "sign_interpretation": "财运：有贵人相助，得财顺利；事业：有贵人相助，做事顺利；感情：有贵人相助，感情顺利；健康：有贵人相助，康复顺利；今日建议：抓住贵人，好好把握。", "weight": 6}
    },
    # ── 6. 大吉签 + 事业问题（青年女性，单身）──
    {
        "label": "测试6：事业问题 + 大吉签",
        "user_info": {"nickname": "阿琳", "gender": "女", "age_range": "20-30", "emotion_status": "单身"},
        "user_question": "我刚拿到一个大公司的offer，想问这份工作发展前景怎么样",
        "sign": {"sign_number": 99, "sign_level": "大吉", "sign_title": "春风得意",
            "sign_poem": "春来无处不飞花，万里青云路不赊。此去前程多顺遂，家门吉庆福无涯。",
            "sign_interpretation": "财运：财运亨通，财源广进；事业：事业顺遂，步步高升；感情：感情美满，幸福甜蜜；健康：身体健康，平安无恙；今日建议：大胆前行，心想事成。", "weight": 2}
    },
]

prompt_template = """你是一位精通吕祖灵签的专业解签师。吕祖灵签源自道教吕洞宾祖师信仰，传统用于指引迷津、趋吉避凶。你深谙传统解签之道，同时兼具温暖、智慧、接地气的话术风格，将古老签文智慧转化为现代人能懂、能用的指引。

【用户信息】
昵称：{nickname}
性别：{gender}
年龄段：{age_range}
感情状态：{emotion_status}

【用户问题】
{user_question}

【抽签结果】
签号：第{sign_number}签
签级：{sign_level}
签题：{sign_title}
签文：{sign_poem}
解文：{sign_interpretation}

【解签专业知识框架】

一、传统解签三步法："以象取义→因人解签→因事断吉凶"
- 以象取义：签文诗偈中的意象是解签的根基。风、雨、浪主变动与考验；花、月、春主希望与转机；山、门、路主事业与前景；舟、桥、渡主过渡与抉择。不可脱离签文意象凭空解读，必须从签文中提取象征，再映射到用户所问之事。
- 因人解签：同一签对不同人解读截然不同。年龄影响人生阶段判断（青年问事业重起步，中年问财运重守成，晚年问健康重养生）；性别影响话术方式；感情状态影响感情维度的侧重（单身求遇、恋爱求稳、已婚求和）。必须结合用户信息差异化解读。
- 因事断吉凶：同一签对不同事吉凶不同。问财与问感情结果可能截然相反。必须聚焦用户所问之事，不可泛泛而谈、面面俱到。

二、签文意象五维度象征体系（解签时按用户问题聚焦主维度，兼顾1-2个辅维度）：
- 财运维度：金、宝、富、谷主财聚；水、风、散、空主财散；秤、尺主公平交易
- 事业维度：路、山、门、桥、梯主事业前景；障、断、迷、壁主事业受阻；日、光主贵人相助
- 感情维度：花、月、鸟、双、莲主感情和合；风、雨、离、孤、镜主感情波折；雁、归主重逢复合
- 健康维度：松、鹤、春、日、泉主身体安康；秋、寒、病、枯、暮主健康需防；药、医主需就医调理
- 人际维度：舟、伴、和、聚、筵主人际和谐；争、独、散、离、咬主人际冲突；信、书主远方消息

三、签级解读核心原则：
- 凶签：传统讲究"凶中藏机，否极泰来"。着重指出风险所在，同时必须点明转机方向——"知凶则避，避凶趋吉"。凶签的真正价值在于预警，提前规避即是最大的吉。
- 小凶签：凶象较轻，多因自身行为或心态不当所致。侧重提醒与防范，强调"改变方式即可化解"，给用户具体的调整方向。
- 次于中平签：偏下但不至凶，提示当前运势偏低需耐心等待。忌冒进，宜蓄力，"退一步海阔天空"。
- 中平签：平平无奇但稳当，守成为主。不宜大动，但也不必忧虑，"稳中求进"。
- 优于中平签：偏上但未至大吉，可适度进取。但不可贪心冒进，"见好就收"方能长久。
- 大吉签：运势鼎盛。但传统智慧讲究"盛极当思退，物极必反"。吉中藏慎，提醒用户珍惜当下、不盲目扩张，方为真吉。

四、话术转化借鉴心理学框架：
- 焦点解决短期治疗（SFBT）：不深挖问题原因，聚焦"接下来可以做什么"。用"例外提问"思维——凶签中也找用户可利用的积极因素，如"你意识到问题本身就是一个转机"。
- 积极心理学：在解读中嵌入"心理韧性（resilience）"概念——凶签不是终局，而是考验；给用户"我能应对"的效能感，而非无力感。
- 叙事疗法"外化"技术：把困境与用户本人分开，如"签文说的困境，不是你的错，而是当前局势"——减轻用户自责和焦虑。
- 动机访谈"自主性"原则：建议以"你可以试试……"而非"你必须……"的句式，留给用户行动的自主感和选择权。

五、传统解签禁忌：
- 不可断言"一定会如何"——签文指引的是趋势与方向，不是确定性的预言
- 不可替代专业判断——健康问题必须建议就医，法律问题必须建议咨询专业人士
- 不可制造恐惧——凶签的目的是预警规避，不是恐吓
- 不可过度安慰——吉签也不可承诺"包成功"，保持"吉中藏慎"

【输出要求】
请严格按以下三段结构输出，每段50-100字，使用JSON格式：

1. question_breakdown：用"以象取义"法拆解用户问题——先识别用户关心的核心维度（财运/事业/感情/健康/人际），再点明1-2个辅维度，最后明确用户真正想知道什么（是求方向、求确认、还是求安慰）
2. sign_translation：用"因人解签+因事断吉凶"法，从签文意象中提取与用户问题相关的象征，翻译为与用户个人信息和处境直接相关的白话解读。同一签对不同人不同事解读不同，不可泛泛照搬解文
3. user_friendly_advice：融合SFBT+积极心理学+叙事疗法的话术转化——聚焦"接下来可以做什么"，用"例外提问"找积极因素，用"外化"减轻自责，给具体可操作的小步骤而非笼统大道理，以"你可以试试"而非"你必须"的句式结尾，留给用户自主感

【注意事项】
- 签级仅使用：凶、小凶、次于中平、中平、优于中平、大吉，不可使用其他签级名称
- 解签仅供参考娱乐，不构成任何专业建议
- 凶签遵循"凶中藏机"原则：先点明风险，再必须指出转机方向和具体规避方法，不可只恐吓不给路
- 小凶/次于中平签侧重"行为可改"：强调凶象轻、因自身行为所致，改变方式即可化解
- 中平/优于中平签侧重"守成稳进"：提醒忌冒进忌贪心，稳中求进
- 大吉签遵循"吉中藏慎"原则：提醒盛极当思退、物极必反，不可盲目画饼承诺
- 健康问题必须建议就医，不可用解签替代医疗建议
- 每段严格控制在50-100字之间
- 必须返回合法JSON，不要包含多余文本

请直接返回JSON："""

# ===== 运行测试 =====
results_summary = []

for i, tc in enumerate(test_cases):
    print(f"\n{'='*70}")
    print(f"📋 {tc['label']}")
    print(f"{'='*70}")
    
    ui = tc["user_info"]
    sg = tc["sign"]
    
    prompt = prompt_template.format(
        nickname=ui["nickname"], gender=ui["gender"],
        age_range=ui["age_range"], emotion_status=ui["emotion_status"],
        user_question=tc["user_question"],
        sign_number=sg["sign_number"], sign_level=sg["sign_level"],
        sign_title=sg["sign_title"], sign_poem=sg["sign_poem"],
        sign_interpretation=sg["sign_interpretation"]
    )
    
    print(f"\n📤 输入：")
    print(f"  用户：{ui['nickname']}，{ui['gender']}，{ui['age_range']}岁，{ui['emotion_status']}")
    print(f"  问题：{tc['user_question']}")
    print(f"  抽签：第{sg['sign_number']}签 [{sg['sign_level']}] {sg['sign_title']}")
    print(f"  签文：{sg['sign_poem']}")
    
    t0 = time.time()
    try:
        response = client.responses.create(
            model="glm-5.1",
            input=prompt
        )
        elapsed = time.time() - t0
        
        raw_output = response.output_text
        print(f"\n📥 模型输出（耗时{elapsed:.1f}s）：")
        print(raw_output)
        
        # 解析JSON
        try:
            json_str = raw_output.strip()
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0].strip()
            elif "```" in json_str:
                json_str = json_str.split("```")[1].split("```")[0].strip()
            
            parsed = json.loads(json_str)
            print(f"\n✅ 解析结果：")
            char_ok = True
            for key, val in parsed.items():
                cn_name = {"question_breakdown":"问题拆解","sign_translation":"签文翻译","user_friendly_advice":"转化话术"}.get(key, key)
                char_count = len(val)
                if char_count < 50:
                    status = f"⚠️ 不足50字（{char_count}字）"
                    char_ok = False
                elif char_count > 100:
                    status = f"⚠️ 超过100字（{char_count}字）"
                    char_ok = False
                else:
                    status = f"✅ {char_count}字"
                print(f"  【{cn_name}】{status}")
                print(f"    {val}")
            
            results_summary.append({
                "label": tc["label"],
                "sign_level": sg["sign_level"],
                "char_ok": char_ok,
                "json_ok": True,
                "elapsed": elapsed
            })
        except Exception as e:
            print(f"\n⚠️ JSON解析失败：{e}")
            results_summary.append({
                "label": tc["label"],
                "sign_level": sg["sign_level"],
                "char_ok": False,
                "json_ok": False,
                "elapsed": elapsed
            })
            
    except Exception as e:
        print(f"\n❌ API调用失败：{type(e).__name__}: {e}")
        results_summary.append({
            "label": tc["label"],
            "sign_level": sg["sign_level"],
            "char_ok": False,
            "json_ok": False,
            "elapsed": 0
        })
    
    if i < len(test_cases) - 1:
        time.sleep(1)

# ===== 汇总报告 =====
print(f"\n{'='*70}")
print("🏁 测试汇总报告")
print(f"{'='*70}")
print(f"\n{'用例':<28} {'签级':<8} {'字数':<8} {'JSON':<8} {'耗时':<8}")
print("-" * 60)
for r in results_summary:
    char_mark = "✅" if r["char_ok"] else "⚠️"
    json_mark = "✅" if r["json_ok"] else "❌"
    print(f"{r['label']:<28} {r['sign_level']:<8} {char_mark:<8} {json_mark:<8} {r['elapsed']:.1f}s")

total = len(results_summary)
char_pass = sum(1 for r in results_summary if r["char_ok"])
json_pass = sum(1 for r in results_summary if r["json_ok"])
print(f"\n字数合规：{char_pass}/{total}  JSON解析：{json_pass}/{total}")
