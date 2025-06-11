import { useState, useEffect, useCallback } from "react";
import api from "../services/api";

const usePostsAPI = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load posts from API
  const loadPosts = useCallback(async (category = null, search = null) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.posts.getAllPosts(category, null, 0, search);
      if (response.success) {
        setPosts(response.data);
      } else {
        throw new Error(response.message || 'Failed to load posts');
      }
    } catch (err) {
      console.error('Error loading posts:', err);
      setError(err.message);
      // Fallback to empty array on error
      setPosts([]);
    } finally {
      setLoading(false);
    }
  }, []);

  // Initial load
  useEffect(() => {
    loadPosts();
  }, [loadPosts]);

  // Get posts by category
  const getPostsByCategory = useCallback(async (category) => {
    if (category === "All" || category === "all") {
      return posts;
    }
    
    try {
      const response = await api.posts.getAllPosts(category);
      if (response.success) {
        return response.data;
      }
      return [];
    } catch (err) {
      console.error('Error getting posts by category:', err);
      return posts.filter(
        (post) => post.category.toLowerCase() === category.toLowerCase()
      );
    }
  }, [posts]);

  // Add new post
  const addPost = useCallback(async (newPost, imageFile = null) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.posts.createPost(newPost, imageFile);
      if (response.success) {
        // Reload posts to get updated list
        await loadPosts();
        return response.data;
      } else {
        throw new Error(response.message || 'Failed to create post');
      }
    } catch (err) {
      console.error('Error creating post:', err);
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [loadPosts]);

  // Update existing post
  const updatePost = useCallback(async (updatedPost, imageFile = null) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.posts.updatePost(updatedPost.id, updatedPost, imageFile);
      if (response.success) {
        // Reload posts to get updated list
        await loadPosts();
        return response.data;
      } else {
        throw new Error(response.message || 'Failed to update post');
      }
    } catch (err) {
      console.error('Error updating post:', err);
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [loadPosts]);

  // Delete post
  const deletePost = useCallback(async (postId) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.posts.deletePost(postId);
      if (response.success) {
        // Reload posts to get updated list
        await loadPosts();
        return true;
      } else {
        throw new Error(response.message || 'Failed to delete post');
      }
    } catch (err) {
      console.error('Error deleting post:', err);
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [loadPosts]);

  // Get post by ID
  const getPostById = useCallback(async (postId) => {
    try {
      // First try to find in current posts
      const localPost = posts.find((post) => post.id === parseInt(postId));
      if (localPost) {
        return localPost;
      }
      
      // If not found locally, fetch from API
      const response = await api.posts.getPostById(postId);
      if (response.success) {
        return response.data;
      }
      return null;
    } catch (err) {
      console.error('Error getting post by ID:', err);
      return null;
    }
  }, [posts]);

  // Get featured posts (posts with featured flag)
  const getFeaturedPosts = useCallback(() => {
    return posts.filter((post) => post.featured);
  }, [posts]);

  // Search posts
  const searchPosts = useCallback(async (searchTerm, category = null) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.posts.searchPosts(searchTerm, category);
      if (response.success) {
        return response.data;
      } else {
        throw new Error(response.message || 'Failed to search posts');
      }
    } catch (err) {
      console.error('Error searching posts:', err);
      setError(err.message);
      return [];
    } finally {
      setLoading(false);
    }
  }, []);

  // Upload image
  const uploadImage = useCallback(async (file) => {
    try {
      const response = await api.posts.uploadImage(file);
      if (response.success) {
        return response.data;
      } else {
        throw new Error(response.message || 'Failed to upload image');
      }
    } catch (err) {
      console.error('Error uploading image:', err);
      throw err;
    }
  }, []);

  // Refresh posts
  const refreshPosts = useCallback(() => {
    return loadPosts();
  }, [loadPosts]);

  return {
    posts,
    loading,
    error,
    getPostsByCategory,
    addPost,
    updatePost,
    deletePost,
    getPostById,
    getFeaturedPosts,
    searchPosts,
    uploadImage,
    refreshPosts,
    loadPosts,
  };
};

export default usePostsAPI;
