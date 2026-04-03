import { Routes } from '@angular/router';
import { HomeComponent } from './home/home';
import { AboutComponent } from './about/about';
import { ServicesComponent } from './services/services';
import { OrderComponent } from './order/order';
import { FeedbackComponent } from './feedback/feedback';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'about', component: AboutComponent },
  { path: 'services', component: ServicesComponent },
  { path: 'order', component: OrderComponent },
  { path: 'feedback', component: FeedbackComponent }
];