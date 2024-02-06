<script lang="ts" setup>
import HomeHeader from "./components/HomeHeader.vue"
import NumerShow from "./components/NumerShow.vue"
import Sort from "./components/Sort.vue"
</script>

<template>
  <div class="app-container">
    <!--  顶部用户信息 -->
    <el-card shadow="never"><HomeHeader /></el-card>
    <!-- 系统部分统计数据展示 -->
    <NumerShow />
    <!-- 客服与审计统计排序展示 -->
    <Sort />
  </div>
</template>

<style lang="scss" scoped>
.el-card {
  margin-bottom: 20px;
}

.audio-player {
  width: 100%;
  height: 100%;
}
</style>
