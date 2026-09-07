"""知己：可直接部署到 Streamlit Community Cloud 的交互演示。"""
from datetime import date, time
from html import escape
import json
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
REPORTS = json.loads((ROOT / "reports.json").read_text(encoding="utf-8"))
STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"

st.set_page_config(page_title="知己 · 八字成长指南", page_icon="🌿", layout="wide")
st.markdown(f"<style>{(ROOT / 'styles.css').read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def valid_pillar(value: str) -> bool:
    """检查单柱格式及干支阴阳配对；不验证四柱历法关系。"""
    return (len(value) == 2 and value[0] in STEMS and value[1] in BRANCHES
            and STEMS.index(value[0]) % 2 == BRANCHES.index(value[1]) % 2)


def go(view: str) -> None:
    st.session_state.view = view


def change_direction() -> None:
    st.session_state.view = "input"


def show_report(index: int) -> None:
    report = REPORTS[index]
    profile = st.session_state.get("profile", {})
    nickname = profile.get("name", "")
    title = f"{nickname}的{report['title']}" if nickname else f"你的{report['title']}"
    heading, back = st.columns([4, 1])
    with heading:
        st.subheader(title)
        st.caption("示例报告 · 内容按所选方向展示，未根据出生信息或八字测算")
    with back:
        st.button("← 修改信息", on_click=go, args=("input",), use_container_width=True)
    left, right = st.columns([1, 1.5], gap="large")
    with left:
        with st.container(border=True):
            st.caption("性格画像 · 示例")
            st.subheader(report["trait"])
            st.markdown(" · ".join(report["words"]))
            st.write(report["body"])
            st.markdown('<div class="elements">木　火　土　金　水</div>', unsafe_allow_html=True)
            st.caption("五行意象为视觉展示，不代表测算比例。")
    with right:
        for number, (tag, detail) in enumerate(zip(report["tags"], report["details"]), 1):
            st.caption(f"0{number} / {tag}")
            st.markdown(f"#### {detail[0]}")
            st.write(detail[1])
            st.divider()
    st.markdown("### 从今天的一件小事开始")
    st.caption("SMALL STEPS, REAL GROWTH")
    completed = 0
    for number, step in enumerate(report["steps"]):
        completed += st.checkbox(step, key=f"step_{index}_{number}")
    st.progress(completed / 3, text=f"今日实践 · 已完成 {completed} / 3")


def show_input(index: int) -> None:
    report = REPORTS[index]
    left, right = st.columns([1.04, 1], gap="large")
    with left:
        with st.container(border=True):
            st.caption("YOUR BEGINNING")
            st.subheader("从你的八字开始")
            mode = st.radio("输入方式", ["直接输入八字", "输入出生信息"], horizontal=True)
            # 输入方式位于表单外，切换时立即显示对应字段。
            with st.form("birth_profile"):
                name = st.text_input("如何称呼你（选填）", max_chars=20, key="nickname",
                                     placeholder="孩子的小名" if index == 0 else "输入昵称，让解读更亲切")
                values = []
                birthday = birth_time = city = None
                if mode == "直接输入八字":
                    for col, label, default in zip(st.columns(4), ["年柱", "月柱", "日柱", "时柱"],
                                                   ["甲子", "丁卯", "乙亥", "辛巳"]):
                        with col:
                            values.append(st.text_input(label, default, max_chars=2, key=label).strip())
                    st.caption("已填入体验八字，可直接修改。仅检查单柱干支格式，不验证四柱历法关系。")
                else:
                    birthday = st.date_input("出生日期 · 公历", value=date(1995, 6, 15),
                                             min_value=date(1900, 1, 1), max_value=date.today())
                    birth_time = st.time_input("出生时间（当地时间）", value=time(9, 0))
                    city = st.text_input("出生城市", placeholder="例如：中国 · 杭州")
                    st.caption("演示版尚未接入时区、真太阳时、节气及出生日期排盘。")
                st.info(f"本次探索：{report['title']}")
                submitted = st.form_submit_button("查看我的解读 →", type="primary", use_container_width=True)
            st.caption("云端部署后，输入会传至 Streamlit 服务处理；本演示不写入数据库或文件，不调用外部分析 API。")
            if submitted:
                if mode == "直接输入八字" and not all(valid_pillar(v) for v in values):
                    st.error("请填写有效的干支组合，例如甲子、丁卯。")
                elif mode == "输入出生信息" and not city.strip():
                    st.error("请填写出生城市。")
                else:
                    st.session_state.profile = {"name": name.strip(), "mode": mode,
                                                "pillars": values, "birthday": birthday,
                                                "birth_time": birth_time, "city": city}
                    for number in range(3):
                        st.session_state.pop(f"step_{index}_{number}", None)
                    go("report")
                    st.rerun()
    with right:
        word = ["天赋", "能量", "事业"][index]
        st.markdown(f'''<div class="preview"><div class="preview-label">你将看见什么 <span>解读预览 ↗</span></div>
            <div class="orbit"><span class="orbit-top">木 · 生长</span><div class="orb">{word}<small>认识 · 接纳 · 生长</small></div><span class="orbit-bottom">土 · 安定</span></div>
            <h2>{escape(report['headline'])}</h2><p>{escape(report['desc'])}</p>
            {''.join(f'<div class="preview-row"><em>0{i+1}</em><div>{escape(tag)}<small>{escape(report["details"][i][0])}</small></div></div>' for i, tag in enumerate(report['tags']))}
            <p class="preview-foot">✧ 理解自己，也拥有改变的自由</p></div>''', unsafe_allow_html=True)


st.session_state.setdefault("view", "input")
st.session_state.setdefault("direction", 1)
with st.sidebar:
    st.markdown('<div class="brand">知己<small>ZHI JI · 生长有时</small></div>', unsafe_allow_html=True)
    st.caption("我的探索")
    st.button("✧ 开始解读", use_container_width=True, on_click=go, args=("input",))
    st.button("◎ 示例报告", use_container_width=True, on_click=go, args=("report",))
    st.divider()
    st.markdown("认识自己，\n\n是一生的开始。")
    st.caption("东方智慧 · 当代成长")
    st.caption("访客体验 / 前端演示版")

st.caption("探索 / 开始解读　　　　　　　　　交互体验 DEMO")
st.markdown('<div class="intro"><small>SELF-DISCOVERY, AT YOUR OWN PACE</small><h1>知己，而后向前。</h1><p>每一种天性，都有适合自己的生长方式。</p></div>', unsafe_allow_html=True)
index = st.radio("选择成长方向", range(3), format_func=lambda i: REPORTS[i]["title"],
                 horizontal=True, key="direction", on_change=change_direction)
for i, col in enumerate(st.columns(3)):
    item = REPORTS[i]
    with col:
        st.markdown(f'<div class="direction-card {"selected" if i == index else ""}"><span>{["♧", "☼", "◎"][i]}</span><h3>{item["title"]}</h3><p>{item["sub"]}</p><small>{" · ".join(item["tags"])}</small></div>', unsafe_allow_html=True)
st.write("")
if st.session_state.view == "report":
    show_report(index)
else:
    show_input(index)
st.divider()
st.caption("知己 ZHI JI · 传统文化视角的自我探索工具。示例不用于定义孩子、预测命运或替代现实商业判断。")
