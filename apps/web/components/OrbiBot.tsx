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
          <div className="absolute bottom-20 right-0 w-[calc(100vw-3rem)] sm:w-96 bg-[#0b1020] rounded-2xl shadow-2xl border border-white/10 overflow-hidden flex flex-col h-96 animate-in fade-in slide-in-from-bottom-2 duration-300">
            {/* Header */}
            <div className="bg-deck border-b border-white/10 text-white p-4 flex justify-between items-center">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-amber-300 rounded-full flex items-center justify-center">
                  <span className="text-slate-900 font-bold text-sm">O</span>
                </div>
                <span className="font-semibold">Orbi</span>
              </div>
              <button
                onClick={() => setIsOpen(false)}
                className="hover:bg-white/10 p-1 rounded transition"
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
                        ? 'bg-amber-300 text-slate-900 rounded-br-none'
                        : 'bg-white/10 text-white/85 rounded-bl-none'
                    }`}
                  >
                    <p className="text-sm">{message.text}</p>
                  </div>
                </div>
              ))}
              {isTyping && (
                <div className="flex justify-start">
                  <div className="bg-white/10 text-white/85 px-4 py-2 rounded-lg rounded-bl-none">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-white/40 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-white/40 rounded-full animate-bounce delay-100"></div>
                      <div className="w-2 h-2 bg-white/40 rounded-full animate-bounce delay-200"></div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="border-t border-white/10 p-3 flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask me anything..."
                className="flex-1 border border-white/10 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-amber-300/60"
              />
              <button
                onClick={handleSendMessage}
                disabled={!input.trim()}
                className="bg-amber-300 hover:bg-amber-200 disabled:opacity-40 text-slate-900 p-2 rounded-lg transition"
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
          className="bg-amber-300 hover:bg-amber-200 text-slate-900 rounded-full ring-1 ring-amber-200/40 w-14 h-14 flex items-center justify-center shadow-lg hover:shadow-xl transition transform hover:scale-110 animate-pulse"
          aria-label="Open Orbi chat"
        >
          <span className="text-2xl">💬</span>
        </button>
      </div>
    </>
  )
}

export default OrbiBot
