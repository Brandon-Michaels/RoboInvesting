package com.example.chatbot;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

@Service
public class ChatService {

    private final WebClient webClient;

    @Value("${openai.api.key}")
    private String openAiApiKey;

    public ChatService(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder.baseUrl("https://api.openai.com/v1").build();
    }

    public String getChatReply(String message) {
        try {
            OpenAIRequest payload = new OpenAIRequest(
                "gpt-3.5-turbo",
                new Message[] {
                    new Message("system", "You are a helpful assistant in the sector of finance and investments."),
                    new Message("user", message)
                }
            );

            String response = webClient.post()
                .uri("/chat/completions")
                .header("Authorization", "Bearer " + openAiApiKey)
                .header("Content-Type", "application/json")
                .bodyValue(payload)
                .retrieve()
                .bodyToMono(String.class)
                .block();

            return response;
        } catch (Exception e) {
            return "Error: " + e.getMessage();
        }
    }

    public static class OpenAIRequest {
        private String model;
        private Message[] messages;

        public OpenAIRequest(String model, Message[] messages) {
            this.model = model;
            this.messages = messages;
        }

        public String getModel() {
            return model;
        }

        public Message[] getMessages() {
            return messages;
        }
    }

    public static class Message {
        private String role;
        private String content;

        public Message(String role, String content) {
            this.role = role;
            this.content = content;
        }

        public String getRole() {
            return role;
        }

        public String getContent() {
            return content;
        }
    }
}
