<template>
    <div class="login-container">
        <el-form class="login-form" label-position="right" autocomplete="on" :model="loginForm">
            <div class="title-container">
                <h3 class="title">系统登录</h3>
            </div>
            <el-form-item prop="email" label="邮箱地址" :rules="emailRulses">
                <el-input v-model="loginForm.email" />
            </el-form-item>
            <el-form-item label="密码" prop="pass" :rules="passRulses">
                <el-input v-model="loginForm.pass" type="password" autocomplete="off" />
            </el-form-item>
            <div class="register-label">
                <RouterLink to="/">注册账户</RouterLink>
            </div>
            <el-form-item>
                <el-button type="primary" @click="login">登录</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script lang="ts" setup>
import { reactive } from 'vue'
import { RouterLink } from 'vue-router'

// 登录表单
const loginForm = reactive({
    email: '',
    pass: '',
})

const emailRulses = [
    {
        required: true,
        message: '请输入邮箱地址',
        trigger: 'blur',
    },
    {
        type: 'email',
        message: '请输入正确的电子邮件地址',
        trigger: ['blur', 'change'],
    },
]

const passRulses = [
    {
        required: true,
        message: '请输入密码',
        trigger: 'blur',
    },
]

// 登录函数
function login() {
    // 验证邮箱和密码是否为空
    if (loginForm.email === '' || loginForm.pass === '') {
        alert('邮箱和密码不能为空')
        return
    }
    console.log(loginForm)
}

</script>

<style lang="scss" scoped>
$bg: #283443;
$bg2: #2D3A4B;
$light_gray: #fff;
$cursor: #fff;

.login-container {
    width: 100%;
    height: 100%;
    background-size: cover;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100%;
    background-color: $bg2;
    overflow: hidden;

    .login-form {
        position: relative;
        width: 520px;
        max-width: 100%;
        margin: 0 auto;
        overflow: hidden;

        .title-container {
            position: relative;

            .title {
                font-size: 26px;
                color: $light_gray;
                margin: 0px auto 40px auto;
                text-align: center;
                font-weight: bold;
            }
        }

        .el-form-item {
            display: block;
            border-radius: 5px;
            color: #454545;
            background-color: #d7e6e3;

            .el-button {
                width: 100%;
            }
        }

        .register-label {
            font-size: 14px;
            color: #00A3F6;
            margin-bottom: 10px;
        }
    }
}
</style>
