import time
import secrets
import base64

# 各种常量
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 6, 8]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]
IP = [2, 6, 3, 1, 4, 8, 5, 7]
IP_INVERSE = [4, 1, 3, 5, 7, 2, 8, 6]
EPBox = [4, 1, 2, 3, 2, 3, 4, 1]
P4 = [2, 4, 3, 1]
SBox1 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
SBox2 = [[0, 1, 2, 3], [2, 3, 1, 0], [3, 0, 1, 2], [2, 1, 0, 3]]


# 工具函数：置换
def permute(data, permutation_table):
    return [data[i - 1] for i in permutation_table]


# 工具函数：左移
def left_shift(bits, shifts):
    return bits[shifts:] + bits[:shifts]


# 工具函数：S盒替换
def s_box_substitution(bits, s_box):
    row = int(f"{bits[0]}{bits[3]}", 2)
    col = int(f"{bits[1]}{bits[2]}", 2)
    value = s_box[row][col]
    return [int(bit) for bit in bin(value)[2:].zfill(2)]


# 工具函数：生成子密钥
def generate_subkeys(key):
    # P10置换
    key = permute(key, P10)
    # 左移
    left, right = left_shift(key[:5], 1), left_shift(key[5:], 1)
    # 生成K1
    k1 = permute(left + right, P8)
    # 再左移
    left, right = left_shift(left, 2), left_shift(right, 2)
    # 生成K2
    k2 = permute(left + right, P8)
    return k1, k2


# 工具函数：轮函数 f_k
def fk(left_half, right_half, subkey):
    # 扩展置换
    right_expanded = permute(right_half, EPBox)
    # 与子密钥异或
    xor_result = [a ^ b for a, b in zip(right_expanded, subkey)]
    # S盒替换
    sbox_output = s_box_substitution(xor_result[:4], SBox1) + s_box_substitution(xor_result[4:], SBox2)
    # P4置换
    sbox_permuted = permute(sbox_output, P4)
    # 与左半部分异或
    result = [a ^ b for a, b in zip(left_half, sbox_permuted)]
    return result


# S-DES加密函数
def sdes_encrypt(plaintext, key):
    # 生成子密钥
    k1, k2 = generate_subkeys(key)
    # 初始置换
    ip_bits = permute(plaintext, IP)
    left, right = ip_bits[:4], ip_bits[4:]
    # 第一轮
    left1 = fk(left, right, k1)
    # 交换
    left2, right2 = right, left1
    # 第二轮
    left3 = fk(left2, right2, k2)
    # 合并并逆初始置换
    pre_output = left3 + right2
    cipher_bits = permute(pre_output, IP_INVERSE)
    return cipher_bits


# S-DES解密函数
def sdes_decrypt(ciphertext, key):
    # 生成子密钥
    k1, k2 = generate_subkeys(key)
    # 初始置换
    ip_bits = permute(ciphertext, IP)
    left, right = ip_bits[:4], ip_bits[4:]
    # 第一轮（注意密钥顺序与加密相反）
    left1 = fk(left, right, k2)
    # 交换
    left2, right2 = right, left1
    # 第二轮
    left3 = fk(left2, right2, k1)
    # 合并并逆初始置换
    pre_output = left3 + right2
    plaintext_bits = permute(pre_output, IP_INVERSE)
    return plaintext_bits


# 工具函数：将字符串转换为二进制列表
def string_to_bin(data):
    bin_data = []
    for char in data:
        bin_values = bin(ord(char))[2:].zfill(8)
        bin_data.extend([int(bit) for bit in bin_values])
    return bin_data


# 工具函数：将二进制列表转换为字符串
def bin_to_string(bin_data):
    chars = []
    for i in range(0, len(bin_data), 8):
        byte = bin_data[i:i + 8]
        byte_str = ''.join(str(bit) for bit in byte)
        chars.append(chr(int(byte_str, 2)))
    return ''.join(chars)


# 工具函数：将二进制数据转换为Base64字符串
def bin_to_base64(bin_data):
    byte_str = ''.join([str(bit) for bit in bin_data])
    byte_array = int(byte_str, 2).to_bytes((len(byte_str) + 7) // 8, byteorder='big')
    return base64.b64encode(byte_array).decode('utf-8')


# 工具函数：将Base64字符串转换为二进制数据
def base64_to_bin(base64_data):
    byte_array = base64.b64decode(base64_data.encode('utf-8'))
    bin_data = ''.join([bin(byte)[2:].zfill(8) for byte in byte_array])
    return [int(bit) for bit in bin_data]


# 加密函数（接收明文和密钥）
def encrypt(plaintext, key):
    plaintext_bits = string_to_bin(plaintext)
    cipher_bits = []
    # 按8位分块加密
    for i in range(0, len(plaintext_bits), 8):
        block = plaintext_bits[i:i + 8]
        if len(block) < 8:
            block += [0] * (8 - len(block))
        cipher_block = sdes_encrypt(block, key)
        cipher_bits.extend(cipher_block)
    return bin_to_base64(cipher_bits)


# 解密函数（接收密文和密钥）
def decrypt(ciphertext, key):
    cipher_bits = base64_to_bin(ciphertext)
    plaintext_bits = []
    # 按8位分块解密
    for i in range(0, len(cipher_bits), 8):
        block = cipher_bits[i:i + 8]
        plain_block = sdes_decrypt(block, key)
        plaintext_bits.extend(plain_block)
    return bin_to_string(plaintext_bits)


# 生成随机10位二进制密钥
def generate_random_key():
    random_number = secrets.randbits(10)
    key = [int(bit) for bit in bin(random_number)[2:].zfill(10)]
    return key


# 工具函数：将字符串形式的密钥转换为列表形式
def key_str_to_list(key_str):
    return [int(bit) for bit in key_str]


# 工具函数：将列表形式的密钥转换为字符串形式
def key_list_to_str(key_list):
    return ''.join(str(bit) for bit in key_list)


# 暴力破解函数
def brute_force_sdes(plaintext, ciphertext):
    """
    尝试找到将 plaintext 加密为 ciphertext 的10位密钥。

    :param plaintext: 明文字符串
    :param ciphertext: 密文的Base64字符串
    :return: 找到的密钥字符串，如果未找到则返回 None
    """
    # 转换明文和密文
    plaintext_bits = string_to_bin(plaintext)
    cipher_bits = base64_to_bin(ciphertext)

    # 确保明文和密文的块数一致
    if len(plaintext_bits) // 8 != len(cipher_bits) // 8:
        print("明文和密文的块数不一致。")
        return None

    # 遍历所有可能的10位密钥
    for key_int in range(0, 1024):
        # 将整数转换为10位二进制列表
        key_str = bin(key_int)[2:].zfill(10)
        key = key_str_to_list(key_str)

        # 加密明文
        encrypted_bits = []
        for i in range(0, len(plaintext_bits), 8):
            block = plaintext_bits[i:i + 8]
            if len(block) < 8:
                block += [0] * (8 - len(block))
            cipher_block = sdes_encrypt(block, key)
            encrypted_bits.extend(cipher_block)

        # 比较加密结果与给定密文
        # 注意：由于给定密文是Base64编码，需要确保比较的是二进制数据
        if encrypted_bits == cipher_bits[:len(encrypted_bits)]:
            return key_str  # 找到匹配的密钥

    return None  # 未找到匹配的密钥


# 新增函数：查找所有可能的密钥
def find_all_keys_sdes(plaintext, ciphertext):
    """
    查找所有能够将 plaintext 加密为 ciphertext 的10位密钥。

    :param plaintext: 明文字符串
    :param ciphertext: 密文的Base64字符串
    :return: 包含所有匹配密钥的列表，如果未找到则返回空列表
    """
    # 转换明文和密文
    plaintext_bits = string_to_bin(plaintext)
    cipher_bits = base64_to_bin(ciphertext)

    # 确保明文和密文的块数一致
    if len(plaintext_bits) // 8 != len(cipher_bits) // 8:
        print("明文和密文的块数不一致。")
        return []

    matching_keys = []

    # 遍历所有可能的10位密钥
    for key_int in range(0, 1024):
        # 将整数转换为10位二进制列表
        key_str = bin(key_int)[2:].zfill(10)
        key = key_str_to_list(key_str)

        # 加密明文
        encrypted_bits = []
        for i in range(0, len(plaintext_bits), 8):
            block = plaintext_bits[i:i + 8]
            if len(block) < 8:
                block += [0] * (8 - len(block))
            cipher_block = sdes_encrypt(block, key)
            encrypted_bits.extend(cipher_block)

        # 比较加密结果与给定密文
        if encrypted_bits == cipher_bits[:len(encrypted_bits)]:
            matching_keys.append(key_str)  # 找到匹配的密钥

    return matching_keys  # 返回所有匹配的密钥


if __name__ == "__main__":
    # 初始化数据
    data = "Hello, S-DES!"
    key = generate_random_key()
    print(f"随机生成的10位密钥: {''.join(str(bit) for bit in key)}")
    # 加密
    encrypted_text = encrypt(data, key)
    print(f"加密后的Base64数据: {encrypted_text}")
    # 解密
    decrypted_text = decrypt(encrypted_text, key)
    print(f"解密后的文本: {decrypted_text}")

    # 暴力破解示例：寻找所有可能的密钥
    print("\n--- 寻找所有可能的密钥 ---")
    # 为破解目的，选择明文和对应的密文
    plaintext_crack = data[:2]  # 例如 "He"
    ciphertext_crack = encrypt(plaintext_crack, key)
    print(f"要破解的明文: '{plaintext_crack}'")
    print(f"对应的密文 (Base64): {ciphertext_crack}")

    start_time = time.time()
    found_keys = find_all_keys_sdes(plaintext_crack, ciphertext_crack)
    end_time = time.time()
    time_taken = end_time - start_time

    if found_keys:
        print(f"找到的密钥数量: {len(found_keys)}")
        print("找到的密钥列表:")
        for k in found_keys:
            print(k)
        print(f"用时: {time_taken:.4f} 秒")
    else:
        print("未找到匹配的密钥。")
