<script lang="ts" setup>
import { computed, ref } from "vue"
import { ElCard, ElForm, ElFormItem, ElDatePicker, ElButton } from "element-plus"
import { ExportData } from "@/api/ding-label/types/ding"
import { ExportQueryApi } from "@/api/ding-label"
import JSZip from "jszip"
import { saveAs } from "file-saver"

const exportForm = ref({
  startTime: null,
  endTime: null
})

const queryResult = ref<ExportData[]>([])
const queryed = ref(false)

const handleQuery = async () => {
  // 根据搜索条件进行查询
  try {
    queryResult.value = await ExportQueryApi(exportForm.value)
    queryed.value = true
  } catch (error) {
    console.error("查询失败", error)
  }
}

/** 重命名音频文件名 */
function renameAudio(path: string) {
  return path.replace(/\//g, "_")
}

/** 导出语料库 */
const exportData = async () => {
  // 创建一个JSZip实例
  const zip = new JSZip()
  // 添加JSON文件
  const jsonData = JSON.stringify(queryResult.value)
  zip.file("ding-info.json", jsonData)

  // 遍历音频文件并添加到ZIP中
  const baseUrl = "http://127.0.0.1:8000/get-audio/?path="
  for (const item of queryResult.value) {
    const response = await fetch(baseUrl + item.audio_path)
    const blob = await response.blob()
    zip.file(renameAudio(item.audio_path), blob) // 假设音频文件扩展名为.wav
  }

  // 生成ZIP文件并让用户下载
  zip.generateAsync({ type: "blob" }).then(function (content) {
    saveAs(content, "EmoDataset.zip")
  })
}

/** 情感标签数值映射为文本 */
const emoText = computed(() => {
  return (emo) => {
    switch (emo) {
      case 0:
        return "积极"
      case 1:
        return "中立"
      case 2:
        return "消极"
    }
  }
})

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
          <el-button type="primary" @click="handleQuery">查询</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 查询结果展示 -->
    <el-card class="search-result">
      <h3 class="title">音频片段查询结果</h3>
      <div v-if="queryed">
        <el-button plain type="primary" class="card-download-button" @click="exportData">导出语料库</el-button>
        <el-table :data="queryResult" border stripe>
          <el-table-column prop="audio_path" label="音频文件" />
          <el-table-column prop="audio_role" label="音频角色" />
          <el-table-column label="情感标签">
            <template #default="{ row }">
              {{ emoText(row.emotion_label) }}
            </template>
          </el-table-column>
          <el-table-column prop="pleasure" label="愉悦度" />
          <el-table-column prop="action" label="激活度" />
          <el-table-column prop="ding_time" label="标注时间" />
        </el-table>
      </div>
      <div v-else class="no-result">无</div>
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
