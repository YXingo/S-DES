<template>
    <el-container class="container">
        <el-header class="header">
            <h2>S-DES加解密系统</h2>
        </el-header>
        <el-main class="main">

            <div class="leftSide">
                <br><br>
                <el-card class="leftCardStyle" shadow="never" :class="{ selectedCard: cardID == 0 }"
                    @click="changeID0">加密系统</el-card>
                <el-card class="leftCardStyle" shadow="never" :class="{ selectedCard: cardID == 1 }"
                    @click="changeID1">解密系统</el-card>
                <el-card class="leftCardStyle" shadow="never" :class="{ selectedCard: cardID == 2 }"
                    @click="changeID2">暴力破解</el-card>
                <el-card class="redLeftCardStyle" shadow="never" style="color: red;" @click="exitSystem">退出系统</el-card>
            </div>

            <div class="divider"></div>
            <div class="rightSide">

                <div class="rightTitle">
                    <h2 v-if="cardID == 0" class="title">加密系统</h2>
                    <h2 v-if="cardID == 1" class="title">解密系统</h2>
                    <h2 v-if="cardID == 2" class="title">暴力破解</h2>
                </div>

                <div class="rightContent">
                    <div class="centerInfo">

                        <div v-if="cardID == 0" class="input">
                            <div
                                style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                                <h3>明文</h3>
                                <el-input v-model="plainText" style="width: 500px; margin-left: 20px;"
                                    placeholder="请输入明文" />
                            </div>
                            <div
                                style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                                <h3>密钥</h3>
                                <el-input v-model="secretKey" style="width: 500px; margin-left: 20px;"
                                    placeholder="请输入密钥" />
                                <el-button style="font-weight: 600; margin-left: 20px;"
                                    @click="getKey">获取随机密钥</el-button>
                            </div>
                            <div
                                style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px; margin-top: 10px;">
                                <el-button style="font-weight: 600;" @click="encryption">开始加密</el-button>
                                <el-input v-model="enResult" style="width: 450px; margin-left: 20px;" placeholder="" />
                            </div>
                        </div>
                        <div v-if="cardID == 1" class="input">
                            <div
                                style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                                <h3>密文</h3>
                                <el-input v-model="cipherText" style="width: 500px; margin-left: 20px;"
                                    placeholder="请输入密文" />
                            </div>
                            <div
                                style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                                <h3>密钥</h3>
                                <el-input v-model="secretKey" style="width: 500px; margin-left: 20px;"
                                    placeholder="请输入密钥" />
                                <el-button style="font-weight: 600; margin-left: 20px;"
                                    @click="getKey">获取随机密钥</el-button>
                            </div>
                            <div
                                style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px; margin-top: 10px;">
                                <el-button style="font-weight: 600;" @click="decryption">开始解密</el-button>
                                <el-input v-model="deResult" style="width: 450px; margin-left: 20px;" placeholder="" />
                            </div>
                        </div>
                        <div v-if="cardID == 2" class="input">
                            <div
                                style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                                <h3>明文</h3>
                                <el-input v-model="plainText" style="width: 500px; margin-left: 20px;"
                                    placeholder="请输入明文" />
                            </div>
                            <div
                                style="display: flex; flex-direction: row; align-items: center; justify-content: left; margin-left: 30px">
                                <h3>密文</h3>
                                <el-input v-model="cipherText" style="width: 395px; margin-left: 20px; margin-right: 20px;"
                                    placeholder="请输入密文" />
                                <el-button style="font-weight: 600;" @click="crack">开始破解</el-button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </el-main>
    </el-container>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import axios from 'axios'
const cardID = ref(0);
const isEncryption = ref(true);
const isViolent = ref(false)
const plainText = ref("");
const cipherText = ref("");
const secretKey = ref("");
const enResult = ref("");
const deResult = ref("");
const solvedKey = ref("");
const timeTaken = ref("");


function changeID0() {
    cardID.value = 0;
}

function changeID1() {
    cardID.value = 1;
}

function changeID2() {
    cardID.value = 2;
}

// 加密函数，从后端获取加密结果
async function encryption() {
    try {
        // 检查输入是否为空
        if (!plainText.value || !secretKey.value) {
            alert('请输入明文和密钥')
            return
        }

        // 发送请求到后端
        const response = await axios.post('http://localhost:5000/encrypt', {
            plainText: plainText.value,
            secretKey: secretKey.value
        })

        enResult.value = response.data.encryptedText

        console.log('加密成功:', enResult.value)
    } catch (error) {
        console.error('加密失败:', error)
        alert('加密失败，请稍后再试')
    }
}


// 加密函数，从后端获取加密结果
async function decryption() {
    try {
        // 检查输入是否为空
        if (!cipherText.value || !secretKey.value) {
            alert('请输入密文和密钥')
            return
        }

        // 发送请求到后端
        const response = await axios.post('http://localhost:5000/decrypt', {
            cipherText: cipherText.value,
            secretKey: secretKey.value
        })

        deResult.value = response.data.decryptedText

        console.log('解密成功:', deResult.value)
    } catch (error) {
        console.error('解密失败:', error)
        alert('解密失败，请稍后再试')
    }
}



// 随机生成密钥
async function getKey() {
    try {
        // 发送请求到后端
        const response = await axios.post('http://localhost:5000/getKey', {})

        secretKey.value = response.data.secretKey

        console.log('获取密钥成功:', secretKey.value)
    } catch (error) {
        console.error('获取密钥失败:', error)
        alert('获取密钥失败，请稍后再试')
    }
}

async function crack() {
    try {
        // 检查输入是否为空
        if (!cipherText.value || !plainText.value) {
            alert('请输入明文和密文')
            return
        }

        // 发送请求到后端
        const response = await axios.post('http://localhost:5000/bruteforce', {
            plaintext: plainText.value,
            ciphertext: cipherText.value
        })

        solvedKey.value = response.data.key
        timeTaken.value = response.data.time_taken

        console.log('解密成功:', solvedKey.value, '  用时:', timeTaken.value)
        const message = `解密成功！用时${timeTaken.value}秒\n解密结果：${solvedKey.value.join(', ')}`
        alert(message)
    } catch (error) {
        console.error('解密失败:', error)
        alert('解密失败，请稍后再试')
    }
}

function exitSystem() {
    alert('您已退出系统！')
}
</script>

<style scoped>
.container {
    width: 100%;
    height: 100%;
    background: rgb(247, 249, 253);
}

.header {
    background-color: rgb(255, 255, 255);
    display: flex;
    justify-content: center;
    align-items: center;
}

.main {
    display: flex;
    padding: 0;
}

.centerInfo {
    background: linear-gradient(to bottom right, #b4daff, #fff);
    width: 95%;
    height: 95%;
    border-radius: 40px;
    display: flex;
    /* align-items: ; */
    justify-content: left;
}

.leftSide {
    width: 15%;
    display: flex;
    align-items: center;
    flex-direction: column;
}

.rightSide {
    width: 85%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.leftCardStyle {
    width: 150px;
    height: 60px;
    /* height: 20%; */
    display: flex;
    justify-content: center;
    align-items: center;
    margin-left: auto;
    background-color: rgb(247, 249, 254);
    border: none;
    cursor: pointer;
    margin-top: 5px;
    /* margin-bottom: 20px; */
    margin-right: 0px;
}

.leftCardStyle:hover {
    background-color: rgb(220, 235, 255);
    color: rgb(115, 163, 231);
    font-weight: bold;
    border-radius: 10px;
    cursor: pointer;
    margin-right: 20px;
}

.redLeftCardStyle {
    width: 150px;
    height: 60px;
    margin-left: auto;
    background-color: rgb(247, 249, 254);
    border: none;
    cursor: pointer;
    margin-right: 0px;
    margin-top: 5px;
}

.redLeftCardStyle:hover {
    background-color: rgba(255, 0, 0, 0.1);
    font-weight: bold;
    border-radius: 10px;
    cursor: pointer;
    margin-right: 20px;
}


.selectedCard {
    background-color: rgb(220, 235, 255);
    color: rgba(90, 156, 248, 1);
    font-weight: bold;
    border-radius: 10px;
    cursor: pointer;
    margin-right: 20px;
}

.divider {
    width: 1px;
    background-color: #ccc;
}

.rightTitle {
    display: flex;
    width: 100%;
    height: 10%;
}

.rightContent {
    width: 100%;
    height: 90%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.title {
    margin-left: 20px;
}

.input {
    width: 60%;
    height: 40%;
    display: flex;
    flex-direction: column;
    margin-top: 30px;
    /* align-items: center; */
    justify-content: left;
}
</style>