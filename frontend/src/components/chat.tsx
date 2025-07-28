import React, { useEffect, useRef, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
type Message = {
    role: 'user' | 'assistant';
    content: string;
};

const Chat = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const messagesEndRef = useRef<HTMLDivElement | null>(null);
    const navigate = useNavigate();

    const handleSend = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        const user_email_id = localStorage.getItem('user');
        const newMessages: Message[] = [...messages, { role: 'user', content: input }];
        setMessages(newMessages);

        try {
            const url = 'http://localhost:3000/chat/response'
            const payload = {
                "user_email_id": localStorage.getItem("user_email_id"),
                "question": input,
            }
            const response = await axios.post(url, payload, {
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json;charset=UTF-8",
                },
            });

            const data = response.data;
            const assistantMessage: Message = {
                role: 'assistant',
                content: typeof data === 'string' ? data : JSON.stringify(data),
            };
            setMessages([...newMessages, assistantMessage]);
        } catch (error) {
            console.error('Chat error:', error);
            setMessages([
                ...newMessages,
                { role: 'assistant', content: 'Error contacting server.' },
            ]);
        }

        setInput('');
    };


    const handleLogout = () => {
        localStorage.removeItem('Bearer Token');
        localStorage.removeItem('user_email_id');
        navigate('/login');
    };

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    return (
        <div className="min-h-screen bg-gray-900 text-white p-4 flex flex-col">
            <div className="flex justify-between items-center mb-4">
                <h1 className="text-xl font-bold">Chat Room</h1>
                <button
                    onClick={handleLogout}
                    className="text-sm bg-red-600 hover:bg-red-700 px-3 py-1 rounded"
                >
                    Logout
                </button>
            </div>

            <div className="flex-1 overflow-y-auto space-y-2 mb-4">
                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        className={`p-2 rounded max-w-lg whitespace-pre-wrap ${msg.role === 'user'
                            ? 'bg-blue-700 self-end ml-auto'
                            : 'bg-gray-700 self-start mr-auto'
                            }`}
                    >
                        <p className="text-xs text-gray-400 mb-1">{msg.role}</p>
                        <div className="prose prose-invert">
                            <ReactMarkdown>{msg.content}</ReactMarkdown>
                        </div>
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>

            <form onSubmit={handleSend} className="flex space-x-2">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type a message..."
                    className="flex-1 p-2 bg-gray-800 border border-gray-600 rounded"
                />
                <button
                    type="submit"
                    className="bg-blue-600 hover:bg-blue-700 px-4 rounded"
                >
                    Send
                </button>
            </form>
        </div>
    );
};

export default Chat;
