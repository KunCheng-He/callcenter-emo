<script setup lang="ts">
import { ref, onBeforeMount, reactive } from "vue"
import { ElMessageBox, ElMessage } from "element-plus"
import { type FormInstance, type FormRules } from "element-plus"
import { useRouter } from "vue-router"
import { getUserInfo } from "@/utils/cache/cookies"
import { useAVLine } from "vue-audio-visual"
import { use } from "echarts/core"
import { LineChart } from "echarts/charts"
import { TitleComponent, GridComponent, TooltipComponent } from "echarts/components"
import { CanvasRenderer } from "echarts/renderers"
import VChart from "vue-echarts"
import { useNowAudioStore } from "@/store/modules/now-audio"
import { addAudioPartApi } from "@/api/audio"
import { addDingLabelApi } from "@/api/ding-label"

use([TitleComponent, LineChart, CanvasRenderer, GridComponent, TooltipComponent])

defineOptions({
  name: "CutAudio"
})

const loading = ref<boolean>(false)

const router = useRouter()

const nowAudioStore = useNowAudioStore()

const userInfo = getUserInfo()

/** 音频对应的情感 */
const leftEmotionMap = ref<string[]>([])
const rightEmotionMap = ref<string[]>([])

/** 页面当前展示的音频 */
const showChannel = ref<string>("左声道音频")
const showAudioUrl = ref<string>(nowAudioStore.leftAudioUrl)
const showEmotionMap = ref<string[]>()

/** 各音乐播放器及其画布 */
const player = ref(null)
const canvas = ref(null)

/** 音频情感图表相关 */
const timeList = ref<string[]>([]) // 图表横坐标
const showOption = ref({
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
      data: showEmotionMap
    }
  ]
})

/** 剪辑相关 */
const cutData = reactive({
  user_id: userInfo.url,
  cut_audio_path: "",
  start_time: 0.0,
  end_time: 0.0
})

/** 情感标注相关 */
const dingFormRef = ref<FormInstance | null>(null)
const dingFormData = reactive({
  audio_part_id: "",
  audio_role: "",
  emotion_label: 0,
  text: "",
  pleasure: 2.5,
  action: 2.5
})
const dingFormRules: FormRules = {
  audio_role: [{ required: true, message: "请选择当前音频片段所属的用户角色", trigger: "blur" }],
  emotion_label: [{ required: true, message: "请选择当前音频片段的情感标签", trigger: "blur" }],
  text: [{ required: true, message: "请输入当前音频片段的文本内容", trigger: "blur" }]
}

/** 设置音乐播放器 */
const setPlayer = () => {
  useAVLine(player, canvas, {
    src: showAudioUrl,
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
  showEmotionMap.value = leftEmotionMap.value
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

/** 切换音频 */
const changeChannel = () => {
  loading.value = true
  if (showChannel.value === "左声道音频") {
    ElMessage({ message: "当前成功切换到 右声道 音频", type: "success" })
    showChannel.value = "右声道音频"
    showAudioUrl.value = nowAudioStore.rightAudioUrl
    showEmotionMap.value = rightEmotionMap.value
  } else {
    ElMessage({ message: "当前成功切换到 左声道 音频", type: "success" })
    showChannel.value = "左声道音频"
    showAudioUrl.value = nowAudioStore.leftAudioUrl
    showEmotionMap.value = leftEmotionMap.value
    console.log(leftEmotionMap.value)
  }
  cutData.start_time = 0.0
  cutData.end_time = 0.0
  loading.value = false
}

/** 确定左侧剪辑时间 */
const leftTime = () => {
  cutData.start_time = player.value.currentTime
}

/** 确定右侧剪辑时间 */
const rightTime = () => {
  cutData.end_time = player.value.currentTime
}

/** 提交剪辑片段 */
const cutAudio = async () => {
  const url = new URL(showAudioUrl.value)
  const params = new URLSearchParams(url.search)
  cutData.cut_audio_path = params.get("path")
  // 剪辑片段时间合法化检测
  if (cutData.start_time > cutData.end_time) {
    ElMessage({ message: "音频片段开始时间不能大于音频片段结束时间", type: "error" })
  } else if (cutData.end_time - cutData.start_time < 1) {
    ElMessage({ message: "音频片段过短，请重新剪辑", type: "error" })
  } else if (cutData.end_time - cutData.start_time > 12) {
    ElMessage({ message: "音频片段过长，请重新剪辑", type: "error" })
  } else {
    // 剪辑片段时间合法
    dingFormRef.value?.validate(async (valid: boolean, fields) => {
      if (valid) {
        loading.value = true
        // 提交剪辑片段
        const res = await addAudioPartApi(cutData)
        // 提交标注情感
        dingFormData.audio_part_id = res.url
        await addDingLabelApi(dingFormData)
        loading.value = false
        // 复原表单
        resetForm()
        // 弹窗提示用户添加剪辑片段成功
        ElMessage({ message: "音频片段添加成功", type: "success" })
      } else {
        console.error("表单校验不通过", fields)
      }
    })
  }
}

/** 全部音频片段剪辑完成 */
const comeBack = () => {
  // 全部剪辑完成则跳转回审查页面
  router.push({ path: "/checkaudio/check" })
}

/** 复原表单 */
const resetForm = () => {
  cutData.start_time = 0.0
  cutData.end_time = 0.0
  dingFormData.audio_role = ""
  dingFormData.emotion_label = 0
  dingFormData.text = ""
  dingFormData.pleasure = 2.5
  dingFormData.action = 2.5
}

/** nowAudioStore 不存在数据则跳转 */
const validData = () => {
  if (nowAudioStore.noCheckAudio === null) {
    ElMessageBox.alert("请先审查音频，存在识别错误后，再剪辑音频片段。", "提示", {
      confirmButtonText: "OK",
      callback: () => {
        router.push({ path: "/" })
      }
    })
  }
}

// 在页面加载前调用的方法
onBeforeMount(() => {
  validData()
  mapEmotion()
  generateTimeList()
  setPlayer()
})
</script>

<template>
  <div class="app-container">
    <el-card shadow="never">
      <el-divider content-position="left">{{ showChannel }}</el-divider>
      <audio class="audio-player" ref="player" crossorigin="anonymous" :src="showAudioUrl" controls />
      <v-chart class="chart" :option="showOption" autoresize />
      <div class="audio-canvas-layout"><canvas class="audio-canvas" ref="canvas" /></div>
    </el-card>
    <el-card shadow="never">
      <el-row>
        <el-col :span="8">
          <el-button type="primary" size="large" @click.prevent="leftTime">
            片段始: {{ cutData.start_time }}
          </el-button>
        </el-col>
        <el-col :span="8">
          <el-button :loading="loading" type="primary" size="large" @click.prevent="changeChannel">切换声道</el-button>
        </el-col>
        <el-col :span="8">
          <el-button type="primary" size="large" @click.prevent="rightTime"> 片段终: {{ cutData.end_time }} </el-button>
        </el-col>
      </el-row>
    </el-card>
    <el-card shadow="never">
      <el-form ref="dingFormRef" :model="dingFormData" :rules="dingFormRules" @keyup.enter="cutAudio">
        <el-row :gutter="20">
          <el-col :span="2"><el-text class="mx-1" type="primary" size="large">角色</el-text></el-col>
          <el-col :span="10">
            <el-form-item prop="audio_role">
              <el-select v-model="dingFormData.audio_role" placeholder="选择角色">
                <el-option key="来电用户" label="来电用户" value="来电用户" />
                <el-option key="服务客服" label="服务客服" value="服务客服" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="2"><el-text class="mx-1" type="primary" size="large">离散情感</el-text></el-col>
          <el-col :span="10">
            <el-form-item prop="emotion_label">
              <el-select v-model="dingFormData.emotion_label" placeholder="选择离散情感">
                <el-option :key="0" label="积极-饱满" :value="0" />
                <el-option :key="1" label="中性-日常" :value="1" />
                <el-option :key="2" label="消极-随意" :value="2" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="2"><el-text class="mx-1" type="primary" size="large">音频文本</el-text></el-col>
          <el-col :span="22">
            <el-form-item prop="text">
              <el-input v-model.trim="dingFormData.text" :rows="2" type="textarea" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="3"
            ><el-text class="mx-1" type="primary" size="large"
              >愉悦维评分 -> {{ dingFormData.pleasure }}</el-text
            ></el-col
          >
          <el-col :span="21">
            <el-form-item prop="pleasure">
              <el-slider v-model.trim="dingFormData.pleasure" :min="0" :max="5" :step="0.1" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="3"
            ><el-text class="mx-1" type="primary" size="large">激活维评分 -> {{ dingFormData.action }}</el-text></el-col
          >
          <el-col :span="21">
            <el-form-item prop="action">
              <el-slider v-model.trim="dingFormData.action" :min="0" :max="5" :step="0.1" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="8">
            <el-button :loading="loading" type="primary" size="large" @click.prevent="comeBack"
              >完成全部片段剪辑</el-button
            >
          </el-col>
          <el-col :span="8" />
          <el-col :span="8">
            <el-button :loading="loading" type="primary" size="large" @click.prevent="cutAudio">添加音频片段</el-button>
          </el-col>
        </el-row>
      </el-form>
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
  padding-left: 10px;
  padding-right: 10px;
}

.el-text {
  padding-bottom: 20px;
}
</style>
