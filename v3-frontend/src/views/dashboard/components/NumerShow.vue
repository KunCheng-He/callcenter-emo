<script lang="ts" setup>
import { getCSUserApi, getCheckUserApi } from "@/api/user"
import { getAllAudioApi, getAllAudioPartApi } from "@/api/audio"
import { ref, onMounted } from "vue"

/** 客服人数 */
const csNum = ref(0)
const setCSNum = async () => {
  const list = await getCSUserApi()
  csNum.value = list.length
}

/** 审查人数 */
const checkNum = ref(0)
const setCheckNum = async () => {
  const list = await getCheckUserApi()
  checkNum.value = list.length
}

/** 音频总数 */
const audioNum = ref(0)
const setAudioNum = async () => {
  const list = await getAllAudioApi()
  audioNum.value = list.length
}

/** 剪辑音频片段总数 */
const audioPartNum = ref(0)
const setAudioPartNum = async () => {
  const list = await getAllAudioPartApi()
  audioPartNum.value = list.length
}

onMounted(() => {
  setCSNum()
  setCheckNum()
  setAudioNum()
  setAudioPartNum()
})
</script>

<template>
  <el-row :gutter="20">
    <el-col :span="6">
      <div class="show-box">
        <div class="show">
          <div>
            <h3 class="title">客服人数</h3>
            <p class="data">{{ csNum }}</p>
          </div>
          <SvgIcon class="icon" name="kefu-user" />
        </div>
      </div>
    </el-col>
    <el-col :span="6">
      <div class="show-box">
        <div class="show">
          <div>
            <h3 class="title">审查人数</h3>
            <p class="data">{{ checkNum }}</p>
          </div>
          <SvgIcon class="icon" name="check-user" />
        </div>
      </div>
    </el-col>
    <el-col :span="6">
      <div class="show-box">
        <div class="show">
          <div>
            <h3 class="title">音频总数</h3>
            <p class="data">{{ audioNum }}</p>
          </div>
          <SvgIcon class="icon" name="audio" />
        </div>
      </div>
    </el-col>
    <el-col :span="6">
      <div class="show-box">
        <div class="show">
          <div>
            <h3 class="title">剪辑总数</h3>
            <p class="data">{{ audioPartNum }}</p>
          </div>
          <SvgIcon class="icon" name="cut-audio" />
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<style lang="scss" scoped>
.show-box {
  --tw-bg-opacity: 1;
  background-color: rgb(255 255 255 / var(--tw-bg-opacity));
  border-radius: 0.375rem;
  padding: 1.5rem;
  transition-property: box-shadow;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 0.15s;
  transition-duration: 0.5s;
  margin-bottom: 20px;

  .show {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .title {
      font-size: 1rem;
      line-height: 1.5rem;
      --tw-text-opacity: 1;
      color: rgb(148 163 184 / var(--tw-text-opacity));
      margin-bottom: 0.5rem;
    }

    .data {
      font-size: 1.875rem;
      line-height: 2.25rem;
      font-weight: 600;
      --tw-text-opacity: 1;
      color: rgb(30 41 59 / var(--tw-text-opacity));
    }

    .icon {
      width: 9em;
      height: 9em;
      margin-left: 30px;
    }
  }
}
</style>
