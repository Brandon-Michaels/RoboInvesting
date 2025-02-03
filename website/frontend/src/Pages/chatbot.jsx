import React, { useState } from 'react';

const Chatbot = () => {
	const [messages, setMessages] = useState([]);
	const [input, setInput] = useState('');

	const handleSendMessage = async () => {
		if (!input.trim()) return;

		const newMessage = { text: input, sender: 'user' };
		setMessages([...messages, newMessage]);
		setInput('');

		// Simulating a chatbot response (Replace this with an API call to OpenAI or another model)
		setTimeout(() => {
			const botResponse = { text: `${newMessage.text}`, sender: 'bot' };
			setMessages((prevMessages) => [...prevMessages, botResponse]);
		}, 1000);
	};

	return (
		<div className="min-h-screen flex flex-col bg-gray-100 items-center justify-center p-4">
			<div className="w-full max-w-2xl bg-white shadow-lg rounded-lg p-4 flex flex-col h-[600px]">
				<div className="text-center text-xl font-bold mb-2">RoboInvestor</div>
				<div className="flex-1 overflow-y-auto p-4 space-y-2 flex flex-col">
					{messages.map((msg, index) => (
						<div
							key={index}
							className={`p-2 rounded-lg w-fit max-w-xs ${msg.sender === 'user' ? 'bg-blue-500 text-white self-end text-right ml-auto' : 'bg-gray-200 text-gray-900 self-start text-left'
								}`}
						>
							{msg.text}
						</div>
					))}
				</div>
				<div className="flex items-center gap-2 p-2 border-t">
					<input
						type="text"
						className="flex-1 p-2 border rounded-lg focus:outline-none"
						value={input}
						onChange={(e) => setInput(e.target.value)}
						onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
						placeholder="Type your message..."
					/>
					<button
						onClick={handleSendMessage}
						className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
					>
						Send
					</button>
				</div>
			</div>
		</div>
	);
};

export default Chatbot;
