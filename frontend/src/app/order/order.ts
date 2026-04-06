import { Component, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { SelectModule } from 'primeng/select';
import { TextareaModule } from 'primeng/textarea';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { ToastModule } from 'primeng/toast';
import { FileUploadModule } from 'primeng/fileupload';
import { MessageService } from 'primeng/api';
import { CommonModule } from '@angular/common';

@Component({
  standalone: true,
  selector: 'app-order',
  styleUrls: ['./order.css'],
  imports: [
    CommonModule,
    FormsModule,
    InputTextModule,
    TextareaModule,
    ButtonModule,
    ToastModule,
    SelectModule,
    FileUploadModule
  ],
  providers: [MessageService],
  templateUrl: './order.html',
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class OrderComponent {
  services = [
    { name: 'Resume' },
    { name: 'Academic Presentation' },
    { name: 'Academic Project' },
    { name: 'Academic Activities' },
    { name: 'Business Presentation' },
    { name: 'Websites' },
    { name: 'Applications' },
    { name: 'Digital Marketing' },
    { name: 'Business Analytics' },
    { name: 'Business Card' },
    { name: 'Brochures' },
    { name: 'Invitation' },
    { name: 'Social Media Post' },
    { name: 'Flex Printing' }
  ];

  selectedService: any;
  selectedFile: File | null = null;

  name = '';
  email = ''
  phone = ''
  message = '';
  

  constructor(
    private route: ActivatedRoute,
    private msg: MessageService
  ) {
    this.route.queryParams.subscribe(p => {
      if (p['service']) {
        this.selectedService = this.services.find(
          s => s.name === p['service']
        );
      }
    });
  }

 onFileSelect(event: any) {
  this.selectedFile = event.files[0];
}

 placeOrder() {
  if (!this.name || !this.email || !this.phone || !this.selectedService) {
    this.msg.add({
      severity: 'warn',
      summary: 'Missing Fields',
      detail: 'Please fill all required details'
    });
    return;
  }

  const formData = new FormData();
  formData.append('name', this.name);
  formData.append('email', this.email);
  formData.append('phone', this.phone);
  formData.append(
    'service',
    this.selectedService?.name || this.selectedService
  );
  formData.append('message', this.message || '');

  if (this.selectedFile) {
    formData.append('file', this.selectedFile);
  }

  fetch('https://kovaidigikite.onrender.com/api/order/', {
    method: 'POST',
    body: formData
  })
    .then(async res => {
      const data = await res.json();
      console.log("ORDER API:", data);

      if (data.success) {
        this.msg.add({
          severity: 'success',
          summary: 'Order Sent',
          detail: 'Order sent successfully ✅'
        });

        this.name = '';
        this.email = '';
        this.phone = '';
        this.message = '';
        this.selectedService = null;
        this.selectedFile = null;
      } else {
        this.msg.add({
          severity: 'error',
          summary: 'Failed',
          detail: JSON.stringify(data.errors)
        });
      }
    })
    .catch(err => {
      console.error(err);
      this.msg.add({
        severity: 'error',
        summary: 'Upload Failed',
        detail: 'Server error ❌'
      });
    });
}
}