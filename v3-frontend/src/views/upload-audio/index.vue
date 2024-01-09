<script lang="ts" setup>
import { ref } from "vue"
import { UploadFilled } from "@element-plus/icons-vue"
import { type FormInstance, type FormRules } from "element-plus"
import { ElMessage } from "element-plus"
import { reactive, onBeforeMount } from "vue"
import { type RoleData } from "@/api/user-role/types/role"
import { getUserRoleApi } from "@/api/user-role"
import { tr } from "element-plus/es/locale/index.mjs"
import console from "console"

defineOptions({
  name: "UploadAudio"
})

const loading = ref<boolean>(false)

// 角色列表
const roleList = ref<RoleData[]>([])

/** 上传表单元素的引用 */
const uploadFormRef = ref<FormInstance | null>(null)

/** 上传表单数据 */
const uploadFormData = reactive({
  // 两个字段，file是文件类型，接收用户上传的文件，cs_user_id是字符串字段
  file: null,
  cs_user_id: ""
})

/** 表单规则校验 */
const uploadFormRules: FormRules = {
  cs_user_id: [{ required: true, message: "请选择文件所属的客服人员" }]
}

/** 上传文件逻辑 */
const handleUpload = () => {
  uploadFormRef.value?.validate(async (valid: boolean, fields) => {
    if (valid) {
      loading.value = true
      console.log("验证通过")
    } else {
      console.log("表单校验不通过", fields)
    }
  })
}

/** 覆盖默认文件上传请求，将文件给到表单对象 */
const setFile = () => {
  console.log("覆盖默认上传行为")
}

/** 超过限制时进行提示 */
const exceedProcess = () => {
  ElMessage.warning("超过文件数量限制")
}

/** 上传文件之前额外的文件类型校验 */
const beforeUpload = (file: File) => {
  const allowedExtensions = ["mp3", "zip"]
  const fileExtension = file.name.split(".").pop().toLowerCase()

  // 文件类型校验
  if (!allowedExtensions.includes(fileExtension)) {
    ElMessage.warning("文件类型只能是 mp3 或 zip")
    return false // 阻止文件上传
  }
  // 文件大小校验
  if (file.size > 1024 * 1024 * 20) {
    ElMessage.warning("文件大小不能超过 20MB")
    return false // 阻止文件上传
  }
  // 通过文件校验
  return true
}

/** 获取角色列表 */
const getCSUsers = async () => {
  try {
    roleList.value = await getUserRoleApi()
  } catch (error) {
    console.error("获取用户角色列表失败", error)
  }
}

// 在页面加载前调用的方法
onBeforeMount(() => {
  getCSUsers() // 获取客服角色列表
})
</script>

<template>
  <div class="app-container">
    <el-card v-loading="loading" shadow="never">
      <el-form ref="uploadFormRef" :model="uploadFormData" :rules="uploadFormRules" @keyup.enter="handleUpload">
        <el-form-item prop="file">
          <el-upload
            v-model="uploadFormData.file"
            class="el-upload"
            :drag="true"
            action=""
            :http-request="setFile"
            :limit="1"
            :on-exceed="exceedProcess"
            :before-upload="beforeUpload"
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">拖拽文件到此处，或 <em>点击上传</em></div>
            <template #tip>
              <div class="el-upload__tip">支持单个mp3文件或zip压缩包</div>
            </template>
          </el-upload>
        </el-form-item>
        <el-form-item prop="cs_user_id">
          <el-select v-model="uploadFormData.cs_user_id" placeholder="选择文件所属的客服人员">
            <el-option v-for="item in roleList" :key="item.url" :label="item.name" :value="item.url" />
          </el-select>
        </el-form-item>
        <el-button :loading="loading" type="primary" size="large" @click.prevent="handleUpload"
          >上传呼叫中心音频</el-button
        >
      </el-form>
    </el-card>
  </div>
</template>

<style lang="scss" scoped>
.el-form {
  width: 100%;
  padding: 20px;

  .el-form-item {
    margin-bottom: 20px;

    &:last-child {
      margin-bottom: 0;
    }

    .el-upload {
      width: 100%;
      display: block;

      .el-upload__text {
        width: 100%;
      }

      .el-upload__tip {
        margin-top: 5px;
        display: block;
        color: #999;
      }
    }

    .el-select {
      width: 100%;
    }
  }

  .el-button {
    width: 100%;
  }
}
</style>
