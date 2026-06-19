'use client'

import { useState, useRef, useEffect } from 'react'
import { Send, X } from 'lucide-react'

interface Message {
  id: string
  text: string
  sender: 'user' | 'bot'
  timestamp: Date
}

const OrbiBot = () => {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: 'Hi! I\'m Orbi. How can I help you today?',
      sender: 'bot',
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async () => {
    if (!input.trim()) return

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      text: input,
      sender: 'user',
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setIsTyping(true)

    // Simulate bot response delay
    setTimeout(() => {
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Soon will be at your service',
        sender: 'bot',
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, botMessage])
      setIsTyping(false)
    }, 500)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <>
      {/* Chat Bubble */}
      <div className="fixed bottom-6 right-6 z-50">
        {isOpen && (
          <div className="absolute bottom-20 right-0 w-96 bg-white rounded-lg shadow-2xl border border-gray-200 flex flex-col h-96 animate-in fade-in slide-in-from-bottom-2 duration-300">
            {/* Header */}
            <div className="bg-gradient-to-r from-pink-500 to-pink-600 text-white p-4 rounded-t-lg flex justify-between items-center">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center">
                  <span className="text-pink-600 font-bold text-sm">O</span>
                </div>
                <span className="font-semibold">Orbi</span>
              </div>
              <button
                onClick={() => setIsOpen(false)}
                className="hover:bg-pink-700 p-1 rounded transition"
                aria-label="Close chat"
              >
                <X size={20} />
              </button>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${
                    message.sender === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  <div
                    className={`max-w-xs px-4 py-2 rounded-lg ${
                      message.sender === 'user'
                        ? 'bg-pink-500 text-white rounded-br-none'
                        : 'bg-gray-100 text-gray-800 rounded-bl-none'
                    }`}
                  >
                    <p className="text-sm">{message.text}</p>
                  </div>
                </div>
              ))}
              {isTyping && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 text-gray-800 px-4 py-2 rounded-lg rounded-bl-none">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="border-t border-gray-200 p-3 flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask me anything..."
                className="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-pink-500"
              />
              <button
                onClick={handleSendMessage}
                disabled={!input.trim()}
                className="bg-pink-500 hover:bg-pink-600 disabled:bg-gray-300 text-white p-2 rounded-lg transition"
                aria-label="Send message"
              >
                <Send size={18} />
              </button>
            </div>
          </div>
        )}

        {/* Float Button */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="bg-gradient-to-r from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700 text-white rounded-full w-14 h-14 flex items-center justify-center shadow-lg hover:shadow-xl transition transform hover:scale-110 animate-pulse"
          aria-label="Open Orbi chat"
        >
          <span className="text-2xl">💬</span>
        </button>
      </div>
    </>
  )
}

export default OrbiBot
