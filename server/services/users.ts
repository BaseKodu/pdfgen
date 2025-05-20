import prisma from '../lib/prisma'
import bcrypt from 'bcryptjs'

// User data type for registration
export interface UserRegistrationData {
  email: string
  password: string
  name: string
}

// User data type for login
export interface UserLoginData {
  email: string
  password: string
}

export const userService = {
  async register(userData: UserRegistrationData) {
    try {
      // Check if user exists
      const existingUser = await prisma.user.findUnique({
        where: { email: userData.email }
      })

      if (existingUser) {
        throw new Error('User with this email already exists')
      }

      // Hash password
      const salt = await bcrypt.genSalt(10)
      const hashedPassword = await bcrypt.hash(userData.password, salt)

      // Create user
      const user = await prisma.user.create({
        data: {
          email: userData.email,
          password: hashedPassword,
          name: userData.name
        }
      })

      // Return user without password
      const { password, ...userWithoutPassword } = user
      return userWithoutPassword
    } catch (error) {
      console.error('Registration error:', error)
      throw error
    }
  },

  async login(loginData: UserLoginData) {
    try {
      // Find user by email
      const user = await prisma.user.findUnique({
        where: { email: loginData.email }
      })

      if (!user) {
        throw new Error('Invalid credentials')
      }

      // Verify password
      const isMatch = await bcrypt.compare(loginData.password, user.password)
      if (!isMatch) {
        throw new Error('Invalid credentials')
      }

      // Return user without password
      const { password, ...userWithoutPassword } = user
      return userWithoutPassword
    } catch (error) {
      console.error('Login error:', error)
      throw error
    }
  },

  async getUserById(id: number) {
    try {
      const user = await prisma.user.findUnique({
        where: { id }
      })

      if (!user) {
        return null
      }

      // Return user without password
      const { password, ...userWithoutPassword } = user
      return userWithoutPassword
    } catch (error) {
      console.error('Get user error:', error)
      return null
    }
  }
}