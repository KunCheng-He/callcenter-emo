export interface LoginRequestData {
  /** admin 或 editor */
  username: string
  /** 密码 */
  password: string
}

export type LoginCodeResponseData = ApiResponseData<string>

export type LoginResponseData = {
  refresh: string
  token: string
  expire: number
  username: string
  email: string
  id: number
}

export type UserInfoResponseData = {
  date_joined: Date
  email: string
  is_active: boolean
  is_staff: boolean
  is_superuser: boolean
  last_login: Date | null
  password: string
  role?: null | string
  url: string
  username: string
  [property: string]: any
}
