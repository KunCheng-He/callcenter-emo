export interface UserRequestData {
  email: string
  username: string
  role: string
  password: string
}

export interface UserData {
  url: string
  email: string
  username: string
  role: string
  password: string
  is_superuser: Boolean
  is_staff: Boolean
  is_active: Boolean
  last_login: string
  date_joined: string
}

export type UserResponseData = Array<UserData>

export type UpdateUserData = { check_num: number; cut_num: number }
