// API Configuration
const API_BASE_URL = 'http://localhost:3001/api';

// Helper function to handle API responses
const handleResponse = async (response) => {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
  }
  return response.json();
};

// Helper function to create FormData for file uploads
const createFormData = (data, file = null) => {
  const formData = new FormData();
  
  // Add all data fields
  Object.keys(data).forEach(key => {
    if (data[key] !== null && data[key] !== undefined) {
      formData.append(key, data[key]);
    }
  });
  
  // Add file if provided
  if (file) {
    formData.append('imageFile', file);
  }
  
  return formData;
};

// Posts API
export const postsAPI = {
  // Get all posts with optional filtering
  async getAllPosts(category = null, limit = null, offset = 0, search = null) {
    const params = new URLSearchParams();
    
    if (category && category !== 'all') params.append('category', category);
    if (limit) params.append('limit', limit);
    if (offset) params.append('offset', offset);
    if (search) params.append('search', search);
    
    const url = `${API_BASE_URL}/posts${params.toString() ? `?${params.toString()}` : ''}`;
    
    const response = await fetch(url);
    return handleResponse(response);
  },

  // Get single post by ID
  async getPostById(id) {
    const response = await fetch(`${API_BASE_URL}/posts/${id}`);
    return handleResponse(response);
  },

  // Create new post
  async createPost(postData, imageFile = null) {
    const formData = createFormData(postData, imageFile);
    
    const response = await fetch(`${API_BASE_URL}/posts`, {
      method: 'POST',
      body: formData,
    });
    
    return handleResponse(response);
  },

  // Update existing post
  async updatePost(id, postData, imageFile = null) {
    const formData = createFormData(postData, imageFile);
    
    const response = await fetch(`${API_BASE_URL}/posts/${id}`, {
      method: 'PUT',
      body: formData,
    });
    
    return handleResponse(response);
  },

  // Delete post
  async deletePost(id) {
    const response = await fetch(`${API_BASE_URL}/posts/${id}`, {
      method: 'DELETE',
    });
    
    return handleResponse(response);
  },

  // Upload image file
  async uploadImage(file) {
    const formData = new FormData();
    formData.append('image', file);
    
    const response = await fetch(`${API_BASE_URL}/posts/upload`, {
      method: 'POST',
      body: formData,
    });
    
    return handleResponse(response);
  },

  // Search posts
  async searchPosts(searchTerm, category = null) {
    return this.getAllPosts(category, null, 0, searchTerm);
  }
};

// Admin API
export const adminAPI = {
  // Admin login
  async login(username, password) {
    const response = await fetch(`${API_BASE_URL}/admin/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });
    
    return handleResponse(response);
  },

  // Admin logout
  async logout() {
    const response = await fetch(`${API_BASE_URL}/admin/logout`, {
      method: 'POST',
    });
    
    return handleResponse(response);
  },

  // Get admin profile
  async getProfile(id) {
    const response = await fetch(`${API_BASE_URL}/admin/profile/${id}`);
    return handleResponse(response);
  },

  // Create new admin
  async createAdmin(username, password) {
    const response = await fetch(`${API_BASE_URL}/admin/create`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });
    
    return handleResponse(response);
  },

  // Change admin password
  async changePassword(id, newPassword) {
    const response = await fetch(`${API_BASE_URL}/admin/change-password/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ newPassword }),
    });
    
    return handleResponse(response);
  },

  // Get all admin users
  async getAllAdmins() {
    const response = await fetch(`${API_BASE_URL}/admin/users`);
    return handleResponse(response);
  }
};

// Utility API
export const utilityAPI = {
  // Health check
  async healthCheck() {
    const response = await fetch(`${API_BASE_URL}/health`);
    return handleResponse(response);
  },

  // Get API info
  async getApiInfo() {
    const response = await fetch('http://localhost:3001/');
    return handleResponse(response);
  }
};

// Export default API object
const api = {
  posts: postsAPI,
  admin: adminAPI,
  utility: utilityAPI,
};

export default api;
