<script lang="ts" setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { UploadFilled } from "@element-plus/icons-vue"
import { type FormInstance, type FormRules } from "element-plus"
import { ElMessage } from "element-plus"
import { reactive } from "vue"
import { uploadApi } from "@/api/upload-audio"

defineOptions({
  name: "UploadModel"
})

const router = useRouter()

const loading = ref<boolean>(false)

/** 上传表单元素的引用 */
const uploadFormRef = ref<FormInstance | null>(null)

/** 上传表单数据 */
const uploadFormData = reactive({
  // 两个字段，file是文件类型，接收用户上传的文件，model_id是字符串字段
  file: null,
  model_id: ""
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
      try {
        const formdata = new FormData()
        formdata.append("cs_user_id", uploadFormData.cs_user_id)
        formdata.append("file", uploadFormData.file)
        const response = await uploadApi(formdata)
        console.log(response)
        router.push({ path: "/" })
        ElMessage.success("上传成功")
      } catch (error) {
        console.log("上传失败", error)
        ElMessage.error("上传失败")
      }
      loading.value = false
    } else {
      console.log("表单校验不通过", fields)
    }
  })
}

/** 覆盖默认文件上传请求，将文件给到表单对象 */
const setFile = (params) => {
  uploadFormData.file = params.file
}

/** 超过限制时进行提示 */
const exceedProcess = () => {
  ElMessage.warning("超过文件数量限制")
}

/** 上传文件之前额外的文件类型校验 */
const beforeUpload = (file: File) => {
  const allowedExtensions = ["pth",]
  const fileExtension = file.name.split(".").pop().toLowerCase()

  // 文件类型校验
  if (!allowedExtensions.includes(fileExtension)) {
    ElMessage.warning("上传的模型参数文件仅支持 .pth 格式")
    return false // 阻止文件上传
  }
  // 通过文件校验
  return true
}
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
              <div class="el-upload__tip">上传的模型参数文件仅支持 .pth 格式</div>
            </template>
          </el-upload>
        </el-form-item>
        <el-form-item prop="model_id">
          <el-input v-model="uploadFormData.model_id" placeholder="请输入模型名称（如：CNN-20240101）" clearable />
        </el-form-item>
        <el-button :loading="loading" type="primary" size="large" @click.prevent="handleUpload"
          >上传模型参数文件</el-button
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
