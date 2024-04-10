<script lang="ts" setup>
import { ref } from "vue"
import { ElCard, ElForm, ElFormItem, ElDatePicker, ElButton, ElMessage } from "element-plus"

const exportForm = ref({
  startTime: "",
  endTime: ""
})

const handleExport = async () => {
  // 模拟导出功能
  try {
    // 模拟请求后端导出数据
    await new Promise((resolve) => setTimeout(resolve, 2000))

    ElMessage.success("语料库正在导出，请稍候...")
  } catch (error) {
    ElMessage.error("语料库导出失败，请重试...")
  }
}

defineOptions({
  name: "ExportAudio"
})
</script>

<template>
  <div class="app-container">
    <el-card class="export-card">
      <h3 class="title">语料库导出</h3>
      <el-form :model="exportForm" inline>
        <el-form-item label="开始时间">
          <el-date-picker v-model="exportForm.startTime" type="date" placeholder="选择开始时间" />
        </el-form-item>
        <el-form-item label="结束时间">
          <el-date-picker v-model="exportForm.endTime" type="date" placeholder="选择结束时间" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleExport">导出</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<style lang="scss" scoped>
.export-card {
  margin-top: 20px;
}

.title {
  font-size: 1rem;
  line-height: 1.5rem;
  --tw-text-opacity: 1;
  color: rgb(148 163 184 / var(--tw-text-opacity));
  margin-bottom: 15px;
  margin-top: -10px;
}

.card-title {
  position: absolute;
  top: 10px;
  left: 10px;
  font-weight: bold;
  font-size: 18px;
  color: #333;
}
</style>
