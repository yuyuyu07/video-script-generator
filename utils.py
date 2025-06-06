from langchain_core.prompts import ChatPromptTemplate  # 导入 聊天提示模板 类
from langchain_openai import ChatOpenAI                # 导入 聊天模型的类
from langchain_community.utilities import WikipediaAPIWrapper  # 导入 维基百科API 类
from model import Model
def generate_script(主题, vudei_长度,选择模型):
    # ------创建 提示模板------
    标题_template = ChatPromptTemplate.from_messages(
        [
            ("human", "请为{subject}这个主题的视频想一个吸引人的标题"),
        ]
    )

    内容_template = ChatPromptTemplate.from_messages(
        [
            ("human",
             """你是一位资深的影视编剧。根据以下创意构思和相关信息，为视频写一个分镜脚本表。
             创意构思：{标题}，视频时长：{持续时间}分钟，生成的脚本的长度尽量遵循视频时长的要求。
             要求开头抓住眼球，中间提供干货内容，结尾有惊喜反转。
             先介绍视频故事大概，然后再生成分镜脚本。
             分镜脚本表格式也请按照【镜头号、时间码（格式0:00-0:03）、画面描述、镜头语言（景别、运镜、景深、光线、色彩、构图）、环境/细节、人物、动作/表情、台词/旁白、音效】分隔，每个分镜脚本 1-5 秒钟。
             整体内容的表达方式要尽量轻松有趣、搞笑、又有一定的思考，吸引年轻人。
             脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
             ```{wikipedia_search}```"""),  # wikipedia_search（维基百科搜索）
        ]
    )

    # ------创建 模型组件------
    模型组件 = 选择模型

    # ------创建 链------
    标题_chain = 标题_template | 模型组件
    内容_chain = 内容_template | 模型组件

    # ------维基百科------
    维基搜索 = WikipediaAPIWrapper(lang="zh")  # 创建 维基百科API 对象
    维基搜索_结果 = 维基搜索.run(主题)            # 调用 .run()方法 搜索 返回摘要

    # ------链式调用------
    视频主题 = 标题_chain.invoke({"subject": 主题}).content
    视频内容 = 内容_chain.invoke({"标题": 主题, "持续时间": vudei_长度,"wikipedia_search": 维基搜索_结果}).content

    # 返回
    return 维基搜索_结果, 视频主题, 视频内容
