import requests
import os
import sys

def luogu_punch():
    cookie_str = os.getenv("LUOGU_COOKIE")
    if not cookie_str:
        print("❌ 错误：未检测到环境变量 LUOGU_COOKIE")
        print("洛谷打卡脚本报错", "❌ 未找到 LUOGU_COOKIE，请检查 GitHub Secrets 设置。")
        sys.exit(1)

    url = "https://www.luogu.com.cn/index/ajax_punch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.luogu.com.cn/",
        "x-requested-with": "XMLHttpRequest"
    }

    # 手动解析 Cookie 字符串为字典
    cookies = {}
    for item in cookie_str.split(';'):
        item = item.strip()
        if '=' in item:
            key, value = item.split('=', 1)
            cookies[key] = value

    try:
        response = requests.get(url, headers=headers, cookies=cookies, timeout=15)

        try:
            data = response.json()
        except:
            msg = f"❌ 服务器返回了非 JSON 数据，可能是网站崩溃或 Cookie 失效。\n状态码: {response.status_code}"
            print(msg)
            return

        code = data.get('code')
        if code == 200:
            html_msg = data.get('more', {}).get('html', '未知')
            msg = f"✅ 打卡成功！\n🎉 运势: {html_msg}"
            print(msg)
        elif code == 201:
            msg = f"✅ 今天已经打过卡了！\n防错信息：{data.get('message', '信息')}"
            print(msg)
        else:
            error_msg = data.get('message', '未知错误')
            msg = f"⚠️ 打卡失败，服务器返回 Code: {code}\n❌ 错误信息: {error_msg}"
            print(msg)
            if code == 401:
                msg += "\n❗ 你的 Cookie 可能已过期，请重新获取！"

    except Exception as e:
        msg = f"❌ 脚本运行发生异常: {e}"
        print(msg)

if __name__ == "__main__":
    luogu_punch()
