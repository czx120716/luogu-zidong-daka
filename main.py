import requests
import os
import sys

def luogu_punch():
    cookie_str = os.getenv("LUOGU_COOKIE")
    if not cookie_str:
        print("❌ 错误：未检测到环境变量 LUOGU_COOKIE")
        sys.exit(1)

    url = "https://www.luogu.com.cn/index/ajax_punch"
    
    # 更完整的浏览器伪装头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.luogu.com.cn/",
        "Origin": "https://www.luogu.com.cn",
        "x-requested-with": "XMLHttpRequest",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Connection": "keep-alive"
    }

    cookies = {}
    for item in cookie_str.split(';'):
        item = item.strip()
        if '=' in item:
            key, value = item.split('=', 1)
            cookies[key] = value

    try:
        # 使用 session 保持连接状态
        session = requests.Session()
        session.headers.update(headers)
        session.cookies.update(cookies)
        
        response = session.get(url, timeout=15)

        # 打印响应内容前100个字符用于调试
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容预览: {response.text[:200]}")

        try:
            data = response.json()
        except:
            msg = f"❌ 服务器返回了非 JSON 数据\n状态码: {response.status_code}"
            print(msg)
            return

        code = data.get('code')
        if code == 200:
            html_msg = data.get('more', {}).get('html', '未知')
            print(f"✅ 打卡成功！\n🎉 运势: {html_msg}")
        elif code == 201:
            print(f"✅ 今天已经打过卡了！{data.get('message', '')}")
        else:
            error_msg = data.get('message', '未知错误')
            print(f"⚠️ 打卡失败，Code: {code}\n错误: {error_msg}")
            if code == 401:
                print("❗ Cookie 已过期，请重新获取！")

    except Exception as e:
        print(f"❌ 脚本异常: {e}")

if __name__ == "__main__":
    luogu_punch()
