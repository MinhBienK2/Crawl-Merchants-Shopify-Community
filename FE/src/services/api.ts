/**
 * API Service - Base HTTP Client
 * Handles all HTTP requests with error handling and interceptors
 */

import axios, { AxiosInstance, AxiosError, AxiosRequestConfig } from 'axios';
import { API_CONFIG } from '@/constants';
import type { ApiError, ApiResponse } from '@/types';

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_CONFIG.BASE_URL,
      timeout: API_CONFIG.TIMEOUT,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        // Add any auth tokens here if needed
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError<ApiError>) => {
        const errorMessage = this.handleError(error);
        return Promise.reject(new Error(errorMessage));
      }
    );
  }

  private handleError(error: AxiosError<ApiError>): string {
    if (error.response) {
      // Server responded with error status
      const data = error.response.data;
      return data?.detail || data?.message || data?.error || 'Server error occurred';
    } else if (error.request) {
      // Request made but no response
      return 'Network error. Please check your connection.';
    } else {
      // Error in request setup
      return error.message || 'An unexpected error occurred';
    }
  }

  async get<T>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    try {
      const response = await this.client.get<T>(url, config);
      return {
        data: response.data,
        status: response.status,
      };
    } catch (error) {
      return {
        error: { message: (error as Error).message },
        status: 500,
      };
    }
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    try {
      const response = await this.client.post<T>(url, data, config);
      return {
        data: response.data,
        status: response.status,
      };
    } catch (error) {
      return {
        error: { message: (error as Error).message },
        status: 500,
      };
    }
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    try {
      const response = await this.client.put<T>(url, data, config);
      return {
        data: response.data,
        status: response.status,
      };
    } catch (error) {
      return {
        error: { message: (error as Error).message },
        status: 500,
      };
    }
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    try {
      const response = await this.client.delete<T>(url, config);
      return {
        data: response.data,
        status: response.status,
      };
    } catch (error) {
      return {
        error: { message: (error as Error).message },
        status: 500,
      };
    }
  }
}

export const apiService = new ApiService();
