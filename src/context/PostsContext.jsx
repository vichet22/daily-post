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

  // Load posts from localStorage
  useEffect(() => {
    const savedPosts = localStorage.getItem("dailyPostArticles");
    if (savedPosts) {
      setPosts(JSON.parse(savedPosts));
    } else {
      // Initialize with default posts
      const defaultPosts = [
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
      setPosts(defaultPosts);
      localStorage.setItem("dailyPostArticles", JSON.stringify(defaultPosts));
    }
  }, []);

  // Save posts to localStorage with error handling
  const updatePosts = (newPosts) => {
    try {
      setPosts(newPosts);
      localStorage.setItem("dailyPostArticles", JSON.stringify(newPosts));
    } catch (error) {
      if (error.name === "QuotaExceededError") {
        // Storage quota exceeded - try to free up space
        console.warn("localStorage quota exceeded, attempting cleanup...");

        // Remove images from older posts to free up space
        const postsWithoutImages = newPosts.map((post, index) => {
          if (index > 4) {
            // Keep images for latest 5 posts only
            return { ...post, image: null };
          }
          return post;
        });

        try {
          setPosts(postsWithoutImages);
          localStorage.setItem(
            "dailyPostArticles",
            JSON.stringify(postsWithoutImages)
          );
          console.log("Storage cleanup successful");
        } catch (secondError) {
          console.error("Failed to save even after cleanup:", secondError);
          throw new Error(
            "Storage quota exceeded. Please delete some posts or use smaller images."
          );
        }
      } else {
        throw error;
      }
    }
  };

  const addPost = (post) => {
    const newPost = {
      ...post,
      id: Date.now(),
      date: new Date().toISOString(),
      readTime: `${Math.ceil(post.content.split(" ").length / 200)} min read`,
    };
    const updatedPosts = [newPost, ...posts];
    updatePosts(updatedPosts);
    return newPost;
  };

  const updatePost = (updatedPost) => {
    if (!updatedPost || !updatedPost.id) {
      throw new Error("Invalid post data: missing post or post ID");
    }

    if (!updatedPost.content || typeof updatedPost.content !== "string") {
      throw new Error("Invalid post content");
    }

    const postWithUpdatedReadTime = {
      ...updatedPost,
      readTime: `${Math.ceil(
        updatedPost.content.split(" ").length / 200
      )} min read`,
    };

    const postExists = posts.some((post) => post.id === updatedPost.id);
    if (!postExists) {
      throw new Error(`Post with ID ${updatedPost.id} not found`);
    }

    const updatedPosts = posts.map((post) =>
      post.id === updatedPost.id ? postWithUpdatedReadTime : post
    );
    updatePosts(updatedPosts);
    return postWithUpdatedReadTime;
  };

  const deletePost = (id) => {
    const updatedPosts = posts.filter((post) => post.id !== id);
    updatePosts(updatedPosts);
  };

  const getPostById = (id) => {
    return posts.find((post) => post.id === parseInt(id));
  };

  const getPostsByCategory = (category) => {
    if (category === "All") return posts;
    return posts.filter(
      (post) => post.category.toLowerCase() === category.toLowerCase()
    );
  };

  const value = {
    posts,
    addPost,
    updatePost,
    deletePost,
    getPostById,
    getPostsByCategory,
    updatePosts,
  };

  return (
    <PostsContext.Provider value={value}>{children}</PostsContext.Provider>
  );
};

export default PostsContext;
