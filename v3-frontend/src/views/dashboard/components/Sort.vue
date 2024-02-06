<script lang="ts" setup>
import { ref, onMounted } from "vue"
import { getTopUserApi } from "@/api/user"

/** 客服业务数据 */
const csTableData = ref([])
const SetCSTabelData = async () => {
  const res = await getTopUserApi("客服", "audio_num", 10)
  const tableData = []
  for (let i = 0; i < res.length; i++) {
    const user = res[i]
    const you = user.user_emo_up + user.user_emo_down + user.user_emo_norm
    let you_score = 0
    if (you > 0) {
      you_score = ((user.user_emo_up + user.user_emo_norm) / you) * 100
    }
    const me = user.emo_up + user.emo_down + user.emo_norm
    let me_score = 0
    if (me > 0) {
      me_score = ((user.emo_up + user.emo_norm) / me) * 100
    }
    tableData.push({
      name: user.username,
      audio_num: user.audio_num,
      you_score: you_score.toFixed(2),
      me_score: me_score.toFixed(2)
    })
  }
  csTableData.value = tableData
}

/** 审计业务数据 */
const checkTableData = ref([])
const SetCheckTabelData = async () => {
  const res = await getTopUserApi("审计", "check_num", 10)
  const tableData = []
  for (let i = 0; i < res.length; i++) {
    const user = res[i]
    tableData.push({
      name: user.username,
      check_num: user.check_num,
      cut_num: user.cut_num
    })
  }
  checkTableData.value = tableData
}

onMounted(() => {
  SetCSTabelData()
  SetCheckTabelData()
})
</script>

<template>
  <div class="sort">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card shadow="never">
          <h3 class="title">客服业务统计</h3>
          <el-table :data="csTableData" stripe height="250" :highlight-current-row="true" style="width: 100%">
            <el-table-column prop="name" label="客服员" />
            <el-table-column prop="audio_num" label="业务量" />
            <el-table-column prop="you_score" label="用户评分" />
            <el-table-column prop="me_score" label="服务评分" />
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="never">
          <h3 class="title">审计业务统计</h3>
          <el-table :data="checkTableData" stripe height="250" :highlight-current-row="true" style="width: 100%">
            <el-table-column prop="name" label="审计员" />
            <el-table-column prop="check_num" label="审计量" />
            <el-table-column prop="cut_num" label="剪辑音频数量" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style lang="scss" scoped>
.el-row {
  margin-bottom: 20px;
}

.el-col {
  border-radius: 4px;
}

.title {
  font-size: 1rem;
  line-height: 1.5rem;
  --tw-text-opacity: 1;
  color: rgb(148 163 184 / var(--tw-text-opacity));
  margin-bottom: 0.5rem;
  margin-top: -5px;
}
</style>
