import PouchDB from 'pouchdb'
import PouchDBFind from 'pouchdb-find'


PouchDB.plugin(PouchDBFind)

// Database setup
export const db = new PouchDB('pdfgen')

// Initialize database with indexes
export async function initializeDB() {
  try {
    // Create indexes for email lookups
    await db.createIndex({
      index: { fields: ['email'] }
    })
    console.log('Database initialized with indexes')
  } catch (error) {
    console.error('Error initializing database:', error)
  }
}

    

// User type definition
export interface User {
  _id?: string
  email: string
  password: string
  name: string
  createdAt: Date,
  displayName: string,
  firstName: string,
  lastName: string,
  profilePhoto: string,
  provider: string
}

// Initialize the database on server startup
initializeDB()