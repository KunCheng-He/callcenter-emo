<script lang="ts" setup>
import { ref } from "vue"
import { useAVLine } from "vue-audio-visual"
import HomeHeader from "./components/HomeHeader.vue"
import NumerShow from "./components/NumerShow.vue"

const player = ref(null)
const canvas = ref(null)

useAVLine(player, canvas, {
  src: "http://127.0.0.1:13331/get-audio/?path=/upload_files/2024/02/05/test2_unzip/z1.mp3",
  canvWidth: 600,
  canvHeight: 120,
  lineColor: ["#FFF", "rgb(0,255,127)", "#00f"]
})
</script>

<template>
  <div class="app-container">
    <!--  顶部用户信息 -->
    <el-card shadow="never"><HomeHeader /></el-card>
    <!-- 系统部分统计数据展示 -->
    <NumerShow />
    <el-card shadow="never">
      <el-divider content-position="left">原始音频</el-divider>
      <audio
        class="audio-player"
        ref="player"
        crossorigin="anonymous"
        src="http://127.0.0.1:13331/get-audio/?path=/upload_files/2024/02/05/test2_unzip/z1.mp3"
        controls
      />
      <div class="audio-canvas-layout"><canvas class="audio-canvas" ref="canvas" /></div>
    </el-card>
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
