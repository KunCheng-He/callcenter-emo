<script lang="ts" setup>
import { onBeforeMount, reactive, ref } from "vue"
import { useRouter } from "vue-router"
import { type FormInstance, type FormRules } from "element-plus"
import { Message, Lock, User } from "@element-plus/icons-vue"
import { ElMessageBox, ElMessage } from "element-plus"
import ThemeSwitch from "@/components/ThemeSwitch/index.vue"
import { getUserRoleApi } from "@/api/user-role"
import { addUserApi } from "@/api/user"
import { type RoleData } from "@/api/user-role/types/role"

const router = useRouter()

// 角色列表
const roleList = ref<RoleData[]>([])

/** 注册表单元素的引用 */
const registerFormRef = ref<FormInstance | null>(null)

/** 注册按钮 Loading */
const loading = ref(false)
/** 注册表单数据 */
const registerFormData = reactive({
  email: "",
  username: "",
  role: "",
  password: ""
})
/** 注册表单校验规则 */
const registerFormRules: FormRules = {
  email: [
    { required: true, message: "请输入邮箱", trigger: "blur" },
    { type: "email", message: "请输入正确的邮箱", trigger: "blur" }
  ],
  username: [
    { required: true, message: "请输入用户名", trigger: "blur" },
    { min: 1, max: 16, message: "长度在 1 到 16 个字符", trigger: "blur" }
  ],
  role: [{ required: true, message: "请选择用户角色", trigger: "blur" }],
  password: [
    { required: true, message: "请输入密码", trigger: "blur" },
    { min: 8, max: 16, message: "长度在 8 到 16 个字符", trigger: "blur" }
  ]
}
/** 注册逻辑 */
const handleRegister = () => {
  registerFormRef.value?.validate(async (valid: boolean, fields) => {
    if (valid) {
      loading.value = true
      try {
        // console.log(registerFormData)
        await addUserApi(registerFormData)
        ElMessage({ message: "注册成功", type: "success" })
        router.push({ path: "/login" })
      } catch (error: any) {
        if (error.response.data?.email !== undefined) {
          ElMessageBox.alert(error.response.data.email[0], "错误", {
            confirmButtonText: "OK"
          })
        }
        registerFormData.email = ""
        registerFormData.password = ""
        registerFormData.username = ""
        registerFormData.role = ""
      }
      loading.value = false
    } else {
      console.error("表单校验不通过", fields)
    }
  })
}
/** 获取角色列表 */
const getUserRole = async () => {
  try {
    roleList.value = await getUserRoleApi()
  } catch (error) {
    console.error("获取用户角色列表失败", error)
  }
}

// 在页面加载前调用的方法
onBeforeMount(() => {
  getUserRole() // 获取角色列表
})
</script>

<template>
  <div class="register-container">
    <ThemeSwitch class="theme-switch" />
    <div class="register-card">
      <div class="title">
        <img src="@/assets/layouts/logo-text-2.png" />
      </div>
      <div class="content">
        <el-form
          ref="registerFormRef"
          :model="registerFormData"
          :rules="registerFormRules"
          @keyup.enter="handleRegister"
        >
          <el-form-item prop="email">
            <el-input
              v-model.trim="registerFormData.email"
              placeholder="邮箱"
              type="text"
              tabindex="1"
              :prefix-icon="Message"
              size="large"
            />
          </el-form-item>
          <el-form-item prop="username">
            <el-input
              v-model.trim="registerFormData.username"
              placeholder="用户名"
              type="text"
              tabindex="1"
              :prefix-icon="User"
              size="large"
            />
          </el-form-item>
          <el-form-item prop="role">
            <el-select v-model="registerFormData.role" placeholder="选择角色">
              <el-option v-for="item in roleList" :key="item.url" :label="item.name" :value="item.url" />
            </el-select>
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              v-model.trim="registerFormData.password"
              placeholder="密码"
              type="password"
              tabindex="2"
              :prefix-icon="Lock"
              size="large"
              show-password
            />
          </el-form-item>
          <el-button :loading="loading" type="primary" size="large" @click.prevent="handleRegister">注 册</el-button>
        </el-form>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  min-height: 100%;

  .theme-switch {
    position: fixed;
    top: 5%;
    right: 5%;
    cursor: pointer;
  }

  .register-card {
    width: 480px;
    border-radius: 20px;
    box-shadow: 0 0 10px #dcdfe6;
    background-color: #fff;
    overflow: hidden;

    .title {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 150px;

      img {
        height: 100%;
      }
    }

    .content {
      padding: 20px 50px 50px 50px;

      :deep(.el-input-group__append) {
        padding: 0;
        overflow: hidden;

        .el-image {
          width: 100px;
          height: 40px;
          border-left: 0px;
          user-select: none;
          cursor: pointer;
          text-align: center;
        }
      }

      .el-button {
        width: 100%;
        margin-top: 10px;
      }
    }
  }
}
</style>
