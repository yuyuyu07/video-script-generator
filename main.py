import streamlit as st             # 导入streamlit库并给它一个简短的别名st。可以使用st来访问streamlit库的所有功能
from utils import generate_script  # 从文件 langchain_组件 导入 generate_script 函数
from model import Model            # 从文件 model_组件 导入 Model 类

# 侧边栏 布局
with st.sidebar:  # 侧边栏 布局
    模型列表 = ["gemini-2.0-flash","deepseek-V3","kimi_moonshot"]
    单选模型 = st.selectbox("模型选择:", 模型列表, index=1)
    f"你选择的模型为：{单选模型}"  # 显示 字符串
    st.markdown("---")

    if 单选模型:
        if 单选模型 == "gemini-2.0-flash":
            st_api_key = st.text_input("请输入API密钥:", type="password")  # 密码 输入框 # 返回 文字
            st.markdown("[API获取地址](https://ai.google.dev/gemini-api/docs?hl=zh-cn)")
        elif 单选模型 == "deepseek-V3":
            st_api_key = st.text_input("请输入API密钥:", type="password")  # 密码 输入框 # 返回 文字
            st.markdown("[API获取地址](https://api-docs.deepseek.com/zh-cn/)")
        elif 单选模型 == "kimi_moonshot":
            st_api_key = st.text_input("请输入API密钥:", type="password")  # 密码 输入框 # 返回 文字
            st.markdown("[API获取地址](https://platform.moonshot.cn/console/account)")

# 显示 大标题
st.title("🎬短视频脚本生成器")  # 显示 大标题

# 行文字 输入框
st_视频主题 = st.text_input("💡请输入视频主题")  # 行文字 输入框  # 返回 文字

# 数字 输入框
st_视频时长 = st.number_input("⌚请输入视频时长（分钟）",value=1.0,min_value=0.1,step=0.1)  # 数字 输入框  # 返回 输入数字

# 数字 输入框
st_创造力 = st.number_input("✨请输入创意值（0-2）",value=1.0,min_value=0.0,max_value=2.0,step=0.1)  # 数字 输入框 # 返回 输入数字

# 按钮 交互
st_提交按钮 = st.button("生成脚本")  # 按钮 交互 # 返回 布尔值（点击True，不按False)

# +------------------------------------------------------------------+
# |                             提交前 检查                            |
# +------------------------------------------------------------------+
# 检测api_key是否输入:
if st_提交按钮 and not st_api_key:  # 如果 点击按钮 并没有 输入 AIP密钥
    st.info("请输入API密钥")  # 提醒 提示
    st.stop()               # 终止 # 类似break

# 检测视频主题是否输入:
if st_提交按钮 and not st_视频主题: # 如果 点击按钮 并没有 输入 主题
    st.info("请输入视频主题")       # 提醒 提示
    st.stop()                    # 终止 # 类似break

# +------------------------------------------------------------------+
# |                             提交                                  |
# +------------------------------------------------------------------+
# 提交 调用自定义函数
if st_提交按钮:
    # 加载等待提示
    with st.spinner("AI正在思考中，请等待..."):  # 使用 st.spinner 创建一个加载动画，提示用户 AI 正在思考 # 只要以下代码没有运行完，就会一直提示正在加载
        # 根据选中的模型，创建 Model 实例，并传入 temperature
        if 单选模型 == "gemini-2.0-flash":
            st_模型 = Model(temperature=st_创造力,api_key=st_api_key).gemini_2_flash
        elif 单选模型 == "deepseek-V3":
            st_模型 = Model(temperature=st_创造力,api_key=st_api_key).deepseek_v3
        elif 单选模型 == "kimi_moonshot":
            st_模型 = Model(temperature=st_创造力,api_key=st_api_key).kimi_moonshot_v1_8k
        # 提交
        维基搜索_结果, 视频主题, 视频脚本 = generate_script(st_视频主题,st_视频时长,选择模型=st_模型)  # 调用函数 返回 结果

    # 成功 提示
    st.success("视频脚本生成成功")   # 成功 提示
    st.divider()  # 显示 分割线

    # +---------------------------------------------------+
    # |                    显示生成内容                      |
    # +---------------------------------------------------+
    # 显示 主题
    st.subheader("🖍视频主题") # 显示 副标题
    st.write(视频主题)
    st.divider()  # 显示 分割线

    # 显示 脚本
    st.subheader("📄视频脚本")  # 显示 副标题
    st.write(视频脚本)
    st.divider()  # 显示 分割线

    # 折叠展开 维基百科
    with st.expander("🔎维基百科搜索结果"):
        st.info(维基搜索_结果)  # 提醒 提示

# streamlit run main.py