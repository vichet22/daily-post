import { useState, useEffect } from "react";

const usePosts = () => {
  const [posts, setPosts] = useState([]);

  // Load posts from localStorage
  useEffect(() => {
    const loadPosts = () => {
      const savedPosts = localStorage.getItem("dailyPostArticles");
      if (savedPosts) {
        setPosts(JSON.parse(savedPosts));
      } else {
        // Default posts if none exist - use template articles
        const defaultPosts = [
          {
            id: 1,
            title: "Bride-to-Be Sucker-Punched at Her Bachelorette Party",
            excerpt:
              "Canada Rinaldi left her bachelorette party in Dallas, Texas on a stretcher, after getting punched by a complete stranger. Rinaldi was rendered unconscious; she suffered a concussion, broken nose, three...",
            content:
              "Canada Rinaldi left her bachelorette party in Dallas, Texas on a stretcher, after getting punched by a complete stranger. Rinaldi was rendered unconscious; she suffered a concussion, broken nose, three fractured teeth, and severe facial bruising.",
            category: "NEWS",
            author: "Admin",
            date: new Date().toISOString(),
            readTime: "3 min read",
            image: null,
            featured: true,
          },
          {
            id: 2,
            title:
              "At least 19 dead in Kentucky, nearly 200,000 left without power after weekend storms",
            excerpt:
              "Kentucky's governor announced the state would look into emergency housing options after storms and severe weather killed at least 19 people in Kentucky. 'We are hard at work this morning...'",
            content:
              "Kentucky's governor announced the state would look into emergency housing options after storms and severe weather killed at least 19 people in Kentucky. We are hard at work this morning to assess the damage and coordinate our response efforts.",
            category: "NEWS",
            author: "Kentucky",
            date: new Date().toISOString(),
            readTime: "4 min read",
            image: null,
            featured: false,
          },
          {
            id: 3,
            title: "NBA Finals Game 7 Tonight: Championship on the Line",
            excerpt:
              "The most anticipated Game 7 in NBA history tips off tonight as two powerhouse teams battle for the championship title. Both teams have everything to play for in what promises to be an epic showdown...",
            content:
              "The most anticipated Game 7 in NBA history tips off tonight as two powerhouse teams battle for the championship title. Both teams have everything to play for in what promises to be an epic showdown at the sold-out arena.",
            category: "SPORT",
            author: "Admin",
            date: new Date().toISOString(),
            readTime: "3 min read",
            image: null,
            featured: true,
          },
        ];
        setPosts(defaultPosts);
        localStorage.setItem("dailyPostArticles", JSON.stringify(defaultPosts));
      }
    };

    loadPosts();

    // Listen for storage changes to update posts in real-time
    const handleStorageChange = () => {
      loadPosts();
    };

    window.addEventListener("storage", handleStorageChange);

    // Also listen for custom events for same-tab updates
    window.addEventListener("postsUpdated", handleStorageChange);

    return () => {
      window.removeEventListener("storage", handleStorageChange);
      window.removeEventListener("postsUpdated", handleStorageChange);
    };
  }, []);

  // Get posts by category
  const getPostsByCategory = (category) => {
    if (category === "All") {
      return posts;
    }
    return posts.filter(
      (post) => post.category.toLowerCase() === category.toLowerCase()
    );
  };

  // Add new post
  const addPost = (newPost) => {
    const post = {
      ...newPost,
      id: Date.now(),
      date: new Date().toISOString(),
      readTime: `${Math.ceil(
        newPost.content.split(" ").length / 200
      )} min read`,
    };
    const updatedPosts = [post, ...posts];
    setPosts(updatedPosts);
    localStorage.setItem("dailyPostArticles", JSON.stringify(updatedPosts));

    // Trigger custom event for same-tab updates
    window.dispatchEvent(new Event("postsUpdated"));

    return post;
  };

  // Update existing post
  const updatePost = (updatedPost) => {
    const updatedPosts = posts.map((post) =>
      post.id === updatedPost.id
        ? {
            ...updatedPost,
            readTime: `${Math.ceil(
              updatedPost.content.split(" ").length / 200
            )} min read`,
          }
        : post
    );
    setPosts(updatedPosts);
    localStorage.setItem("dailyPostArticles", JSON.stringify(updatedPosts));

    // Trigger custom event for same-tab updates
    window.dispatchEvent(new Event("postsUpdated"));

    return updatedPost;
  };

  // Delete post
  const deletePost = (postId) => {
    const updatedPosts = posts.filter((post) => post.id !== postId);
    setPosts(updatedPosts);
    localStorage.setItem("dailyPostArticles", JSON.stringify(updatedPosts));

    // Trigger custom event for same-tab updates
    window.dispatchEvent(new Event("postsUpdated"));

    return true;
  };

  // Get post by ID
  const getPostById = (postId) => {
    return posts.find((post) => post.id === parseInt(postId));
  };

  // Get featured posts
  const getFeaturedPosts = () => {
    return posts.filter((post) => post.featured);
  };

  return {
    posts,
    getPostsByCategory,
    addPost,
    updatePost,
    deletePost,
    getPostById,
    getFeaturedPosts,
  };
};

export default usePosts;
