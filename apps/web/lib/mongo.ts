// One MongoDB client for the website's server code (sign-in and contact messages).
// It connects lazily on first use, so builds without MONGODB_URI still succeed.
import { MongoClient } from 'mongodb'

export const mongoClient = new MongoClient(process.env.MONGODB_URI || 'mongodb://127.0.0.1:27017')

export const mongoDb = () => mongoClient.db(process.env.MONGODB_DB || 'uniaiverse')
