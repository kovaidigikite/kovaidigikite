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
    { name: 'Resume', price: 299,},
    { name: 'Academic Presentation', price: 499, },
    { name: 'Academic Project', price: 999, },
    { name: 'Academic Activities', price: 399,  },
    { name: 'Business Presentation', price: 799,  },
    { name: 'Websites', price: 4999,  },
    { name: 'Applications', price: 9999, },
    { name: 'Digital Marketing', price: 1999, },
    { name: 'Business Analytics', price: 2999, },
    { name: 'Business Card', price: 199,  },
    { name: 'Brochures', price: 499,  },
    { name: 'Invitation', price: 299,  },
    { name: 'Social Media Post', price: 99, },
    { name: 'Flex Printing', price: 999, }
  ];

  goToOrder(service: string) {
    this.router.navigate(['/order'], { queryParams: { service } });
  }
}