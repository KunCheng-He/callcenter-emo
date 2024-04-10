<script lang="ts" setup>
import { ref } from "vue"
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

interface SearchResult {
  fileName: string
  kefuName: string
  time: string
  userScore: number
  serviceScore: number
}

const searchForm = ref({
  username: "",
  startTime: "",
  endTime: ""
})

const userList = ref([
  { id: "1", username: "kefu0" },
  { id: "2", username: "kefu1" },
  { id: "3", username: "kefu2" }
])

const searchResult = ref<SearchResult[]>([])
const searched = ref(false)

const handleSearch = () => {
  // 根据搜索条件进行搜索，这里暂时假设直接从服务器获取搜索结果
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

defineOptions({
  name: "QueryChecked"
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
            <el-option v-for="user in userList" :key="user.id" :label="user.username" :value="user.id" />
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
      <div v-if="selectedRow">
        <p>文件名: {{ selectedRow.fileName }}</p>
        <p>时间: {{ selectedRow.time }}</p>
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
}

.no-result {
  text-align: center;
  padding: 20px;
}
</style>
