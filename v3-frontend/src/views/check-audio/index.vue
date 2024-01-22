<script setup lang="ts">
import { ref } from "vue"

defineOptions({
  name: "CheckAudio"
})

const loading = ref<boolean>(false)
</script>

<template>
  <div class="app-container">
    <el-card v-loading="loading" shadow="never">
      <h1>CheckAudio</h1>
    </el-card>
  </div>
</template>

<style lang="scss" scoped></style>
