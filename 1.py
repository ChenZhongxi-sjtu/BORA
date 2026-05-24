import requests
import base64

# 1. 填入你的谷歌 API Key
API_KEY = "AIzaSyAO05DSyOP14C1bPO7EWuG5d1pXAhxL4Yo"

def check_and_generate():
    print("🔍 第一步：正在向谷歌服务器查询您的 API Key 拥有哪些模型的权限...")
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
    
    try:
        response = requests.get(list_url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"❌ 查询模型失败: {e}")
        return

    # 遍历你的 Key 支持的所有模型，寻找含有 'imagen' 的画图模型
    available_models = data.get('models', [])
    imagen_model_name = None
    
    for model in available_models:
        # 如果找到了画图模型
        if 'imagen' in model['name'].lower():
            imagen_model_name = model['name']
            print(f"✅ 恭喜！找到支持的画图模型: {imagen_model_name}")
            print(f"   该模型支持的方法为: {model.get('supportedGenerationMethods', [])}")
            break

    # 如果没找到任何画图模型
    if not imagen_model_name:
        print("\n❌ 诊断结果：您的 API Key 当前【不支持】任何画图模型！")
        print("原因分析：")
        print("1. 谷歌目前对免费版 API Key 的 Imagen 画图功能有严格的地区限制（通常要求你的 Google Cloud 账号归属地及常用 IP 位于美国/欧洲等地区）。")
        print("2. 您的账号仍在排队等待开通画图权限中。")
        print("💡 建议：您可以尝试用这个 Key 调用 Gemini 文本模型，但目前无法用它生成图片。")
        return

    # ==========================================
    # 第二步：如果找到了画图模型，则开始自动画图
    # ==========================================
    print(f"\n🎨 第二步：正在使用 {imagen_model_name} 请求生成图片，请稍候...")
    
    # 自动拼接正确的生成地址
    generate_url = f"https://generativelanguage.googleapis.com/v1beta/{imagen_model_name}:predict"
    
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    }
    
    payload = {
        "instances": [{"prompt": "A cute magical flying cat, fantasy art, highly detailed"}],
        "parameters": {"sampleCount": 1, "aspectRatio": "1:1"}
    }

    try:
        gen_response = requests.post(generate_url, headers=headers, json=payload)
        gen_response.raise_for_status()
        result = gen_response.json()
        
        if "predictions" in result and len(result["predictions"]) > 0:
            base64_image = result["predictions"][0]["bytesBase64Encoded"]
            image_data = base64.b64decode(base64_image)
            filename = "my_ai_art.png"
            
            with open(filename, "wb") as file:
                file.write(image_data)
            print(f"\n🎉 成功啦！图片已保存到当前目录下的: {filename}")
        else:
            print("API 返回了成功状态，但没有找到图片数据：", result)
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ 画图请求失败: {e}")
        if gen_response.text:
            print(f"服务器返回的详细错误: {gen_response.text}")

if __name__ == "__main__":
    import warnings
    # 屏蔽掉那个烦人的 Mac OpenSSL 警告，让输出看起来更清爽
    warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")
    
    check_and_generate()