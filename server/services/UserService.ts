import bcrypt from 'bcryptjs'
import type { User } from './db';
import { db } from './db'

// User service with auth methods
export const userService = {
  async register(userData: Omit<User, '_id' | 'createdAt'>): Promise<User | null> {
    try {
      // Check if user exists
      const existingUsers = await db.find({
        selector: { email: userData.email },
        limit: 1
      })

      if (existingUsers.docs.length > 0) {
        throw new Error('User with this email already exists')
      }

      // Hash password
      const salt = await bcrypt.genSalt(10)
      const hashedPassword = await bcrypt.hash(userData.password, salt)

      // Create user document
      const newUser = {
        email: userData.email,
        password: hashedPassword,
        name: userData.name,
        createdAt: new Date()
      }

      const response = await db.post(newUser as any)
      const createdUser = await db.get(response.id) as unknown as User
      
      // Return user without password
      const { password, ...userWithoutPassword } = createdUser
      return userWithoutPassword as any
    } catch (error) {
      console.error('Registration error:', error)
      throw error
    }
  },

  async login(email: string, password: string): Promise<Omit<User, 'password'> | null> {
    try {
      // Find user by email
      const result = await db.find({
        selector: { email },
        limit: 1
      })

      if (result.docs.length === 0) {
        throw new Error('Invalid credentials')
      }

      const user = result.docs[0] as unknown as User

      // Verify password
      const isMatch = await bcrypt.compare(password, user.password)
      if (!isMatch) {
        throw new Error('Invalid credentials')
      }

      // Return user without password
      const { password: _, ...userWithoutPassword } = user
      return userWithoutPassword
    } catch (error) {
      console.error('Login error:', error)
      throw error
    }
  },

  async getUserById(id: string): Promise<Omit<User, 'password'> | null> {
    try {
      const user = await db.get(id) as unknown as User
      if (!user) return null

      // Return user without password
      const { password, ...userWithoutPassword } = user
      return userWithoutPassword
    } catch (error) {
      console.error('Get user error:', error)
      return null
    }
  },

  async logout(): Promise<void> {
    // With PouchDB, logout is handled on the client side
    // by clearing the user state in the store
  }
}
