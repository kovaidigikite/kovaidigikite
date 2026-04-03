import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { InputTextModule } from 'primeng/inputtext';
import { SelectModule } from 'primeng/select';
import { RatingModule } from 'primeng/rating';
import { TextareaModule } from 'primeng/textarea';
import { ButtonModule } from 'primeng/button';
import { ToastModule } from 'primeng/toast';
import { MessageService } from 'primeng/api';

@Component({
  selector: 'app-feedback',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    InputTextModule,
    SelectModule,
    RatingModule,
    TextareaModule,
    ButtonModule,
    ToastModule
  ],
  templateUrl: './feedback.html',
  styleUrl: './feedback.css',
  providers: [MessageService]
})
export class FeedbackComponent {
  services = [
    'Resume',
    'Academic Presentation',
    'Academic Project',
    'Business Presentation',
    'Websites',
    'Applications',
    'Digital Marketing'
  ];

  name = '';
  orderDetails = '';
  contact = '';
  service = '';
  designFeedback = 0;
  customerFeedback = 0;
  comments = '';
  overallRating = 0;

  constructor(private msg: MessageService) {}

  submitFeedback() {
    if (
      !this.name ||
      !this.orderDetails ||
      !this.contact ||
      !this.service ||
      !this.designFeedback ||
      !this.customerFeedback ||
      !this.overallRating
    ) {
      this.msg.add({
        severity: 'warn',
        summary: 'Missing Fields',
        detail: 'Please fill all required fields'
      });
      return;
    }

    this.msg.add({
      severity: 'success',
      summary: 'Feedback Submitted',
      detail: 'Thank you for your feedback 💙'
    });

    fetch('https://https://kovaidigikite.onrender.com/api/feedback/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: this.name,
    orderDetails: this.orderDetails,
    contact: this.contact,
    service: this.service,
    designFeedback: this.designFeedback,
    customerFeedback: this.customerFeedback,
    comments: this.comments,
    overallRating: this.overallRating
  })
})
  }
}