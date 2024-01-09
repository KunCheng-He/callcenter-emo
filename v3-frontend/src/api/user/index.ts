import { request } from "@/utils/service"
import type * as User from "./types/user"

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
