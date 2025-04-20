import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="chatbot-container" [class.active]="isOpen">
      <div class="chatbot-header" (click)="toggleChatbot()">
        <span>Chat Assistant</span>
        <span class="chatbot-icon">💬</span>
      </div>
      <div class="chatbot-content" *ngIf="isOpen">
        <div class="chat-messages">
          <div *ngFor="let message of messages" class="message" [class.user]="message.isUser">
            {{ message.text }}
          </div>
        </div>
        <div class="chat-input">
          <input 
            #chatInput
            type="text" 
            [(ngModel)]="userMessage" 
            (keyup.enter)="sendMessage()"
            placeholder="Type your message..."
          >
          <button (click)="sendMessage()" [disabled]="!userMessage.trim()">Send</button>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .chatbot-container {
      position: fixed;
      bottom: 0px;
      right: 20px;
      width: 300px;
      background: white;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      z-index: 1000;
      transition: all 0.3s ease;
    }

    .chatbot-header {
      padding: 10px 15px;
      background: #0014dc;
      color: white;
      border-radius: 8px 8px 0 0;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .chatbot-content {
      height: 0;
      overflow: hidden;
      transition: height 0.3s ease;
    }

    .chatbot-container.active .chatbot-content {
      height: 400px;
      display: flex;
      flex-direction: column;
    }

    .chat-messages {
      flex: 1;
      padding: 15px;
      overflow-y: auto;
    }

    .message {
      margin-bottom: 10px;
      padding: 8px 12px;
      border-radius: 4px;
      background: #f0f0f0;
      max-width: 80%;
    }

    .message.user {
      background: #0014dc;
      color: white;
      margin-left: auto;
    }

    .chat-input {
      padding: 10px;
      border-top: 1px solid #eee;
      display: flex;
      gap: 10px;
    }

    .chat-input input {
      flex: 1;
      padding: 8px;
      border: 1px solid #ddd;
      border-radius: 4px;
    }

    .chat-input button {
      padding: 8px 15px;
      background: #0014dc;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }

    .chat-input button:hover {
      background: #0014dc;
      opacity: 0.9;
    }
  `]
})
export class ChatbotComponent implements OnInit {
  isOpen = false;
  userMessage = '';
  messages: { text: string; isUser: boolean }[] = [];
  isLoading = false;

  constructor(private http: HttpClient) {}

  ngOnInit() {
    // Add welcome message
    this.messages.push({
      text: "Hello! I'm here to help you with the Oil & Gas Production Analytics. How can I assist you today?",
      isUser: false
    });
  }

  toggleChatbot() {
    this.isOpen = !this.isOpen;
  }

  sendMessage() {
    if (!this.userMessage.trim()) return;

    const userMessage = this.userMessage;
    this.messages.push({ text: userMessage, isUser: true });
    this.userMessage = '';
    this.isLoading = true;

    this.http.post<{ response: string }>(`${environment.apiUrl}/chatbot`, {
      message: userMessage
    }).subscribe({
      next: (data) => {
        this.messages.push({
          text: data.response,
          isUser: false
        });
      },
      error: (error) => {
        console.error('Error getting chatbot response:', error);
        this.messages.push({
          text: "Sorry, I'm having trouble connecting to the server. Please try again later.",
          isUser: false
        });
      }
    });
  }
} 