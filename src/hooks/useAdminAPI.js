import { useState, useCallback } from "react";
import api from "../services/api";

const useAdminAPI = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [adminData, setAdminData] = useState(null);

  // Admin login
  const login = useCallback(async (username, password) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.admin.login(username, password);
      if (response.success) {
        setAdminData(response.data);
        // Store admin authentication in localStorage
        localStorage.setItem('dailyPostAdminAuth', 'true');
        localStorage.setItem('dailyPostAdminData', JSON.stringify(response.data));
        return response.data;
      } else {
        throw new Error(response.message || 'Login failed');
      }
    } catch (err) {
      console.error('Error during login:', err);
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  // Admin logout
  const logout = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      await api.admin.logout();
      setAdminData(null);
      // Clear admin authentication from localStorage
      localStorage.removeItem('dailyPostAdminAuth');
      localStorage.removeItem('dailyPostAdminData');
      return true;
    } catch (err) {
      console.error('Error during logout:', err);
      setError(err.message);
      // Still clear local data even if API call fails
      setAdminData(null);
      localStorage.removeItem('dailyPostAdminAuth');
      localStorage.removeItem('dailyPostAdminData');
      return true;
    } finally {
      setLoading(false);
    }
  }, []);

  // Get admin profile
  const getProfile = useCallback(async (id) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.admin.getProfile(id);
      if (response.success) {
        return response.data;
      } else {
        throw new Error(response.message || 'Failed to get profile');
      }
    } catch (err) {
      console.error('Error getting profile:', err);
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  // Create new admin
  const createAdmin = useCallback(async (username, password) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.admin.createAdmin(username, password);
      if (response.success) {
        return response.data;
      } else {
        throw new Error(response.message || 'Failed to create admin');
      }
    } catch (err) {
      console.error('Error creating admin:', err);
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  // Change admin password
  const changePassword = useCallback(async (id, newPassword) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.admin.changePassword(id, newPassword);
      if (response.success) {
        return response.data;
      } else {
        throw new Error(response.message || 'Failed to change password');
      }
    } catch (err) {
      console.error('Error changing password:', err);
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  // Get all admin users
  const getAllAdmins = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.admin.getAllAdmins();
      if (response.success) {
        return response.data;
      } else {
        throw new Error(response.message || 'Failed to get admin users');
      }
    } catch (err) {
      console.error('Error getting admin users:', err);
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  // Check if admin is authenticated
  const isAuthenticated = useCallback(() => {
    const authStatus = localStorage.getItem('dailyPostAdminAuth');
    const storedAdminData = localStorage.getItem('dailyPostAdminData');
    
    if (authStatus === 'true' && storedAdminData) {
      try {
        const parsedData = JSON.parse(storedAdminData);
        setAdminData(parsedData);
        return true;
      } catch (err) {
        console.error('Error parsing stored admin data:', err);
        localStorage.removeItem('dailyPostAdminAuth');
        localStorage.removeItem('dailyPostAdminData');
        return false;
      }
    }
    
    return false;
  }, []);

  // Initialize admin state from localStorage
  const initializeAuth = useCallback(() => {
    return isAuthenticated();
  }, [isAuthenticated]);

  // Clear error
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    loading,
    error,
    adminData,
    login,
    logout,
    getProfile,
    createAdmin,
    changePassword,
    getAllAdmins,
    isAuthenticated,
    initializeAuth,
    clearError,
  };
};

export default useAdminAPI;
