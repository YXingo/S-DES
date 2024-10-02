from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import DES

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)
CORS(app, resources={r'/*': {'origins': '*'}})


# 新增的路由处理加密请求
@app.route('/encrypt', methods=['POST'])
def handle_encryption():
    data = request.json
    plain_text = data.get('plainText')
    secret_key = data.get('secretKey')

    if not plain_text or not secret_key:
        return jsonify({'error': '缺少明文或密钥'}), 400

    try:
        # 将密钥字符串转换为整数列表
        int_key = [int(bit) for bit in secret_key]
        encrypted_text = DES.encrypt(plain_text, int_key)
        print(f"Encrypted text: {encrypted_text}")
        return jsonify({'encryptedText': str(encrypted_text)})
    except Exception as e:
        print(f"Encryption error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/decrypt', methods=['POST'])
def handle_decryption():
    data = request.json
    cipher_text = data.get('cipherText')
    secret_key = data.get('secretKey')

    if not cipher_text or not secret_key:
        return jsonify({'error': '缺少密文或密钥'}), 400

    try:
        # 将密钥字符串转换为整数列表
        int_key = [int(bit) for bit in secret_key]
        decrypted_text = DES.decrypt(cipher_text, int_key)
        print(f"Decrypted text: {decrypted_text}")
        return jsonify({'decryptedText': str(decrypted_text)})
    except Exception as e:
        print(f"Decryption error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/getKey', methods=['POST'])
def get_key():
    try:
        random_key = DES.generate_random_key()
        random_key = ''.join(str(num) for num in random_key)
        print(f"Secret Key: {random_key}")
        return jsonify({'secretKey': str(random_key)})
    except Exception as e:
        print(f"error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 明文He，密文b5Q=对应的密钥有四个
@app.route('/bruteforce', methods=['POST'])
def bruteforce():
    data = request.json
    plaintext = data.get('plaintext')
    ciphertext = data.get('ciphertext')

    if not plaintext or not ciphertext:
        return jsonify({'error': '请提供明文和密文'}), 400

    start_time = time.time()
    found_keys = DES.find_all_keys_sdes(plaintext, ciphertext)
    end_time = time.time()

    time_taken = end_time - start_time

    if found_keys:
        return jsonify({
            'key': found_keys,
            'time_taken': round(time_taken, 2)
        })
    else:
        return jsonify({'error': '未找到匹配的密钥'}), 404


# 主程序入口
if __name__ == '__main__':
    app.run(debug=DEBUG)
