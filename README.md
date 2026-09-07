# 知己 · 八字成长指南

可直接上传 GitHub、部署到 Streamlit Community Cloud 的 Python 交互演示。保留原版松绿与玉白风格，界面采用 Streamlit 原生控件重新实现，并非 React 页面的像素级复刻。

## 功能

- 三类方向：儿童天赋解说、个人能量提升、个人事业方案。
- 四柱输入及干支格式校验；出生日期、时间、城市输入流程。
- 对应方向的示例报告、昵称展示、可勾选的每日实践清单。
- 无需 API Key、数据库、Node.js 或 Sites 服务。

**这是演示版：不同八字不会生成不同测算结果。** 报告从 `reports.json` 中读取，仅按方向切换。没有接入真实排盘、大运计算、AI 分析或付费服务。单柱格式校验不等于完整四柱历法校验。

## 上传 GitHub

1. 解压代码包。
2. 在 GitHub 新建仓库，例如 `zhiji-streamlit`。
3. 使用 **Add file → Upload files**，上传解压后的所有文件和 `.streamlit` 文件夹，再提交。
4. 确保仓库首页直接能看到 `app.py`、`requirements.txt`、`reports.json`、`styles.css`。

请上传解压后的内容，不要只上传 ZIP 文件。如果操作系统隐藏了 `.streamlit` 文件夹，请显示隐藏文件，或在 GitHub 新建 `.streamlit/config.toml` 并复制配置内容。

```text
仓库根目录/
├── app.py
├── reports.json
├── styles.css
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── config.toml
```

## 连接 Streamlit 部署

1. 打开 https://share.streamlit.io/，登录并连接 GitHub 账号。
2. 点击 **Create app**，选择从 GitHub 部署。
3. Repository：选你的 `zhiji-streamlit` 仓库。
4. Branch：选择实际上传的分支，通常是 `main`。
5. Main file path：填写 **`app.py`**。
6. 在 Advanced settings 中选 Python **3.12**，无需填写 Secrets。
7. 点击 **Deploy**，等待依赖安装后获得应用链接。

若你把整个文件夹上传了，入口改为 `zhiji-streamlit/app.py`；但建议使用上述根目录结构。

官方部署说明：https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

## 本地运行

建议 Python 3.12。在此文件夹打开终端：

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS / Linux 使用：source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## 修改内容

- `reports.json`：三个方向的标题、画像、分析内容、每日实践。
- `styles.css`：配色、卡片、圆形意象及移动端样式。
- `.streamlit/config.toml`：Streamlit 全局主题。
- `app.py`：输入验证、页面切换和报告展示逻辑。

## 数据与后续开发

云端运行时，用户输入会传到 Streamlit 服务器，在当前会话中处理。本演示不写入数据库或文件，不调用外部 API；会话状态不作为永久存档，刷新或断开会话后可能丢失。平台自身的日志和保留策略由平台管理。

后续如要接入真实功能，需要单独实现历法、节气、时区及大运计算，再把结果传入分析服务。API 密钥应放到 Streamlit Secrets，切勿写入 GitHub。

示例内容只用于传统文化视角的自我探索，不用于定义孩子、预测命运或替代现实商业判断。
