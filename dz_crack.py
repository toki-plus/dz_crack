import hashlib
import asyncio
import openpyxl

async def check_password(password, username, pass_hash, salt):
    global flag
    password_md5 = hashlib.md5(password.encode('utf-8')).hexdigest()
    encrypted_password = hashlib.md5((password_md5 + salt).encode('utf-8')).hexdigest()
    if encrypted_password == pass_hash:
        flag = True
        print('破解成功，"{}"的密码为：{}'.format(username, password))
        with open('result.txt', 'a+', encoding='utf-8') as f:
            f.write('破解成功，"{}"的密码为：{}'.format(username, password) + '\n')
        return True
    else:
        return False

async def check_match():
    # 匹配密码字典中的所有密码
    tasks = []
    with open('password.txt', 'r') as f:
        batch_size = 500 # 调整启动的协程数量，避免字段过大导致系统崩溃
        while True:
            lines = f.readlines(batch_size)
            if not lines:
                break
            for password in lines:
                password = password.strip()
                tasks.append(check_password(password, username, pass_hash, salt))
            await asyncio.gather(*tasks)
            tasks = []
            if flag:
                print("√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√")
                break

    # 仅匹配一个密码（密码喷洒）
    # tasks = []
    # password = 'a123456'
    # tasks.append(check_password(password, username, pass_hash, salt))
    # await asyncio.gather(*tasks)
    # if flag:
    #     print("√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√")

    print("爆破结束！")

if __name__ == '__main__':

    # 破解xlsx表格中的所有Hash（模板为：dz_hash.xlsx）
    workbook = openpyxl.load_workbook('dz_hash.xlsx')
    sheet = workbook.active

    for row in sheet.iter_rows(min_row=2, values_only=True):
        flag = False
        username = row[1]
        pass_hash = row[2]
        salt = row[3]
        print(username, pass_hash, salt)
        try:
            asyncio.run(check_match())
        except:
            continue

    # 仅破解单个Hash（测试密码为：a123456）
    # flag = False
    # username = '测试号'
    # pass_hash = '96a48dd30ff0bea1c9a5aa9e427caa20'
    # salt = '83535d'
    # asyncio.run(check_match())


