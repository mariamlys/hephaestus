"use client"

import { useState, useRef, useEffect } from "react"

function ChatBox({ messages, onSendMessage, isLoading }) {
  const [inputValue, setInputValue] = useState("")
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (inputValue.trim() && !isLoading) {
      onSendMessage(inputValue.trim())
      setInputValue("")
    }
  }

  const formatTime = (date) => {
    return new Date(date).toLocaleTimeString("fr-FR", {
      hour: "2-digit",
      minute: "2-digit",
    })
  }

  const quickPrompts = ["Musique pour travailler", "Playlist running", "Sons relaxants"]

  return (
    <div className="flex flex-col h-full glass rounded-2xl overflow-hidden border-gradient">
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.length === 1 && (
          <div className="flex flex-col items-center justify-center h-full text-center py-12 animate-fade-in">
            <div className="w-20 h-20 rounded-2xl bg-gradient-accent flex items-center justify-center mb-6 animate-pulse-glow">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none">
                <path d="M9 18V5l12-2v13" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                <circle cx="6" cy="18" r="3" stroke="white" strokeWidth="2" />
                <circle cx="18" cy="16" r="3" stroke="white" strokeWidth="2" />
              </svg>
            </div>
            <h2 className="text-2xl font-semibold text-gradient mb-2">Bienvenue sur MusicBot</h2>
            <p className="text-white/50 max-w-md mb-8">
              Décris ton activité, ton mood ou ce que tu veux ressentir. L'IA compose une playlist unique pour toi.
            </p>
            <div className="flex flex-wrap justify-center gap-2">
              {quickPrompts.map((prompt, i) => (
                <button
                  key={i}
                  onClick={() => onSendMessage(prompt)}
                  className="px-4 py-2 rounded-full glass hover:bg-white/10 text-sm text-white/70 hover:text-white transition-all"
                >
                  {prompt}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((message, index) => (
          <div
            key={message.id}
            className={`flex gap-4 animate-fade-in-up ${message.type === "user" ? "flex-row-reverse" : ""}`}
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            {message.type === "bot" && (
              <div className="flex-shrink-0">
                <div className="w-10 h-10 rounded-xl bg-gradient-accent flex items-center justify-center glow-sm">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                    <path
                      d="M9 18V5l12-2v13"
                      stroke="white"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                    <circle cx="6" cy="18" r="3" stroke="white" strokeWidth="2" />
                    <circle cx="18" cy="16" r="3" stroke="white" strokeWidth="2" />
                  </svg>
                </div>
              </div>
            )}

            <div className={`flex flex-col max-w-[75%] ${message.type === "user" ? "items-end" : "items-start"}`}>
              <div
                className={`px-4 py-3 rounded-2xl ${
                  message.type === "user"
                    ? "bg-gradient-primary text-white rounded-br-md"
                    : "glass text-white/90 rounded-bl-md"
                }`}
              >
                <p className="text-sm leading-relaxed">{message.content}</p>
              </div>
              <span className="text-[10px] text-white/30 mt-1.5 px-1">{formatTime(message.timestamp)}</span>
            </div>

            {message.type === "user" && (
              <div className="flex-shrink-0">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center text-sm font-semibold">
                  U
                </div>
              </div>
            )}
          </div>
        ))}

        {isLoading && (
          <div className="flex gap-4 animate-fade-in-up">
            <div className="w-10 h-10 rounded-xl bg-gradient-accent flex items-center justify-center glow-sm">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                <path d="M9 18V5l12-2v13" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                <circle cx="6" cy="18" r="3" stroke="white" strokeWidth="2" />
                <circle cx="18" cy="16" r="3" stroke="white" strokeWidth="2" />
              </svg>
            </div>
            <div className="glass px-5 py-4 rounded-2xl rounded-bl-md">
              <div className="flex items-center gap-3">
                <div className="flex gap-1.5">
                  <span
                    className="w-2 h-2 bg-indigo-400 rounded-full animate-typing"
                    style={{ animationDelay: "0s" }}
                  ></span>
                  <span
                    className="w-2 h-2 bg-purple-400 rounded-full animate-typing"
                    style={{ animationDelay: "0.2s" }}
                  ></span>
                  <span
                    className="w-2 h-2 bg-pink-400 rounded-full animate-typing"
                    style={{ animationDelay: "0.4s" }}
                  ></span>
                </div>
                <span className="text-xs text-white/40">Composition en cours...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 border-t border-white/5 bg-black/20">
        <form onSubmit={handleSubmit} className="flex gap-3">
          <div className="flex-1 relative">
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Décris ton mood ou ton activité..."
              disabled={isLoading}
              className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3.5 text-sm text-white placeholder-white/30 focus:outline-none focus:border-indigo-500/50 focus:ring-2 focus:ring-indigo-500/20 transition-all disabled:opacity-50"
            />
          </div>
          <button
            type="submit"
            disabled={!inputValue.trim() || isLoading}
            className="px-5 py-3.5 bg-gradient-primary hover:opacity-90 text-white rounded-xl transition-all disabled:opacity-30 disabled:cursor-not-allowed glow-sm"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path
                d="M22 2L11 13M22 2L15 22L11 13M22 2L2 9L11 13"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </button>
        </form>
      </div>
    </div>
  )
}

export default ChatBox
