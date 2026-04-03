import { Component, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ButtonModule } from 'primeng/button';
import { ToastModule } from 'primeng/toast';
import { MessageService } from 'primeng/api';

@Component({
  selector: 'app-about',
  standalone: true,
  templateUrl: './about.html',
  styleUrl: './about.css',
  imports: [
    CommonModule,
    FormsModule,
    ButtonModule,
    ToastModule
  ],
  providers: [MessageService],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class AboutComponent {
  contactName = '';
  contactEmail = '';
  contactPhone = '';
  contactMessage = '';

  constructor(private msg: MessageService) {}

  sendMessage() {
    if (
      !this.contactName ||
      !this.contactEmail ||
      !this.contactPhone ||
      !this.contactMessage
    ) {
      this.msg.add({
        severity: 'warn',
        summary: 'Missing Details',
        detail: 'Please fill all fields ⚠️'
      });
      return;
    }

    const data = {
      name: this.contactName,
      email: this.contactEmail,
      phone: this.contactPhone,
      message: this.contactMessage
    };

    fetch('http://127.0.0.1:8000/api/contact/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
      .then(res => res.json())
      .then(res => {
        if (res.success) {
          this.msg.add({
            severity: 'success',
            summary: 'Message Sent',
            detail: 'We will contact you soon'
          });

          this.contactName = '';
          this.contactEmail = '';
          this.contactPhone = '';
          this.contactMessage = '';
        } else {
          this.msg.add({
            severity: 'error',
            summary: 'Failed',
            detail: 'Message sending failed '
          });
        }
      })
      .catch(() => {
        this.msg.add({
          severity: 'error',
          summary: 'Server Error',
          detail: 'Backend connection failed'
        });
      });
  }
}