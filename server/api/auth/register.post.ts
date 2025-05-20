import { userService } from "../../services/users"

export default defineEventHandler(async (event) => {
  try {
    const body = await readBody(event)
    
    // Validate request body
    if (!body.email || !body.password || !body.name) {
      return createError({
        statusCode: 400,
        statusMessage: 'Missing required fields'
      })
    }
    
    const user = await userService.register({
      email: body.email,
      password: body.password,
      name: body.name
    })
    
    return user
  } catch (error: any) {
    return createError({
      statusCode: 400,
      statusMessage: error.message
    })
  }
})

