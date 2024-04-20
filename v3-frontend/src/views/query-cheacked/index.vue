<script lang="ts" setup>
import { ref, onBeforeMount } from "vue"
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
import { getCSUserApi } from "@/api/user"
import { type UserData } from "@/api/user/types/user"
import { getReportApi } from "@/api/report"
import { ReportDataList } from "@/api/report/types/report"

defineOptions({
  name: "QueryChecked"
})

const searchForm = ref({
  username: "",
  startTime: "",
  endTime: ""
})

const userList = ref<UserData[]>([])

const searchResult = ref<ReportDataList[]>([])
const searched = ref(false)

const handleSearch = () => {
  // 根据搜索条件进行搜索，这里暂时假设直接从服务器获取搜索结果
  console.log(searchForm.value)
  // 替换成您的实际搜索逻辑
  searchResult.value = [
    { fileName: "z1.mp3", kefuName: "kefu2", time: "2024-02-05", userScore: 41.33, serviceScore: 32.98 },
    { fileName: "z2.mp3", kefuName: "kefu2", time: "2024-02-05", userScore: 39.01, serviceScore: 30.45 },
    { fileName: "z3.mp3", kefuName: "kefu2", time: "2024-02-05", userScore: 46.21, serviceScore: 50.75 },
    { fileName: "hello.mp3", kefuName: "kefu2", time: "2024-02-07", userScore: 29.89, serviceScore: 36.96 }
  ]
  searched.value = true
}

// 弹出对话框的开关
const dialogVisible = ref(false)

// 当前选中的行数据
const selectedRow = ref<SearchResult | null>(null)

// 处理每行查看详情的点击事件
const handleTableRowClick = (row: SearchResult) => {
  selectedRow.value = row
  dialogVisible.value = true
}

const handleClose = (done: () => void) => {
  ElMessageBox.confirm("您确定要关闭此对话框吗？")
    .then(() => {
      done()
    })
    .catch(() => {
      // catch error
    })
}

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
      data: ["消极", "中立", "积极"]
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
      data: ["消极", "中立", "积极"]
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
            <el-option v-for="user in userList" :key="user.url" :label="user.username" :value="user.url" />
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
        <el-button plain class="card-download-button">下载质检报告</el-button>
        <el-table :data="searchResult" border stripe>
          <el-table-column prop="fileName" label="文件名" />
          <el-table-column prop="kefuName" label="客服代表" />
          <el-table-column prop="time" label="时间" />
          <el-table-column prop="userScore" label="用户评分" />
          <el-table-column prop="serviceScore" label="服务评分" />
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
    <el-dialog v-model="dialogVisible" title="音频详细信息" width="500" :before-close="handleClose">
      <div v-if="selectedRow" class="table-container">
        <el-card shadow="never">
          <el-divider content-position="left">原始音频</el-divider>
          <audio
            class="audio-player"
            ref="player1"
            crossorigin="anonymous"
            src="http://127.0.0.1:8000/get-audio/?path=/upload_files/2024/02/05/test2_unzip/z1.mp3"
            controls
          />
          <div class="audio-canvas-layout"><canvas class="audio-canvas" ref="canvas1" /></div>
        </el-card>
        <el-card shadow="never">
          <el-divider content-position="left">左声道音频</el-divider>
          <audio
            class="audio-player"
            ref="player2"
            crossorigin="anonymous"
            src="http://127.0.0.1:8000/get-audio/?path=/upload_files/2024/02/05/test2_unzip/z1_left.wav"
            controls
          />
          <v-chart class="chart" :option="leftOption" autoresize />
          <div class="audio-canvas-layout"><canvas class="audio-canvas" ref="canvas2" /></div>
        </el-card>
        <el-card shadow="never">
          <el-divider content-position="left">右声道音频</el-divider>
          <audio
            class="audio-player"
            ref="player3"
            crossorigin="anonymous"
            src="http://127.0.0.1:8000/get-audio/?path=/upload_files/2024/02/05/test2_unzip/z1_right.wav"
            controls
          />
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

.no-result {
  text-align: center;
  padding: 20px;
}
</style>
