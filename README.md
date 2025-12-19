# Math Audio Synthesizer Service

这是一个基于华为云 SIS (Speech Interaction Service) 的微服务与管线系统，用于从图片识别数学表达式，经校验与自然语言化后，合成为高质量音频。

## 功能特性

- **微服务架构**: 使用 FastAPI 构建，提供 RESTful API。
- **华为云 SIS 集成**: 封装了华为云语音合成 SDK，支持鉴权和参数配置。
- **文本预处理**: 自动处理长文本分段，并优化数学符号的朗读（如 √ -> 平方根）。
- **音频存储**: 自动按日期和 ID 存储生成的 MP3 文件。
- **日志与监控**: 记录详细的操作日志和错误日志，支持版本管理。
- **容错机制**: 网络异常自动重试，音频完整性校验。

## 快速开始

 **运行SIS后端服务**:
  使用 python start_server.py 启动服务
 **运行测试**:
  python tests/pipeline_test.py
### 前置要求

- Python 3.8+
- 华为云账号及 SIS 服务开通 (AK/SK)

### 安装与启动

1. **一键启动 (推荐 Windows 用户)**://这个功能还没有完善，可能会有一点问题
   双击运行 `run_service.bat`，脚本会自动创建虚拟环境、安装依赖并启动服务。

2. **手动启动**:
   ```bash
   pip install -r requirements.txt
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   ```

   注意：SIS SDK通过项目内本地依赖提供，脚本已自动设置 `PYTHONPATH` 指向 `huaweicloud-python-sdk-sis-1.8.5`。

### 配置

在项目根目录下创建或编辑 `key.txt` (或者使用环境变量)，格式如下:

```text
huawei_ak:YOUR_AK
huawei_sk:YOUR_SK
region:cn-east-3
project_id:YOUR_PROJECT_ID (可选)
```

### API 使用

**Endpoint:** `POST /synthesize`

**Request Body:**

```json
{
  "text": "已知函数 f(x) = x^2 + 2x + 1...",
  "question_id": "q12345",
  "voice": "chinese_xiaoyan_common"  // 可选
}
```

**Response:**

```json
{
  "status": "success",
  "audio_path": "/audio/2024-05-20/q12345_1716182930.mp3",
  "duration": 12.5
}
```

### 使用说明
- 完整管线（图片识别 → 校验 → 转译 → 合成）：
  - `POST /process-image` 上传图片并执行全流程
  - `files`: `file` 图片；`form`: `question_id`、`synthesize`、`text`(可选，提供则跳过OCR)
  - 返回包括 `ocr_text`、`answer_text`、`natural_text`、`audio_path`、`run_dir`
  - 输出目录：`output/<时间戳>/`，每一步输出与日志见 `steps.log`
  - 模型调用位置（文件与行）：
    - OCR-VL：`src/services/agent_client.py:22`（`ocr_paddle_vl`）
    - DeepSeek校验：`src/services/agent_client.py:55`（`deepseek_check`）
    - DeepSeek转译：`src/services/agent_client.py:81`（`deepseek_translate`）
    - 管线编排：`src/services/pipeline_service.py:34`（`process`）
  - 提示词修改：
    - 校验提示词：`reference/prompt_answers.txt`
    - 转译提示词：优先读取 `reference/prompt_translate.txt`，若不存在则读取 `reference/prompt_translated.txt`
    - 管线读取逻辑：`src/services/pipeline_service.py:16` 自动从上述 `reference` 路径加载

## 项目结构


```
.
├── src/                          # 源代码
│   ├── main.py                   # API 入口（/synthesize, /process-image）
│   ├── config.py                 # 配置加载（key.txt/env），输出目录创建
│   ├── services/
│   │   ├── sis_service.py        # 华为云 SIS 封装
│   │   ├── agent_client.py       # 模型直连客户端（OCR/DeepSeek）
│   │   └── pipeline_service.py   # 流程编排与逐步输出
│   ├── utils/
│   │   ├── text_processor.py     # 数学符号规范化与分段
│   │   ├── image_processor.py    # 本地 OCR （RapidOCR/pytesseract）
│   │   └── versioning.py         # 三位版本号管理与日志记录
├── tests/
│   ├── pipeline_test.py          # 管线端到端测试（默认 data/1.jpg）
│   ├── service_test.py           # 合成接口测试（/synthesize）
│   └── sdk_test.py               # 直接 SDK 合成测试
├── output/                       # 管线输出（时间戳为目录名）
├── audio_output/                 # 合成接口输出（按日期分目录）
├── log/                          # 日志目录（error_log, version_log, version_state.json）
├── requirements.txt              # 依赖列表
├── run_service.bat               # Windows 启动脚本（自动创建/回退环境）
├── Dockerfile                    # Docker 构建文件
├── key.txt                       # 配置文件 (用户提供)
└── reference/                    # 提示词与参考文件（勿修改）
```

## 用例测试
- SDK 测试：`python tests/sdk_test.py`
  - 直接调用 SDK，将文本转换为音频，输出到 `audio_output/tests/`。
  - 需要先安装华为云 SIS SDK。
- 服务测试：`python tests/service_test.py`
  - 调用本地服务接口，验证服务可用性与请求体格式。
  - 需要先运行服务：`run_service.bat` 或 `uvicorn src.main:app --host 0.0.0.0 --port 8000`.

## 整体流程（必看）
- 输入图片 → OCR-VL（PaddleOCR-VL-0.9B，`http://1.95.xxx.xx:8080/v1/chat/completions`）这里是基于PaddleOCR-VL-0.9B模型的OCR-VL服务，输入图片后，会返回图片中的文本内容。根据自身情况切换OCR，推荐使用OCR：RapidOCR、PaddleOCR等模型服务
- 文本校验 → `DeepSeek v3.2`（提示词见 `reference/prompt_answers.txt`）
- 自然语言转译 → `DeepSeek v3.2`（提示词见 `reference/prompt_translate.txt` 或 `prompt_translated.txt`）
- 语音合成 → 华为云 `SIS`（输出到 `output/<时间戳>/audio.mp3` 或 `/audio_output/<日期>/` 视接口）

## 接口说明
- `POST /process-image`
  - Form 字段：`question_id`、`synthesize`(true/false)、`text`(可选，若提供则跳过 OCR)
  - 文件字段：`file`（图片）
  - 返回：包括 `ocr_text`、`answer_text`、`natural_text`、`audio_path`
  - 示例：
    ```python
    import requests
    files = {"file": open("data/test.jpg", "rb")}
    data = {"question_id": "pipe_001", "synthesize": "true", "text": "可选文本"}
    resp = requests.post("http://127.0.0.1:8000/process-image", files=files, data=data)
    print(resp.json())
    ```

## 版本控制
- 使用三位版本号：每次成功执行流程自动增加 `PATCH`，满 10 进位到 `MINOR`。
- 历史记录写入 `log/version_log`，状态存储于 `log/version_state.json`。
- 每步控制台打印进度，同时在 `output/<时间戳>/steps.log` 记录每步输出。

## 版本历史
- 详见 `log/version_log`
