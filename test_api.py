from openai import OpenAI
import json

client = OpenAI(
    api_key="",
    base_url=""
)

# 简单测试先
print("=== 基础连通测试 ===")
try:
    response = client.chat.completions.create(
        model="glm-5.1",
        messages=[{"role": "user", "content": "你好，请用JSON格式回复：{\"msg\": \"hello\"}"}],
        temperature=0.7,
        max_tokens=100
    )
    print(f"response类型: {type(response)}")
    print(f"完整response: {response}")
    print(f"choices: {response.choices}")
    if response.choices:
        c = response.choices[0]
        print(f"choice.message: {c.message}")
        print(f"content: {c.message.content}")
        print(f"role: {c.message.role}")
except Exception as e:
    print(f"错误: {type(e).__name__}: {e}")

# 尝试用 responses API
print("\n=== 尝试 responses API ===")
try:
    resp2 = client.responses.create(
        model="glm-5.1",
        input="你好，请回复一个简单的JSON"
    )
    print(f"responses结果: {resp2}")
    print(f"output: {resp2.output_text if hasattr(resp2, 'output_text') else 'N/A'}")
except Exception as e:
    print(f"responses API错误: {type(e).__name__}: {e}")
