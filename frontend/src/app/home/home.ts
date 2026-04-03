import { Component, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { CommonModule } from '@angular/common';
import { CarouselModule } from 'primeng/carousel';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ToastModule } from 'primeng/toast';
import { MessageService } from 'primeng/api';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    ButtonModule,
    CommonModule,
    CarouselModule,
    RouterModule,
    FormsModule,
    ToastModule
  ],
  templateUrl: './home.html',
  styleUrl: './home.css',
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  providers: [MessageService]
})
export class HomeComponent {
  images = [
    'assets/2.png',
    'assets/3.png',
    'assets/4.png',
    'assets/5.png'
  ];

  currentIndex = 0;

  contactName = '';
  contactEmail = '';
  contactPhone = '';
  contactMessage = '';

  constructor(private msg: MessageService) {}

  next() {
    this.currentIndex = (this.currentIndex + 1) % this.images.length;
  }

  prev() {
    this.currentIndex =
      (this.currentIndex - 1 + this.images.length) % this.images.length;
  }

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

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(this.contactEmail)) {
      this.msg.add({
        severity: 'warn',
        summary: 'Invalid Email',
        detail: 'Please enter a valid email 📧'
      });
      return;
    }

    const data = {
      name: this.contactName,
      email: this.contactEmail,
      phone: this.contactPhone,
      message: this.contactMessage
    };

    fetch('https://kovaidigikite.onrender.com/api/contact/', {
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
          detail: 'Backend connection failed '
        });
      });
  }
}