<script setup lang="ts">
import { ref } from "vue"
import { ElMessageBox } from "element-plus"
import { useRouter } from "vue-router"
import { getUserInfo } from "@/utils/cache/cookies"

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
</script>

<template>
  <div class="app-container">
    <el-card v-loading="loading" shadow="never">
      <h1>CheckAudio</h1>
    </el-card>
  </div>
</template>

<style lang="scss" scoped></style>
