from openai import OpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper
import requests
import urllib3
from requests.exceptions import SSLError

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def generate_script(subject, video_length, creativity, api_key):
    title_template = ChatPromptTemplate.from_messages(  
        [
            ("human", "请为'{subject}'这个主题的视频想一个吸引人的标题")
        ]
    )

    script_template = ChatPromptTemplate.from_messages(
        [
            ("human","""你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
             视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
             要求开头抓住眼球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
             整体内容的表达方式要尽量轻松有趣，吸引年轻人。
             脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
             ```{wikipedia_search}```""")
        ]
    )

    llm = ChatOpenAI(
        api_key = api_key, 
        base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1", 
        model = "deepseek-v3",
        temperature = creativity
    )

    title_chain = title_template | llm
    script_chain = script_template | llm

    title = title_chain.invoke({"subject": subject}).content

    # 创建自定义会话以禁用SSL验证
    session = requests.Session()
    session.verify = False  # 禁用SSL验证
    
    # 使用自定义会话创建WikipediaAPIWrapper
    search = WikipediaAPIWrapper(
        lang="zh",
        requests_session=session,  # 使用自定义会话
        top_k_results=3  # 限制结果数量
    )
    
    try:
        search_result = search.run(subject)
    except SSLError:
        # 如果SSL错误仍然发生，返回空结果
        search_result = "维基百科搜索结果不可用"
    except Exception as e:
        # 处理其他可能的异常
        search_result = f"搜索时出错: {str(e)}"

    script = script_chain.invoke({"title": title, "duration": video_length,
                                  "wikipedia_search": search_result}).content
    
    return search_result, title, script
