import { createContext, useContext, useState, useEffect } from "react";

const PostsContext = createContext();

export const usePosts = () => {
  const context = useContext(PostsContext);
  if (!context) {
    throw new Error("usePosts must be used within a PostsProvider");
  }
  return context;
};

export const PostsProvider = ({ children }) => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Get default posts
  const getDefaultPosts = () => [
    {
      id: 1,
      title: "Bride-to-Be Sucker-Punched at Her Bachelorette Party",
      excerpt:
        "Canada Rinaldi left her bachelorette party in Dallas, Texas on a stretcher, after getting punched by a complete stranger. Rinaldi was rendered unconscious; she suffered a concussion, broken nose, three...",
      content:
        "Canada Rinaldi left her bachelorette party in Dallas, Texas on a stretcher, after getting punched by a complete stranger. Rinaldi was rendered unconscious; she suffered a concussion, broken nose, three fractured teeth, and severe facial bruising. The incident occurred at approximately 11:30 PM outside a popular downtown Dallas venue where Rinaldi was celebrating with her bridal party.",
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
        "Kentucky's governor announced the state would look into emergency housing options after storms and severe weather killed at least 19 people in Kentucky. We are hard at work this morning to assess the damage and coordinate our response efforts. The devastating storms swept through the state over the weekend, bringing with them destructive winds, heavy rainfall, and multiple tornadoes.",
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
        "The most anticipated Game 7 in NBA history tips off tonight as two powerhouse teams battle for the championship title. Both teams have everything to play for in what promises to be an epic showdown at the sold-out arena. The series has been a back-and-forth thriller, with neither team able to gain a decisive advantage.",
      category: "SPORT",
      author: "Admin",
      date: new Date().toISOString(),
      readTime: "3 min read",
      image: null,
      featured: true,
    },
    {
      id: 4,
      title: "Senate Passes Landmark Healthcare Reform Bill",
      excerpt:
        "In a historic 52-48 vote, the Senate passed comprehensive healthcare reform legislation that will expand coverage to millions of Americans. The bill now heads to the House for final approval...",
      content:
        "In a historic 52-48 vote, the Senate passed comprehensive healthcare reform legislation that will expand coverage to millions of Americans. The bill now heads to the House for final approval before reaching the President's desk. The legislation includes provisions for lowering prescription drug costs, expanding Medicare benefits, and creating new healthcare access programs.",
      category: "POLITICS",
      author: "Admin",
      date: new Date().toISOString(),
      readTime: "4 min read",
      image: null,
      featured: false,
    },
    {
      id: 5,
      title: "World Cup Qualifier: Team USA Advances to Finals",
      excerpt:
        "Team USA secured their spot in the World Cup finals with a dramatic 3-2 victory over Brazil in yesterday's semifinal match. The win marks the first time in 12 years that the US team has reached this stage...",
      content:
        "Team USA secured their spot in the World Cup finals with a dramatic 3-2 victory over Brazil in yesterday's semifinal match. The win marks the first time in 12 years that the US team has reached this stage of the tournament. The match was a rollercoaster of emotions, with Brazil taking an early 2-0 lead in the first half.",
      category: "SPORT",
      author: "Admin",
      date: new Date().toISOString(),
      readTime: "3 min read",
      image: null,
      featured: false,
    },
    {
      id: 6,
      title: "Presidential Debate Draws Record 85 Million Viewers",
      excerpt:
        "Last night's presidential debate shattered viewership records with 85 million Americans tuning in to watch the candidates clash on key issues. The heated exchange covered healthcare, economy, and foreign policy...",
      content:
        "Last night's presidential debate shattered viewership records with 85 million Americans tuning in to watch the candidates clash on key issues. The heated exchange covered healthcare, economy, and foreign policy in what many are calling the most consequential debate in recent history. The 90-minute debate was marked by sharp disagreements on healthcare policy.",
      category: "POLITICS",
      author: "Admin",
      date: new Date().toISOString(),
      readTime: "4 min read",
      image: null,
      featured: true,
    },
  ];

  // Load posts from localStorage
  const loadPosts = async (category = null, search = null) => {
    setLoading(true);
    setError(null);

    try {
      // Simulate loading delay for better UX
      await new Promise((resolve) => setTimeout(resolve, 300));

      const savedPosts = localStorage.getItem("dailyPostArticles");
      let allPosts = [];

      if (savedPosts) {
        allPosts = JSON.parse(savedPosts);
      } else {
        // Initialize with default posts
        allPosts = getDefaultPosts();
        localStorage.setItem("dailyPostArticles", JSON.stringify(allPosts));
      }

      // Filter by category if specified
      if (category && category !== "All" && category !== "all") {
        allPosts = allPosts.filter(
          (post) => post.category.toLowerCase() === category.toLowerCase()
        );
      }

      // Filter by search if specified
      if (search) {
        const searchLower = search.toLowerCase();
        allPosts = allPosts.filter(
          (post) =>
            post.title.toLowerCase().includes(searchLower) ||
            post.excerpt.toLowerCase().includes(searchLower) ||
            post.content.toLowerCase().includes(searchLower)
        );
      }

      setPosts(allPosts);
    } catch (err) {
      console.error("Error loading posts:", err);
      setError("Failed to load posts");
      setPosts([]);
    } finally {
      setLoading(false);
    }
  };

  // Initial load
  useEffect(() => {
    loadPosts();
  }, []);

  const addPost = async (post, imageFile = null) => {
    setLoading(true);
    setError(null);

    try {
      // Simulate API delay
      await new Promise((resolve) => setTimeout(resolve, 500));

      const savedPosts = localStorage.getItem("dailyPostArticles");
      const existingPosts = savedPosts
        ? JSON.parse(savedPosts)
        : getDefaultPosts();

      // Generate new ID
      const newId = Math.max(...existingPosts.map((p) => p.id), 0) + 1;

      // Create new post with generated ID
      const newPost = {
        ...post,
        id: newId,
        date: new Date().toISOString(),
        author: "Admin",
        featured: false,
        // Handle image file (for now, just store the filename or URL)
        image: imageFile ? URL.createObjectURL(imageFile) : post.image || null,
      };

      // Add to posts array
      const updatedPosts = [newPost, ...existingPosts];

      // Save to localStorage
      localStorage.setItem("dailyPostArticles", JSON.stringify(updatedPosts));

      // Reload posts to reflect changes
      await loadPosts();

      return newPost;
    } catch (err) {
      console.error("Error creating post:", err);
      setError("Failed to create post");
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const updatePost = async (updatedPost, imageFile = null) => {
    setLoading(true);
    setError(null);

    try {
      const response = await api.posts.updatePost(
        updatedPost.id,
        updatedPost,
        imageFile
      );
      if (response.success) {
        // Reload posts to get updated list
        await loadPosts();
        return response.data;
      } else {
        throw new Error(response.message || "Failed to update post");
      }
    } catch (err) {
      console.error("Error updating post:", err);
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const deletePost = async (id) => {
    setLoading(true);
    setError(null);

    try {
      const response = await api.posts.deletePost(id);
      if (response.success) {
        // Reload posts to get updated list
        await loadPosts();
        return true;
      } else {
        throw new Error(response.message || "Failed to delete post");
      }
    } catch (err) {
      console.error("Error deleting post:", err);
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const getPostById = (id) => {
    return posts.find((post) => post.id === parseInt(id));
  };

  const getPostsByCategory = async (category) => {
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
      console.error("Error getting posts by category:", err);
      return posts.filter(
        (post) => post.category.toLowerCase() === category.toLowerCase()
      );
    }
  };

  const value = {
    posts,
    loading,
    error,
    addPost,
    updatePost,
    deletePost,
    getPostById,
    getPostsByCategory,
    loadPosts,
  };

  return (
    <PostsContext.Provider value={value}>{children}</PostsContext.Provider>
  );
};

export default PostsContext;
