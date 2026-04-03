import { bootstrapApplication } from '@angular/platform-browser';
import { provideAnimations } from '@angular/platform-browser/animations';
import { provideRouter } from '@angular/router';  // 🔥 ADD
import { providePrimeNG } from 'primeng/config';
import Lara from '@primeng/themes/lara';

import { App } from './app/app';
import { routes } from './app/app.routes';  // 🔥 ADD

bootstrapApplication(App, {
  providers: [
    provideAnimations(),
    provideRouter(routes),   // 🔥 MUST ADD
    providePrimeNG({
      theme: {
        preset: Lara
      }
    })
  ]
});