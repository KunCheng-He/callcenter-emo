<script lang="ts" setup>
import { ref, onBeforeMount, computed } from "vue"
import {
  ElForm,
  ElFormItem,
  ElButton,
  ElCard,
  ElSelect,
  ElOption,
  ElDatePicker,
  ElTable,
  ElTableColumn,
  ElDialog,
  ElMessageBox
} from "element-plus"
import { useAVLine } from "vue-audio-visual"
import { use } from "echarts/core"
import { LineChart } from "echarts/charts"
import { TitleComponent, GridComponent, TooltipComponent } from "echarts/components"
import { CanvasRenderer } from "echarts/renderers"
import VChart from "vue-echarts"
import { getCSUserApi } from "@/api/user"
import { type UserData } from "@/api/user/types/user"
import { getReportApi } from "@/api/report"
import { ReportDataList, ReportData } from "@/api/report/types/report"

use([TitleComponent, LineChart, CanvasRenderer, GridComponent, TooltipComponent])

defineOptions({
  name: "QueryChecked"
})

const searchForm = ref({
  username: null,
  startTime: null,
  endTime: null
})

const userList = ref<UserData[]>([])

const searchResult = ref<ReportDataList[]>([])
const searched = ref(false)

const handleSearch = async () => {
  // 根据搜索条件进行搜索
  try {
    searchResult.value = await getReportApi(searchForm.value)
    searched.value = true
  } catch (error) {
    console.error("查询失败", error)
  }
}

// 弹出对话框的开关
const dialogVisible = ref(false)

// 当前选中的行数据
const selectedRow = ref<ReportData | null>(null)

// 处理每行查看详情的点击事件
const handleTableRowClick = (row: ReportData) => {
  selectedRow.value = row
  dialogVisible.value = true
  getAudioUrl() // 合成音频播放连接
  setPlayer() // 设置播放器
  generateTimeList() // 生成时间列表
  mapEmotion() // 映射情感
}

/** 关闭查看详情的提示 */
const handleClose = (done: () => void) => {
  ElMessageBox.confirm("您确定要关闭此对话框吗？")
    .then(() => {
      done()
    })
    .catch((error) => {
      // catch error
      console.log("对话框关闭发生错误：", error)
    })
}

/** 音频对应的播放地址 */
const audioOriUrl = ref("")
const audioLeftUrl = ref("")
const audioRightUrl = ref("")

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

/** 获取客服用户列表 */
const getUserList = async () => {
  try {
    userList.value = await getCSUserApi()
  } catch (error) {
    console.error("获取客服用户列表失败", error)
  }
}

// 计算大于1的数字占比
const EmotionsRatio = computed(() => {
  return (Emotions) => {
    if (!Emotions || Emotions.length === 0) {
      return 0
    }
    const total = Emotions.length
    const countAboveOne = Emotions.filter((emotion) => emotion > 1).length
    return ((countAboveOne / total) * 100).toFixed(2)
  }
})

/** 合成音频后端 url */
const getAudioUrl = () => {
  const baseUrl = "http://127.0.0.1:8000/get-audio/?path="
  audioOriUrl.value = baseUrl + selectedRow.value.orig_file_path
  audioLeftUrl.value = baseUrl + selectedRow.value.left_file_path
  audioRightUrl.value = baseUrl + selectedRow.value.right_file_path
}

/** 设置音乐播放器 */
const setPlayer = () => {
  useAVLine(player1, canvas1, {
    src: audioOriUrl.value,
    canvWidth: 600,
    canvHeight: 120,
    lineColor: ["#FFF", "rgb(0,255,127)", "#00f"]
  })
  useAVLine(player2, canvas2, {
    src: audioLeftUrl.value,
    canvWidth: 600,
    canvHeight: 120,
    lineColor: ["#FFF", "rgb(0,255,127)", "#00f"]
  })
  useAVLine(player3, canvas3, {
    src: audioRightUrl.value,
    canvWidth: 600,
    canvHeight: 120,
    lineColor: ["#FFF", "rgb(0,255,127)", "#00f"]
  })
}

/** 根据情感长度生成时间列表 */
const generateTimeList = () => {
  if (selectedRow.value.left_emotions) {
    const secondsList = selectedRow.value.left_emotions.map((value, index) => {
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
  if (selectedRow.value.left_emotions) {
    leftEmotionMap.value = selectedRow.value.left_emotions.map((value) => {
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
  if (selectedRow.value.right_emotions) {
    rightEmotionMap.value = selectedRow.value.right_emotions.map((value) => {
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

/** 下载质检报告 */
const downloadReport = () => {
  // 将 searchResult 转换为 JSON 字符串
  const jsonData = JSON.stringify(searchResult.value)
  // 创建 Blob 对象
  const blob = new Blob([jsonData], { type: "application/json" })
  // 创建下载链接
  const url = URL.createObjectURL(blob)
  // 创建一个隐藏的 <a> 元素
  const a = document.createElement("a")
  a.style.display = "none"
  a.href = url
  a.download = "report.json" // 文件名
  // 将 <a> 元素添加到 DOM 中
  document.body.appendChild(a)
  // 模拟点击下载链接
  a.click()
  // 移除 <a> 元素
  document.body.removeChild(a)
  // 释放 Blob 对象占用的 URL
  URL.revokeObjectURL(url)
}

// 在页面加载前调用的方法
onBeforeMount(() => {
  getUserList() // 获取客服角色列表
})
</script>

<template>
  <div class="app-container">
    <!-- 顶部搜索框 -->
    <el-card class="search-box">
      <h3 class="title">呼叫中心智能质检结果查询</h3>
      <el-form :model="searchForm" inline row>
        <el-form-item label="用户名">
          <el-select v-model="searchForm.username" placeholder="请选择">
            <el-option v-for="user in userList" :key="user.username" :label="user.username" :value="user.username" />
          </el-select>
        </el-form-item>
        <el-form-item label="开始时间">
          <el-date-picker v-model="searchForm.startTime" type="date" placeholder="选择日期" />
        </el-form-item>
        <el-form-item label="结束时间">
          <el-date-picker v-model="searchForm.endTime" type="date" placeholder="选择日期" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 搜索结果展示 -->
    <el-card class="search-result">
      <h3 class="title">质检查询结果</h3>
      <div v-if="searched">
        <el-button plain type="primary" class="card-download-button" @click="downloadReport">下载质检报告</el-button>
        <el-table :data="searchResult" border stripe>
          <el-table-column prop="orig_file_path" label="文件名" />
          <el-table-column prop="username" label="客服代表" />
          <el-table-column prop="upload_time" label="时间" />
          <el-table-column label="用户评分">
            <template #default="{ row }">
              {{ EmotionsRatio(row.left_emotions) }}
            </template>
          </el-table-column>
          <el-table-column label="服务评分">
            <template #default="{ row }">
              {{ EmotionsRatio(row.right_emotions) }}
            </template>
          </el-table-column>
          <el-table-column label="查看详情">
            <template #default="{ row }">
              <el-button plain @click="handleTableRowClick(row)">查看详情</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div v-else class="no-result">无</div>
    </el-card>

    <!-- 详情弹窗 -->
    <el-dialog v-model="dialogVisible" title="音频详细信息" width="1000" :before-close="handleClose">
      <div v-if="selectedRow" class="table-container">
        <el-card shadow="never">
          <el-divider content-position="left">原始音频</el-divider>
          <audio class="audio-player" ref="player1" crossorigin="anonymous" :src="audioOriUrl" controls />
          <div class="audio-canvas-layout"><canvas class="audio-canvas" ref="canvas1" /></div>
        </el-card>
        <el-card shadow="never">
          <el-divider content-position="left">左声道音频</el-divider>
          <audio class="audio-player" ref="player2" crossorigin="anonymous" :src="audioLeftUrl" controls />
          <v-chart class="chart" :option="leftOption" autoresize />
          <div class="audio-canvas-layout"><canvas class="audio-canvas" ref="canvas2" /></div>
        </el-card>
        <el-card shadow="never">
          <el-divider content-position="left">右声道音频</el-divider>
          <audio class="audio-player" ref="player3" crossorigin="anonymous" :src="audioRightUrl" controls />
          <v-chart class="chart" :option="rightOption" autoresize />
          <div class="audio-canvas-layout"><canvas class="audio-canvas" ref="canvas3" /></div>
        </el-card>
        <!-- 添加其他需要展示的信息 -->
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="dialogVisible = false">关闭</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<style lang="scss" scoped>
.title {
  font-size: 1rem;
  line-height: 1.5rem;
  --tw-text-opacity: 1;
  color: rgb(148 163 184 / var(--tw-text-opacity));
  margin-bottom: 15px;
  margin-top: -10px;
}

.search-box {
  margin-bottom: 20px;
}

.search-result {
  margin-top: 20px;
  position: relative;
}

.card-download-button {
  position: absolute;
  top: 10px; /* 调整顶部距离以适应标题栏高度 */
  right: 10px; /* 设置与右侧的距离 */
  margin-right: 15px;
  margin-bottom: 10px;
}

.chart {
  width: 100%;
  height: 30vh;
  margin-bottom: -50px;
}

.no-result {
  text-align: center;
  padding: 20px;
}
</style>
