import { userService } from '~/server/services/users'

export default defineEventHandler(async (event) => {
  try {
    const query = getQuery(event)
    const userId = query.id
    
    if (!userId) {
      return createError({
        statusCode: 400,
        statusMessage: 'User ID is required'
      })
    }
    
    const user = await userService.getUserById(parseInt(userId.toString()))
    
    if (!user) {
      return createError({
        statusCode: 404,
        statusMessage: 'User not found'
      })
    }
    
    return user
  } catch (error: any) {
    return createError({
      statusCode: 500,
      statusMessage: error.message
    })
  }
})