import { request } from "@/utils/service"
import type * as User from "./types/user"

/** 获取用户角色列表 */
export function addUserApi(data: User.UserRequestData) {
  return request<User.CreateUserResponse>({
    url: "/users/",
    method: "post",
    data
  })
}
