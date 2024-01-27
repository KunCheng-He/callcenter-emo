<script setup lang="ts">
import { ref, onBeforeMount } from "vue"
import { ElMessageBox } from "element-plus"
import { useAVLine } from "vue-audio-visual"
import { useRouter } from "vue-router"
import { getUserInfo } from "@/utils/cache/cookies"
import { type AudioData } from "@/api/audio/types/audio"
import { getNOCheckAudioApi } from "@/api/audio"
import { getEmotionForAudioApi } from "@/api/emotion"

defineOptions({
  name: "CheckAudio"
})

// const loading = ref<boolean>(false)

const router = useRouter()

const userinfo = getUserInfo()

// 通过 userinfo 判断用户角色是否为审计，否则弹窗提示，跳转首页
if (userinfo.role.match(/\/roles\/(\d+)\/$/)[1] != "2") {
  ElMessageBox.alert("您非审计用户，无法对音频进行审核，确认后将跳转首页。", "提示", {
    confirmButtonText: "OK",
    callback: () => {
      router.push({ path: "/" })
    }
  })
}

// 当前用户角色符合

/** 未审核音频列表 */
const noCheckAudioList = ref<AudioData[]>([])

/** 当前未审核音频 */
const noCheckAudio = ref<AudioData | null>(null)

/** 所有音频请求后端url */
const oriAudioUrl = ref<string>("")
const leftAudioUrl = ref<string>("")
const rightAudioUrl = ref<string>("")

/** 音频对应的情感 */
const frameNum = ref<number>(0)
const leftEmotion = ref<number[] | null>(null)
const rightEmotion = ref<number[] | null>(null)

/** 各音乐播放器及其画布 */
const player1 = ref(null)
const canvas1 = ref(null)
const player2 = ref(null)
const canvas2 = ref(null)
const player3 = ref(null)
const canvas3 = ref(null)

/** 获取未审核音频列表 */
const getNoCheckAudio = async () => {
  try {
    noCheckAudioList.value = await getNOCheckAudioApi()
    isHave() // 判断是否全部审核完成
  } catch (error) {
    console.error("获取未审核音频列表失败", error)
  }
}

/** 音频已经全部审核完成则跳转到首页 */
const isHave = () => {
  if (noCheckAudioList.value.length == 0) {
    ElMessageBox.alert("音频全部审核完成，确认后将跳转首页。", "提示", {
      confirmButtonText: "OK",
      callback: () => {
        router.push({ path: "/" })
      }
    })
  } else {
    noCheckAudio.value = noCheckAudioList.value[0]
    // 合成音频后端 url
    getAudioUrl()
    // 请求音频情感
    getEmotion()
  }
}

/** 合成音频后端 url */
const getAudioUrl = () => {
  const baseUrl = "http://127.0.0.1:8000/get-audio/?path="
  oriAudioUrl.value = baseUrl + noCheckAudio.value.orig_file_path
  leftAudioUrl.value = baseUrl + noCheckAudio.value.left_file_path
  rightAudioUrl.value = baseUrl + noCheckAudio.value.right_file_path
}

/** 请求情感结果 */
const getEmotion = async () => {
  try {
    const emotionDatas = await getEmotionForAudioApi(noCheckAudio.value.url.match(/\/audio\/(\d+)\/$/)[1])
    const emotionData = emotionDatas[0]
    frameNum.value = emotionData.frame_num
    leftEmotion.value = emotionData.left_emotions
    rightEmotion.value = emotionData.right_emotions
  } catch (error) {
    ElMessageBox.alert("情感结果请求失败，确认后将跳转首页。", "提示", {
      confirmButtonText: "OK",
      callback: () => {
        router.push({ path: "/" })
      }
    })
  }
}

/** 设置音乐播放器 */
const setPlayer = () => {
  useAVLine(player1, canvas1, {
    src: oriAudioUrl,
    canvWidth: 600,
    canvHeight: 120,
    lineColor: ["#FFF", "rgb(0,255,127)", "#00f"]
  })
  useAVLine(player2, canvas2, {
    src: leftAudioUrl,
    canvWidth: 600,
    canvHeight: 120,
    lineColor: ["#FFF", "rgb(0,255,127)", "#00f"]
  })
  useAVLine(player3, canvas3, {
    src: rightAudioUrl,
    canvWidth: 600,
    canvHeight: 120,
    lineColor: ["#FFF", "rgb(0,255,127)", "#00f"]
  })
}

// 在页面加载前调用的方法
onBeforeMount(() => {
  getNoCheckAudio() // 获取未审核音频列表
  setPlayer() // 设置音乐播放器
})
</script>

<template>
  <div class="app-container">
    <el-card shadow="never">
      <el-divider content-position="left">原始音频</el-divider>
      <audio class="audio-player" ref="player1" crossorigin="anonymous" :src="oriAudioUrl" controls />
      <div class="audio-canvas-layout"><canvas class="audio-canvas" ref="canvas1" /></div>
    </el-card>
    <el-card shadow="never">
      <el-divider content-position="left">左声道音频</el-divider>
      <audio class="audio-player" ref="player2" crossorigin="anonymous" :src="leftAudioUrl" controls />
      <div class="audio-canvas-layout"><canvas class="audio-canvas" ref="canvas2" /></div>
    </el-card>
    <el-card shadow="never">
      <el-divider content-position="left">右声道音频</el-divider>
      <audio class="audio-player" ref="player3" crossorigin="anonymous" :src="rightAudioUrl" controls />
      <div class="audio-canvas-layout"><canvas class="audio-canvas" ref="canvas3" /></div>
    </el-card>
  </div>
</template>

<style lang="scss" scoped>
.el-card {
  border-radius: 10px;
  margin-bottom: 20px;
  :deep(.el-card__body) {
    padding-bottom: 2px;
  }
}

.el-divider {
  margin-top: 10px;
  margin-bottom: 25px;
}

.audio-player {
  width: 100%;
  height: 100%;
}

.audio-canvas-layout {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 20vh; // 可根据需要调整高度，这里设置为视口的高度

  .audio-canvas {
    // 设置canvas样式，可以根据需要进行调整
    border: 1px solid #ccc;
  }
}
</style>
