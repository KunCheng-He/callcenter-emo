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
  ElDialog
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
  { id: "1", username: "User1" },
  { id: "2", username: "User2" }
])

const searchResult = ref<SearchResult[]>([])
const searched = ref(false)

const handleSearch = () => {
  // 根据搜索条件进行搜索，这里暂时假设直接从服务器获取搜索结果
  // 替换成您的实际搜索逻辑
  searchResult.value = [
    { fileName: "File1", kefuName: "kefu1", time: "2024-04-10", userScore: 90, serviceScore: 85 },
    { fileName: "File2", kefuName: "kefu2", time: "2024-04-09", userScore: 95, serviceScore: 88 }
  ]
  searched.value = true
}

const showDetail = () => {
  // 点击查看详情按钮时展示详情弹窗
  detailDialogVisible.value = true
}

const detailDialogVisible = ref(false)

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
              <el-button type="text" @click="showDetail(row)">查看详情</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div v-else class="no-result">无</div>
    </el-card>

    <!-- 详情弹窗 -->
    <el-dialog v-model:visible="detailDialogVisible" title="详情信息">
      <!-- 这里放置详情信息的展示内容 -->
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
