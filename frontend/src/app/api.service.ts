import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../environments/environment.prod';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  sendOrder(data: any) {
    return this.http.post(`${this.apiUrl}/orders/`, data);
  }

  sendFeedback(data: any) {
    return this.http.post(`${this.apiUrl}/feedback/`, data);
  }
}