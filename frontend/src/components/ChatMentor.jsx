import React, { useState, useRef, useEffect } from 'react';
import { 
  MessageSquareCode, 
  Send, 
  Sparkles, 
  Bot, 
  User, 
  Globe, 
  BookOpen, 
  ExternalLink, 
  RefreshCw,
  Key,
  Copy,
  Check
} from 'lucide-react';
import { sendChatMessage } from '../services/api';

const QUICK_PROMPTS = [
  'What is the difference between BFS and DFS in graph traversal?',
  'Explain ACID properties in relational databases with examples',
  'What are the most common questions for TCS Digital technical round?',
  'How can a student improve campus placement chances with 1 backlog?',
  'Explain CAP theorem in distributed systems'
];

export default function ChatMentor() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      text: 'Hello! I am your **CampusNova AI Placement & Technical Interview Mentor**.\n\nAsk me anything about Data Structures & Algorithms, System Design, Core CS concepts, or campus placement strategies. I search our verified interview knowledge bank first and fall back to live web search when necessary!',
      source: 'system',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [customKey, setCustomKey] = useState('');
  const [showKeyInput, setShowKeyInput] = useState(false);
  const [copiedIdx, setCopiedIdx] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (queryText) => {
    const textToSend = queryText || input;
    if (!textToSend.trim() || loading) return;

    const userMessage = {
      role: 'user',
      text: textToSend.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const res = await sendChatMessage(textToSend.trim(), customKey.trim() || null);
      const assistantMessage = {
        role: 'assistant',
        text: res.answer,
        source: res.source, // 'Knowledge base' or 'Web'
        category: res.category,
        roleDomain: res.role,
        webLinks: res.web_links || [],
        confidence: res.confidence,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          text: `⚠️ Error contacting AI Mentor: ${err.message}. Please check your backend connection or configure a Groq API key.`,
          source: 'error',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const copyAnswer = (text, idx) => {
    navigator.clipboard.writeText(text);
    setCopiedIdx(idx);
    setTimeout(() => setCopiedIdx(null), 2000);
  };

  return (
    <div className="py-6 max-w-4xl mx-auto space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-mono mb-2">
            <MessageSquareCode className="w-3.5 h-3.5" />
            <span>Feature 7: Hybrid RAG + Live Web Placement Mentor</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
            AI Placement & Technical Interview Mentor
          </h1>
          <p className="text-slate-400 text-xs sm:text-sm mt-1">
            Semantic vector retrieval against verified interview banks with automatic live web search fallback.
          </p>
        </div>

        {/* Optional Groq Key Toggle */}
        <button
          onClick={() => setShowKeyInput(!showKeyInput)}
          className="self-start sm:self-auto flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200 text-xs font-mono transition-colors"
        >
          <Key className="w-3.5 h-3.5" />
          <span>{showKeyInput ? 'Hide API Key' : 'Custom Groq Key'}</span>
        </button>
      </div>

      {/* Groq Key Input Collapsible */}
      {showKeyInput && (
        <div className="p-4 rounded-xl bg-slate-900/90 border border-slate-800 space-y-2">
          <label className="text-xs font-semibold text-slate-300 font-mono">
            Custom Groq API Key (Optional — backend already provides default key)
          </label>
          <input
            type="password"
            value={customKey}
            onChange={(e) => setCustomKey(e.target.value)}
            placeholder="gsk_..."
            className="input-field text-xs font-mono"
          />
        </div>
      )}

      {/* Quick Prompts */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-none text-xs">
        <span className="text-slate-400 font-mono whitespace-nowrap">Suggested:</span>
        {QUICK_PROMPTS.map((prompt, i) => (
          <button
            key={i}
            onClick={() => handleSend(prompt)}
            className="px-3 py-1.5 rounded-lg bg-slate-900/80 hover:bg-slate-800 text-slate-300 border border-slate-800 whitespace-nowrap transition-colors flex-shrink-0"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Chat Messages Box */}
      <div className="glass-panel p-4 sm:p-6 h-[520px] flex flex-col justify-between">
        
        <div className="overflow-y-auto space-y-4 pr-2">
          {messages.map((msg, idx) => {
            const isUser = msg.role === 'user';
            return (
              <div 
                key={idx} 
                className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}
              >
                {!isUser && (
                  <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center flex-shrink-0 text-white mt-1 shadow-md shadow-blue-500/20">
                    <Bot className="w-4 h-4" />
                  </div>
                )}

                <div className={`max-w-[85%] rounded-2xl p-4 text-xs sm:text-sm leading-relaxed ${
                  isUser 
                    ? 'bg-gradient-to-br from-blue-600 to-indigo-600 text-white rounded-tr-none shadow-md shadow-blue-500/10' 
                    : 'bg-slate-900/90 border border-slate-800 text-slate-200 rounded-tl-none space-y-3'
                }`}>
                  
                  {/* Meta Bar for Assistant */}
                  {!isUser && msg.source && msg.source !== 'system' && (
                    <div className="flex items-center justify-between gap-2 border-b border-slate-800/80 pb-2">
                      <div className="flex items-center gap-2">
                        {msg.source === 'Knowledge base' ? (
                          <span className="badge-kb">
                            <BookOpen className="w-3 h-3" />
                            <span>Knowledge base</span>
                          </span>
                        ) : msg.source === 'Web' ? (
                          <span className="badge-web">
                            <Globe className="w-3 h-3" />
                            <span>Web Search</span>
                          </span>
                        ) : null}

                        {msg.category && (
                          <span className="text-[10px] font-mono text-slate-400 bg-slate-800/80 px-2 py-0.5 rounded">
                            {msg.category}
                          </span>
                        )}
                      </div>

                      <button
                        onClick={() => copyAnswer(msg.text, idx)}
                        className="text-slate-400 hover:text-slate-200 p-1 rounded"
                        title="Copy answer"
                      >
                        {copiedIdx === idx ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                      </button>
                    </div>
                  )}

                  {/* Message Body */}
                  <div className="whitespace-pre-wrap font-sans">
                    {msg.text}
                  </div>

                  {/* Web Citation Links */}
                  {!isUser && msg.webLinks?.length > 0 && (
                    <div className="pt-2 border-t border-slate-800/80 space-y-1.5">
                      <div className="text-[11px] font-mono text-slate-400 flex items-center gap-1">
                        <Globe className="w-3 h-3 text-blue-400" />
                        <span>Sources & Citations:</span>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {msg.webLinks.map((link, lIdx) => (
                          <a
                            key={lIdx}
                            href={link.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-1 text-[11px] px-2.5 py-1 rounded-md bg-blue-500/10 hover:bg-blue-500/20 text-blue-400 border border-blue-500/20 transition-colors"
                          >
                            <span className="truncate max-w-[200px]">{link.title || link.url}</span>
                            <ExternalLink className="w-3 h-3 flex-shrink-0" />
                          </a>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Timestamp */}
                  <div className={`text-[10px] font-mono pt-1 text-right ${isUser ? 'text-blue-200' : 'text-slate-500'}`}>
                    {msg.timestamp}
                  </div>

                </div>

                {isUser && (
                  <div className="w-8 h-8 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center flex-shrink-0 text-slate-300 mt-1">
                    <User className="w-4 h-4" />
                  </div>
                )}
              </div>
            );
          })}

          {loading && (
            <div className="flex gap-3 items-center text-slate-400 text-xs">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white">
                <Bot className="w-4 h-4" />
              </div>
              <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 flex items-center gap-2 font-mono">
                <RefreshCw className="w-3.5 h-3.5 animate-spin text-blue-400" />
                <span>Searching knowledge base & synthesizing answer...</span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Bar */}
        <form 
          onSubmit={(e) => { e.preventDefault(); handleSend(); }}
          className="mt-4 pt-3 border-t border-slate-800 flex items-center gap-2"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your interview or placement question..."
            disabled={loading}
            className="input-field"
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="btn-primary py-2.5 px-4 rounded-xl flex-shrink-0"
          >
            <Send className="w-4 h-4" />
            <span className="hidden sm:inline">Ask</span>
          </button>
        </form>

      </div>
    </div>
  );
}
