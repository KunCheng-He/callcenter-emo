import { request } from "@/utils/service"
import type * as Role from "./types/role"

/** 获取用户角色列表 */
export function getUserRoleApi() {
  return request<Role.UserRoleResponseData>({
    url: "/roles/",
    method: "get"
  })
}
