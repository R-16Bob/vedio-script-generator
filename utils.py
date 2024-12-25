# 所有与大模型交互的代码
import os

from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_community.utilities import WikipediaAPIWrapper
def generate_script(subject, video_length, creativity, model_name, api_key="000"):
    '''
    :returns
    1. 获取视频标题
    2. 调用维基百科api获得信息
    3. 获取视频脚本内容
    '''
    title_template = ChatPromptTemplate.from_messages(
        [("human", "请为'{subject}'这个主题的视频想一个吸引人的标题")]
    )
    script_template = ChatPromptTemplate.from_messages(
#         [("human",
#              """你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
#              视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
#              要求开头抓住限球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
#              整体内容的表达方式要尽量轻松有趣，吸引年轻人。
#              脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
#              ```{wikipedia_search}```""")
# ]
        [("human",
          """你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
          视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
          要求开头抓住限球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
          整体内容的表达方式要尽量轻松有趣，吸引年轻人。
          """)
         ]
    )
    # 获取模型
    if "gpt" in model_name:
        model = ChatOpenAI(model="gpt-4o-mini",api_key=api_key, temperature=creativity, base_url="https://api.aigc369.com/v1")
    else:
        model = ChatOllama(model=model_name,  temperature=creativity)
    # chain，使用LangChain表达式语言
    title_chain = title_template | model
    script_chain = script_template | model

    title = title_chain.invoke({"subject": subject}).content
    # 维基百科调用
    # search = WikipediaAPIWrapper(lan="zh")
    # search_result = search.run(subject)

    # script = script_chain.invoke({"title": title, "duration": video_length, "wikipedia_search": search_result}).content
    # return title, search_result, script
    # script = script_chain.invoke({"title": title, "duration": video_length}).content
    chain_stream = script_chain.stream({"title": title, "duration": video_length})
    return title, chain_stream

if __name__ == "__main__":
    title, stream=generate_script("呼啸山庄", 0.6, 0.7, "glm4", os.getenv("OPENAI_API_KEY"))
    print(title)
    for chunk in stream:
        print(chunk.content, end="", flush=True)
