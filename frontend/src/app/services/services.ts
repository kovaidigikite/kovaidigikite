import { Component, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { Router } from '@angular/router';
import { CardModule } from 'primeng/card';
import { CommonModule } from '@angular/common';

@Component({
  standalone: true,
  selector: 'app-services',
  imports: [CommonModule, CardModule],
  templateUrl: './services.html',
  styleUrl: './services.css',
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class ServicesComponent {

  constructor(private router: Router) {}

 services = [
  { name: 'Resume', price: 299 },
  { name: 'Academic Presentation', price: 499 },
  { name: 'Academic Project', price: 999 },
  { name: 'Business Presentation', price: 799 },
  { name: 'Websites', price: 2999 },
  { name: 'Digital Marketing', price: 999 },
  { name: 'Business Analytics', price: 1999 },
  { name: 'Business Card Designing', price: 299 },
  { name: 'Brochures Designing', price: 299 },
  { name: 'Invitation Designing', price: 299 },
  { name: 'Social Media Post', price: 99 },
  { name: 'Printing', note: 'Based on quantity' }
];

  goToOrder(service: string) {
    this.router.navigate(['/order'], { queryParams: { service } });
  }
}