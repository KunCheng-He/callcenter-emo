<template>
    <!-- 提示 404，并提供返回首页的按钮 -->
    <div class="not-found">
        <h1>404</h1>
        <h3>页面未找到</h3>
        <div class="not-found-btn">
            <el-button type="primary" @click="goHome">返回首页</el-button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router"
const router = useRouter()

function goHome() {
    console.log('go home')
    // 路由跳转
    router.push('/')
}
</script>

<style lang="scss" scoped></style>