'use client'
// uniAI — the uniAIverse website assistant. Replaces OrbiBot.
// Talks to the AI Services API (/api/bot). Works with no LLM key (knowledge-base answers);
// if the API has an LLM configured the answers are rephrased, never invented.
import { useState, useRef, useEffect } from 'react'
import { Send, X } from 'lucide-react'

const API = (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000') + '/api/bot'

interface Message { id: string; text: string; sender: 'user' | 'bot'; link?: { label: string; url: string } | null; quick?: string[] }

const UniAIBot = () => {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [session, setSession] = useState<string | null>(null)
  const endRef = useRef<HTMLDivElement>(null)

  useEffect(() => { endRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [messages])
  useEffect(() => {
    if (!isOpen || messages.length) return
    fetch(`${API}/config`).then(r => r.json())
      .then(c => setMessages([{ id: 'g', text: c.greeting, sender: 'bot', quick: c.quick_replies }]))
      .catch(() => setMessages([{ id: 'g', text: "Hi, I'm uniAI 👋 Ask me about our services, courses, demos or how to book a call.", sender: 'bot' }]))
  }, [isOpen])

  const send = async (text: string) => {
    const t = text.trim(); if (!t) return
    setMessages(p => [...p, { id: Date.now() + 'u', text: t, sender: 'user' }]); setInput(''); setIsTyping(true)
    try {
      const r = await fetch(`${API}/chat`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message: t, session }) })
      const b = await r.json(); setSession(b.session)
      setMessages(p => [...p, { id: Date.now() + 'b', text: b.text, sender: 'bot', link: b.link, quick: b.quick_replies }])
    } catch {
      setMessages(p => [...p, { id: Date.now() + 'b', text: 'I could not reach the assistant service. You can still book a call at calendly.com/uniaiverse2025/30min.', sender: 'bot' }])
    } finally { setIsTyping(false) }
  }

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {isOpen && (
        <div className="absolute bottom-20 right-0 w-[22rem] sm:w-96 bg-white rounded-lg shadow-2xl border border-gray-200 flex flex-col h-[28rem]">
          <div className="bg-gradient-to-r from-teal-600 to-teal-700 text-white p-4 rounded-t-lg flex justify-between items-center">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center"><span className="text-teal-700 font-bold text-sm">u</span></div>
              <span className="font-semibold">uniAI</span>
            </div>
            <button onClick={() => setIsOpen(false)} className="hover:bg-teal-800 p-1 rounded" aria-label="Close chat"><X size={20} /></button>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.map(m => (
              <div key={m.id} className={`flex flex-col ${m.sender === 'user' ? 'items-end' : 'items-start'}`}>
                <div className={`max-w-xs px-4 py-2 rounded-lg text-sm ${m.sender === 'user' ? 'bg-teal-600 text-white rounded-br-none' : 'bg-gray-100 text-gray-800 rounded-bl-none'}`}>
                  <p>{m.text}</p>
                  {m.link && <a href={m.link.url} target="_blank" rel="noopener noreferrer" className="block mt-2 text-teal-700 underline font-medium">{m.link.label} →</a>}
                </div>
                {m.quick && m.sender === 'bot' && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {m.quick.map(q => <button key={q} onClick={() => send(q)} className="text-xs border border-teal-600 text-teal-700 rounded-full px-2 py-1 hover:bg-teal-50">{q}</button>)}
                  </div>
                )}
              </div>
            ))}
            {isTyping && <div className="bg-gray-100 text-gray-500 px-4 py-2 rounded-lg rounded-bl-none w-fit text-sm">…</div>}
            <div ref={endRef} />
          </div>
          <div className="border-t border-gray-200 p-3 flex gap-2">
            <input type="text" value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); send(input) } }}
              placeholder="Ask about services, courses, demos, booking…" className="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-teal-600" />
            <button onClick={() => send(input)} disabled={!input.trim()} className="bg-teal-600 hover:bg-teal-700 disabled:bg-gray-300 text-white p-2 rounded-lg" aria-label="Send"><Send size={18} /></button>
          </div>
        </div>
      )}
      <button onClick={() => setIsOpen(!isOpen)} className="bg-gradient-to-r from-teal-600 to-teal-700 text-white rounded-full w-14 h-14 flex items-center justify-center shadow-lg hover:scale-110 transition" aria-label="Open uniAI chat">
        <span className="text-2xl">💬</span>
      </button>
    </div>
  )
}
export default UniAIBot
