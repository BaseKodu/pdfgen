import Cookies from 'js-cookie'

const GUEST_COOKIE = 'is_guest_user'
const COOKIE_OPTIONS = {
  expires: 7,
  secure: process.env.NODE_ENV === 'production',
  sameSite: 'strict'
}

export const getGuestFlag = () => Cookies.get(GUEST_COOKIE) === 'true'

export const setGuestFlag = (isGuest) =>
  isGuest
    ? Cookies.set(GUEST_COOKIE, 'true', COOKIE_OPTIONS)
    : Cookies.remove(GUEST_COOKIE)
