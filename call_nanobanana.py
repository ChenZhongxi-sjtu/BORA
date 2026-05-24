import os
import mimetypes
from google import genai
from google.genai import types

# 1. 初始化客户端 (请替换为你的 API_KEY)
client = genai.Client(api_key="AIzaSyDooV131tT0-SpozhiEZ4UHzRgxhy6ZqDk")

def generate_process_diagram():
    model = "gemini-3.1-flash-image-preview"
    
    # 核心：复用你之前的专业提示词
    prompt_text = (
        "第二部分：科学分类 (Classification by Activity Level) （建议使用柱状图或金字塔图，直观展示体积与放射性的反比关系）  低放废料 (LLW - Low-Level Waste)：  来源： 医院、工业、核电站运行（如手套、工服、工具、过滤器）。  特点： 体积最大（约占 90%），放射性极低，半衰期短。  处置： 浅地层埋置，数十年后即可衰变至安全水平。  中放废料 (ILW - Intermediate-Level Waste)：  来源： 核电站退役零部件、化学污泥、反应堆内构建。  特点： 体积较小（约占 7%），放射性高于 LLW，部分含有长半衰期核素。  处置： 需要更深的地下处置库或屏蔽容器。  高放废料 (HLW - High-Level Waste)：  来源： 乏燃料（使用过的核燃料），或乏燃料后处理产生的废液。  特点： 体积最小（约占 3%），但含有极高的放射性和热量，半衰期极长（数万年）。  处置： 深地质处置（DGR）是目前国际公认的最安全、最可行的最终处置方案。  第三部分：安全处置流程 (Safe Disposal Process - 以 HLW 为例) （建议使用带箭头的流程图或多重屏障系统示意图）  反应堆卸出： 乏燃料具有强放射性和高热量。  水池冷却 (几年)： 存放在核电站内的乏燃料水池中，利用水作为屏蔽和冷却剂。  干式储存 (几十年)： 冷却后转移至特制的干式储存桶（钢和混凝土结构）中，在地面临时存放。  后处理 (可选)： 回收有用的铀和钚，减少废料体积。  深地质处置 (DGR - 最终)：  多重屏障系统：  1. 废料基质： 玻璃化固化。  2. 处置罐： 耐腐蚀金属（如铜、钢）。  3. 缓冲填料： 膨润土。  4. 天然岩石： 稳定的深层地质构造（如花岗岩、盐岩）。按照上下个构图 文字要少 尽量用图像表达，突出重点，清晰易懂，背景为白色"
    )

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt_text)],
        ),
    ]

    # 配置：映射 16:9 比例和生成模式
    generate_content_config = types.GenerateContentConfig(
        image_config=types.ImageConfig(
            aspect_ratio="9:16",  # 只保留比例，删掉 image_size 和 person_generation
        ),
        response_modalities=[
            "IMAGE",
            "TEXT",
        ],
    )

    print("🚀 正在通过 SDK 呼叫 Gemini 3.1 绘制流程图...")

    file_index = 0
    try:
        # 使用流式生成
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            if chunk.parts is None:
                continue
            
            # 处理图像数据
            if chunk.parts[0].inline_data and chunk.parts[0].inline_data.data:
                # 构造文件名
                file_extension = mimetypes.guess_extension(chunk.parts[0].inline_data.mime_type) or ".png"
                file_name = f"RL_Process_Flowchart_{file_index}{file_extension}"
                
                # 获取二进制数据
                image_bytes = chunk.parts[0].inline_data.data
                
                # 保存文件
                with open(file_name, "wb") as f:
                    f.write(image_bytes)
                
                print(f"🎉 流程图生成成功！已保存为: {file_name}")
                file_index += 1
            
            # 处理可能的文本反馈（例如模型对图片的描述）
            elif chunk.text:
                print(f"💬 模型说明: {chunk.text}")

    except Exception as e:
        print(f"❌ 生成失败: {e}")

if __name__ == "__main__":
    generate_process_diagram()