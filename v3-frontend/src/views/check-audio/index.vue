<script setup lang="ts">
import { ref, onBeforeMount } from "vue"
import { ElMessageBox, ElMessage } from "element-plus"
import { useAVLine } from "vue-audio-visual"
import { useRouter } from "vue-router"
import { getUserInfo } from "@/utils/cache/cookies"
import { type AudioData } from "@/api/audio/types/audio"
import { getNOCheckAudioApi, updateAudioCheckedApi } from "@/api/audio"
import { getEmotionForAudioApi } from "@/api/emotion"
import { updateUserApi } from "@/api/user"
import { use } from "echarts/core"
import { LineChart } from "echarts/charts"
import { TitleComponent, GridComponent, TooltipComponent } from "echarts/components"
import { CanvasRenderer } from "echarts/renderers"
import VChart from "vue-echarts"
import { useNowAudioStore } from "@/store/modules/now-audio"

use([TitleComponent, LineChart, CanvasRenderer, GridComponent, TooltipComponent])

defineOptions({
  name: "CheckAudio"
})

const loading = ref<boolean>(false)

const router = useRouter()

const userinfo = getUserInfo()

const nowAudioStore = useNowAudioStore()

// 通过 userinfo 判断用户角色是否为审计，否则弹窗提示，跳转首页
if (userinfo.role === null) {
  ElMessage({ type: "error", message: "管理员无需审核" })
  router.push({ path: "/" })
} else if (userinfo.role.match(/\/roles\/(\d+)\/$/)[1] != "2") {
  ElMessage({ type: "error", message: "您非审计用户，无法对音频进行审核" })
  router.push({ path: "/" })
}

// 当前用户角色符合

/** 未审核音频列表 */
const noCheckAudioList = ref<AudioData[]>([])

/** 音频对应的情感 */
const leftEmotionMap = ref<string[]>([])
const rightEmotionMap = ref<string[]>([])

/** 各音乐播放器及其画布 */
const player1 = ref(null)
const canvas1 = ref(null)
const player2 = ref(null)
const canvas2 = ref(null)
const player3 = ref(null)
const canvas3 = ref(null)

/** 音频情感图表相关 */
const timeList = ref<string[]>([]) // 图表横坐标
const leftOption = ref({
  title: {
    subtext: "*每个情感表示为当前时间节点至10秒后该音频片段的情感识别结果",
    left: "right",
    subtextStyle: {
      fontSize: 12,
      fontWeight: "normal",
      color: "red"
    }
  },
  xAxis: {
    type: "category",
    data: timeList,
    axisLine: {
      show: true // 显示x轴线
    },
    axisTick: {
      show: false // 隐藏x轴刻度
    },
    splitLine: {
      show: true // 显示网格线
    }
  },
  yAxis: {
    type: "category",
    data: ["消极", "中立", "积极"],
    axisLine: { show: true },
    axisTick: { show: false },
    splitLine: { show: true }
  },
  tooltip: {
    trigger: "axis",
    formatter: function (params) {
      const xValue = params[0].axisValue
      const yValue = params[0].data
      return `情感：${yValue}<br>时间：${xValue}`
    }
  },
  series: [
    {
      type: "line",
      data: leftEmotionMap
    }
  ]
})
const rightOption = ref({
  title: {
    subtext: "*每个情感表示为当前时间节点至10秒后该音频片段的情感识别结果",
    left: "right",
    subtextStyle: {
      fontSize: 12,
      fontWeight: "normal",
      color: "red"
    }
  },
  xAxis: {
    type: "category",
    data: timeList,
    axisLine: { show: true },
    axisTick: { show: false },
    splitLine: { show: true }
  },
  yAxis: {
    type: "category",
    data: ["消极", "中立", "积极"],
    axisLine: { show: true },
    axisTick: { show: false },
    splitLine: { show: true }
  },
  tooltip: {
    trigger: "axis",
    formatter: function (params) {
      const xValue = params[0].axisValue
      const yValue = params[0].data
      return `情感：${yValue}<br>时间：${xValue}`
    }
  },
  series: [
    {
      type: "line",
      data: rightEmotionMap
    }
  ]
})

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
const isHave = async () => {
  if (noCheckAudioList.value.length == 0) {
    ElMessageBox.alert("音频全部审核完成，确认后将跳转首页。", "提示", {
      confirmButtonText: "OK",
      callback: () => {
        router.push({ path: "/" })
      }
    })
  } else {
    nowAudioStore.noCheckAudio = noCheckAudioList.value[0]
    // 合成音频后端 url
    getAudioUrl()
    // 设置音乐播放器
    setPlayer()
    // 请求音频情感
    getEmotion()
  }
}

/** 合成音频后端 url */
const getAudioUrl = () => {
  const baseUrl = "http://127.0.0.1:8000/get-audio/?path="
  nowAudioStore.oriAudioUrl = baseUrl + nowAudioStore.noCheckAudio.orig_file_path
  nowAudioStore.leftAudioUrl = baseUrl + nowAudioStore.noCheckAudio.left_file_path
  nowAudioStore.rightAudioUrl = baseUrl + nowAudioStore.noCheckAudio.right_file_path
}

/** 请求情感结果 */
const getEmotion = async () => {
  try {
    const emotionDatas = await getEmotionForAudioApi(nowAudioStore.noCheckAudio.url.match(/\/audio\/(\d+)\/$/)[1])
    const emotionData = emotionDatas[0]
    nowAudioStore.frameNum = emotionData.frame_num
    nowAudioStore.leftEmotion = emotionData.left_emotions
    nowAudioStore.rightEmotion = emotionData.right_emotions
    // 生成时间列表
    generateTimeList()
    // 映射情感
    mapEmotion()
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
    src: nowAudioStore.oriAudioUrl,
    canvWidth: 600,
    canvHeight: 120,
    lineColor: ["#FFF", "rgb(0,255,127)", "#00f"]
  })
  useAVLine(player2, canvas2, {
    src: nowAudioStore.leftAudioUrl,
    canvWidth: 600,
    canvHeight: 120,
    lineColor: ["#FFF", "rgb(0,255,127)", "#00f"]
  })
  useAVLine(player3, canvas3, {
    src: nowAudioStore.rightAudioUrl,
    canvWidth: 600,
    canvHeight: 120,
    lineColor: ["#FFF", "rgb(0,255,127)", "#00f"]
  })
}

/** 根据情感长度生成时间列表 */
const generateTimeList = () => {
  if (nowAudioStore.leftEmotion) {
    const secondsList = nowAudioStore.leftEmotion.map((value, index) => {
      const timeInSeconds = 2.5 * index
      return timeInSeconds
    })

    timeList.value = secondsList.map((seconds) => {
      const minutes = Math.floor(seconds / 60)
      const remainingSeconds = seconds % 60
      return minutes > 0 ? `${minutes}分${remainingSeconds}秒` : `${remainingSeconds}秒`
    })
  }
}

/** 根据情感数值做映射 */
const mapEmotion = () => {
  if (nowAudioStore.leftEmotion) {
    leftEmotionMap.value = nowAudioStore.leftEmotion.map((value) => {
      switch (value) {
        case 0:
          return "积极"
        case 1:
          return "中立"
        case 2:
          return "消极"
      }
    })
  }
  if (nowAudioStore.rightEmotion) {
    rightEmotionMap.value = nowAudioStore.rightEmotion.map((value) => {
      switch (value) {
        case 0:
          return "积极"
        case 1:
          return "中立"
        case 2:
          return "消极"
      }
    })
  }
}

/** 审阅完成的统一操作 */
const completeChecked = async () => {
  try {
    loading.value = true
    // 音频 checked 变更
    const id = Number(nowAudioStore.noCheckAudio.url.match(/\/audio\/(\d+)\/$/)[1])
    await updateAudioCheckedApi(id)
    // 用户审查数变更
    const userid = Number(userinfo.url.match(/\/users\/(\d+)\/$/)[1])
    const check_num = Number(userinfo.check_num) + 1
    await updateUserApi(userid, { check_num: check_num })
    loading.value = false
  } catch (error) {
    ElMessageBox.alert("审阅结果提交失败，确认后将跳转首页。", "提示", {
      confirmButtonText: "OK",
      callback: () => {
        router.push({ path: "/" })
      }
    })
  }
}

/** 该音频项通过检查 */
const passChecked = async () => {
  await completeChecked()
  // 刷新当前页面自动进入下一条音频审查
  getNoCheckAudio()
}

/** 选择剪辑音频 */
const cutAudio = async () => {
  await completeChecked()
  // 进入音频剪辑页面
  router.push({ path: "/checkaudio/cut" })
}

// 在页面加载前调用的方法
onBeforeMount(() => {
  getNoCheckAudio() // 获取未审核音频列表
})
</script>

<template>
  <div class="app-container">
    <el-card shadow="never">
      <el-divider content-position="left">原始音频</el-divider>
      <audio class="audio-player" ref="player1" crossorigin="anonymous" :src="nowAudioStore.oriAudioUrl" controls />
      <div class="audio-canvas-layout"><canvas class="audio-canvas" ref="canvas1" /></div>
    </el-card>
    <el-card shadow="never">
      <el-divider content-position="left">左声道音频</el-divider>
      <audio class="audio-player" ref="player2" crossorigin="anonymous" :src="nowAudioStore.leftAudioUrl" controls />
      <v-chart class="chart" :option="leftOption" autoresize />
      <div class="audio-canvas-layout"><canvas class="audio-canvas" ref="canvas2" /></div>
    </el-card>
    <el-card shadow="never">
      <el-divider content-position="left">右声道音频</el-divider>
      <audio class="audio-player" ref="player3" crossorigin="anonymous" :src="nowAudioStore.rightAudioUrl" controls />
      <v-chart class="chart" :option="rightOption" autoresize />
      <div class="audio-canvas-layout"><canvas class="audio-canvas" ref="canvas3" /></div>
    </el-card>
    <el-card shadow="never">
      <el-row>
        <el-col :span="8">
          <el-button :loading="loading" type="primary" size="large" @click.prevent="cutAudio">剪辑音频片段</el-button>
        </el-col>
        <el-col :span="8" />
        <el-col :span="8">
          <el-button :loading="loading" type="primary" size="large" @click.prevent="passChecked">通过</el-button>
        </el-col>
      </el-row>
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
  margin-top: -20px;

  .audio-canvas {
    // 设置canvas样式，可以根据需要进行调整
    border: 1px solid #ccc;
  }
}

.chart {
  width: 100%;
  height: 30vh;
  margin-bottom: -50px;
}

.el-col {
  display: grid;
  margin-bottom: 10px;
}
</style>
