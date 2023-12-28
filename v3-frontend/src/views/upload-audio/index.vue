<script lang="ts" setup>
import { ref } from "vue"

defineOptions({
  name: "UploadAudio"
})

const loading = ref<boolean>(false)
</script>

<template>
  <div class="app-container">
    <el-card v-loading="loading" shadow="never">
      <p>test</p>
    </el-card>
  </div>
</template>

<style lang="scss" scoped></style>
