export interface UserRequestData {
  email: string
  username: string
  role: string
  password: string
}

export type CreateUserResponse = {
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
