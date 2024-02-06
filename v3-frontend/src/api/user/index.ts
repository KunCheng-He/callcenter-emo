import { request } from "@/utils/service"
import * as User from "./types/user"

/** 添加用户 */
export function addUserApi(data: User.UserRequestData) {
  return request<User.UserData>({
    url: "/users/",
    method: "post",
    data
  })
}

/** 获取客服用户 */
export function getCSUserApi() {
  return request<User.UserResponseData>({
    url: "/users/",
    method: "get",
    params: {
      role: "客服"
    }
  })
}

/** 获取审计用户 */
export function getCheckUserApi() {
  return request<User.UserResponseData>({
    url: "/users/",
    method: "get",
    params: {
      role: "审计"
    }
  })
}

/** 更新用户信息: 审查数 - 剪辑数 */
export function updateUserApi(id: number, data: User.UpdateUserData) {
  return request<User.UserData>({
    url: `/users/${id}/`,
    method: "patch",
    data
  })
}
