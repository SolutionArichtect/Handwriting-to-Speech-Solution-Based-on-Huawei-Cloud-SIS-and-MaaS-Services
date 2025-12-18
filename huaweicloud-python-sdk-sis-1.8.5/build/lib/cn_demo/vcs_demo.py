import base64
import os
from huaweicloud_sis.bean.vcs_register_voice_request import RegisterVoiceRequest
from huaweicloud_sis.bean.vcs_synthesis import VcsSynthesisRequest
from huaweicloud_sis.client.vcs_client import VcsClient
from huaweicloud_sis.bean.sis_config import SisConfig

# 鉴权参数
# 认证用的ak和sk硬编码到代码中或者明文存储都有很大的安全风险，建议在配置文件或者环境变量中密文存放，使用时解密，确保安全； 
# 本示例以ak和sk保存在环境变量中来实现身份验证为例，运行本示例前请先在本地环境中设置环境变量HUAWEICLOUD_SIS_AK/HUAWEICLOUD_SIS_SK/HUAWEICLOUD_SIS_PROJECT_ID。
ak = os.getenv("HUAWEICLOUD_SIS_AK")             # 从环境变量获取ak 参考https://support.huaweicloud.com/sdkreference-sis/sis_05_0003.html
assert ak is not None, "Please add ak in your develop environment"
sk = os.getenv("HUAWEICLOUD_SIS_SK")             # 从环境变量获取sk 参考https://support.huaweicloud.com/sdkreference-sis/sis_05_0003.html
assert sk is not None, "Please add sk in your develop environment"
region = ''         # region，如cn-north-4
project_id = ""     # project id 同region一一对应，参考https://support.huaweicloud.com/api-sis/sis_03_0008.html

path = "" # 参考音频路径
voice_name = "" # 声音名称
text = "这是一个测试。" # 待合成文本

def register_voice_example(path, voice_name):
    with open(path, 'rb') as f:
        data = f.read()
        data = str(base64.b64encode(data), 'utf-8')
    config = SisConfig()
    config.set_connect_timeout(10)       # 设置连接超时，单位s
    config.set_read_timeout(60)          # 设置读取超时，单位s
    vcs_client = VcsClient(ak, sk, region, project_id, sis_config=config)
    register_voice_request = RegisterVoiceRequest(data, voice_name)
    result = vcs_client.register_voice(register_voice_request)
    print(result)

def query_example():
    config = SisConfig()
    config.set_connect_timeout(10)       # 设置连接超时，单位s
    config.set_read_timeout(60)          # 设置读取超时，单位s
    vcs_client = VcsClient(ak, sk, region, project_id, sis_config=config)
    result = vcs_client.query_voice_name()
    print(result)


def synthesis_example(text, voice_name):
    # step1 初始化客户端
    config = SisConfig()
    config.set_connect_timeout(10)       # 设置连接超时，单位s
    config.set_read_timeout(60)          # 设置读取超时，单位s
    vcs_client = VcsClient(ak, sk, region, project_id, sis_config=config)
    synthesis_request = VcsSynthesisRequest(text, voice_name)
    synthesis_request.set_sample_rate("16000")
    synthesis_request.set_audio_format("wav")
    synthesis_request.set_saved(False)
    synthesis_request.set_saved_path("demo.wav")
    result = vcs_client.synthesis(synthesis_request)
    print(result)

if __name__ == '__main__':
    # 注册
    register_voice_example(path, voice_name)
    # 查询
    query_example()
    # 合成
    synthesis_example(text, voice_name)