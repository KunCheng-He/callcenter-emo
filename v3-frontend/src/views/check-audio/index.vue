<script setup lang="ts">
import { ref, onBeforeMount } from "vue"
import { ElMessageBox } from "element-plus"
import { AVWaveform } from "vue-audio-visual"
import { useRouter } from "vue-router"
import { getUserInfo } from "@/utils/cache/cookies"
import { type AudioData } from "@/api/audio/types/audio"
import { getNOCheckAudioApi } from "@/api/audio"
import { getEmotionForAudioApi } from "@/api/emotion"

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

/** 当前未审核音频 */
const noCheckAudio = ref<AudioData | null>(null)

/** 所有音频请求后端url */
const oriAudioUrl = ref<string>("")
const leftAudioUrl = ref<string>("")
const rightAudioUrl = ref<string>("")

/** 音频对应的情感 */
const frameNum = ref<number>(0)
const leftEmotion = ref<number[] | null>(null)
const rightEmotion = ref<number[] | null>(null)

const flag = ref<boolean>(false)

const changeflag = () => {
  flag.value = !flag.value
}

/** 获取未审核音频列表 */
const getNoCheckAudio = async () => {
  try {
    noCheckAudioList.value = await getNOCheckAudioApi()
    isHave() // 判断是否全部审核完成
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
    noCheckAudio.value = noCheckAudioList.value[0]
    // 合成音频后端 url
    getAudioUrl()
    // 请求音频情感
    getEmotion()
  }
}

/** 合成音频后端 url */
const getAudioUrl = () => {
  const baseUrl = "http://127.0.0.1:8000/get-audio/?path="
  oriAudioUrl.value = baseUrl + noCheckAudio.value.orig_file_path
  leftAudioUrl.value = baseUrl + noCheckAudio.value.left_file_path
  rightAudioUrl.value = baseUrl + noCheckAudio.value.right_file_path
}

/** 请求情感结果 */
const getEmotion = async () => {
  try {
    const emotionDatas = await getEmotionForAudioApi(noCheckAudio.value.url.match(/\/audio\/(\d+)\/$/)[1])
    const emotionData = emotionDatas[0]
    frameNum.value = emotionData.frame_num
    leftEmotion.value = emotionData.left_emotions
    rightEmotion.value = emotionData.right_emotions
  } catch (error) {
    ElMessageBox.alert("情感结果请求失败，确认后将跳转首页。", "提示", {
      confirmButtonText: "OK",
      callback: () => {
        router.push({ path: "/" })
      }
    })
  }
}

// 在页面加载前调用的方法
onBeforeMount(() => {
  getNoCheckAudio() // 获取未审核音频列表
})
</script>

<template>
  <div class="app-container">
    <el-card v-loading="loading" shadow="never">
      <div class="common-layout">
        <el-container>
          <el-header>
            <h1>音频审计</h1>
          </el-header>
          <el-main>
            <el-divider content-position="left">原始音频</el-divider>
            <AVWaveform v-if="flag" :src="oriAudioUrl" />
            <p v-else>false没有渲染</p>
            <el-button type="primary" @click.prevent="changeflag"
              >Click the button to perform a second rendering</el-button
            >
          </el-main>
        </el-container>
      </div>
    </el-card>
  </div>
</template>

<style lang="scss" scoped></style>
