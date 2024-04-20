<script lang="ts" setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { UploadFilled } from "@element-plus/icons-vue"
import { type FormInstance, type FormRules } from "element-plus"
import { ElMessage } from "element-plus"
import { reactive, onBeforeMount } from "vue"
import { type UserData } from "@/api/user/types/user"
import { getCSUserApi } from "@/api/user"
import { uploadApi } from "@/api/upload-audio"
import { getUserInfo } from "@/utils/cache/cookies"
import { getSERModelApi } from "@/api/upload-model"
import { SERModelResponseData } from "@/api/upload-model/types/sermodel"

defineOptions({
  name: "UploadAudio"
})

const router = useRouter()

const loading = ref<boolean>(false)

const userinfo = getUserInfo()

// 角色列表
const csUserList = ref<UserData[]>([])

// 模型列表
const modelList = ref<SERModelResponseData[]>([])

/** 上传表单元素的引用 */
const uploadFormRef = ref<FormInstance | null>(null)

/** 只有管理员可以上传音频 */
if (userinfo.role !== null) {
  ElMessage({ type: "warning", message: "上传呼叫中心业务音频请联系管理员" })
  router.push({ path: "/" })
}

/** 上传表单数据 */
const uploadFormData = reactive({
  // 两个字段，file是文件类型，接收用户上传的文件，cs_user_id是字符串字段
  file: null,
  cs_user_id: "",
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

/** 获取客服用户列表 */
const getCSUsers = async () => {
  try {
    csUserList.value = await getCSUserApi()
  } catch (error) {
    console.error("获取客服用户列表失败", error)
  }
}

/** 获取模型列表 */
const getModels = async () => {
  try {
    modelList.value = await getSERModelApi()
  } catch (error) {
    console.error("获取模型列表失败", error)
  }
}

// 在页面加载前调用的方法
onBeforeMount(() => {
  getCSUsers() // 获取客服角色列表
  getModels() // 获取模型列表
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
            <el-option v-for="item in csUserList" :key="item.url" :label="item.username" :value="item.url" />
          </el-select>
        </el-form-item>
        <el-form-item prop="model_id">
          <el-select v-model="uploadFormData.model_id" placeholder="选择语音情感识别模型">
            <el-option v-for="item in modelList" :key="item.url" :label="item.name" :value="item.url" />
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
