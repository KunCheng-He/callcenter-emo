/** 统一处理 Cookie */

import CacheKey from "@/constants/cache-key"
import Cookies from "js-cookie"

export const getToken = () => {
  return Cookies.get(CacheKey.TOKEN)
}
export const setToken = (token: string) => {
  Cookies.set(CacheKey.TOKEN, token)
}
export const removeToken = () => {
  Cookies.remove(CacheKey.TOKEN)
}

/** 统一处理 登录用户的基本信息 */
// 用户信息不存在 cookies 里面
// const UserInfoKey = "userinfo"
// export const getUserInfo = () => {
//   return Cookies.get(JSON.parse(UserInfoKey))
// }
// export const setUserInfo = (token: object) => {
//   Cookies.set(UserInfoKey, JSON.stringify(token))
// }
// export const removeUserInfo = () => {
//   Cookies.remove(UserInfoKey)
// }
