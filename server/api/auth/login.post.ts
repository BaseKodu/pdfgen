import { userService } from '~/server/services/users'

export default defineEventHandler(async (event) => {
  try {
    const body = await readBody(event)
    
    // Validate request body
    if (!body.email || !body.password) {
      return createError({
        statusCode: 400,
        statusMessage: 'Missing required fields'
      })
    }
    
    const user = await userService.login({
      email: body.email,
      password: body.password
    })
    
    return user
  } catch (error: any) {
    return createError({
      statusCode: 401,
      statusMessage: error.message
    })
  }
})