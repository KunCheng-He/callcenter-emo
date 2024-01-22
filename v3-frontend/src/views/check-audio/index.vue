<script setup lang="ts">
import { ref, onBeforeMount } from "vue"
import { ElMessageBox } from "element-plus"
import { useRouter } from "vue-router"
import { getUserInfo } from "@/utils/cache/cookies"
import { type AudioData } from "@/api/audio/types/audio"
import { getNOCheckAudioApi } from "@/api/audio"

defineOptions({
  name: "CheckAudio"
})

const loading = ref<boolean>(false)

const router = useRouter()

const userinfo = getUserInfo()

// 通过 userinfo 判断用户角色是否为审计，否则弹窗提示，跳转首页
if (userinfo.role.match(/\/roles\/(\d+)\/$/)[1] != "2") {
  ElMessageBox.alert("您非审计用户，无法对音频进行审核，确认后将跳转首页。", "提示", {
    confirmButtonText: "OK",
    callback: () => {
      router.push({ path: "/" })
    }
  })
}

// 当前用户角色符合

/** 未审核音频列表 */
const noCheckAudioList = ref<AudioData[]>([])

/** 获取未审核音频列表 */
const getNoCheckAudio = async () => {
  try {
    noCheckAudioList.value = await getNOCheckAudioApi()
  } catch (error) {
    console.error("获取未审核音频列表失败", error)
  }
}

/** 音频已经全部审核完成则跳转到首页 */
const isHave = () => {
  if (noCheckAudioList.value.length == 0) {
    ElMessageBox.alert("音频全部审核完成，确认后将跳转首页。", "提示", {
      confirmButtonText: "OK",
      callback: () => {
        router.push({ path: "/" })
      }
    })
  } else {
    console.log("未审核音频列表不为空")
  }
}

// 在页面加载前调用的方法
onBeforeMount(() => {
  getNoCheckAudio() // 获取未审核音频列表
  isHave() // 判断是否全部审核完成
})
</script>

<template>
  <div class="app-container">
    <el-card v-loading="loading" shadow="never">
      <h1>CheckAudio</h1>
    </el-card>
  </div>
</template>

<style lang="scss" scoped></style>
