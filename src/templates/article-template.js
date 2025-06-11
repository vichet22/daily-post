// Article Template for Daily Post
// Follow this structure for consistent formatting

export const articleTemplate = {
  id: 0, // Auto-increment this number
  title: "Your Article Title Here",
  excerpt: "Brief description of the article that appears in the preview. Keep it engaging and informative, ending with ellipsis if needed...",
  content: `
    <p>First paragraph should grab the reader's attention and provide the main story details. Include key facts like who, what, when, where.</p>
    
    <p>Second paragraph should provide additional context and background information. This helps readers understand the significance of the story.</p>
    
    <p>Include quotes from relevant people when possible. "This adds credibility and human interest to your story," said Expert Name, Title.</p>
    
    <p>Provide more details, statistics, or analysis in subsequent paragraphs. Each paragraph should focus on one main idea or aspect of the story.</p>
    
    <p>Include any relevant consequences, next steps, or future implications of the story. This helps readers understand why the story matters.</p>
    
    <p>End with a strong conclusion that ties everything together or provides a call to action for readers.</p>
  `,
  category: "NEWS", // Options: "NEWS", "SPORT", "POLITICS"
  author: "Admin", // Use "Admin" or specific author name
  date: "May 20, 2025", // Format: "Month DD, YYYY"
  readTime: "3 min read", // Estimate based on content length
  image: "/api/placeholder/600/400", // Placeholder or actual image path
  tags: ["tag1", "tag2", "tag3", "tag4"] // Relevant keywords for the article
};

// Guidelines for creating articles:

// TITLE GUIDELINES:
// - Keep titles concise but descriptive
// - Use active voice when possible
// - Include key details that grab attention
// - Examples from template:
//   * "Bride-to-Be Sucker-Punched at Her Bachelorette Party"
//   * "At least 19 dead in Kentucky, nearly 200,000 left without power after weekend storms"

// EXCERPT GUIDELINES:
// - Should be 1-2 sentences
// - Provide enough detail to entice readers
// - Can end with "..." to indicate more content
// - Should match the tone and style of the full article

// CONTENT GUIDELINES:
// - Use HTML paragraph tags <p></p>
// - Include quotes with proper attribution
// - Provide specific details, numbers, and facts
// - Structure with clear beginning, middle, and end
// - Each paragraph should be 2-4 sentences

// DATE FORMAT:
// - Use format: "Month DD, YYYY" (e.g., "May 20, 2025")
// - Keep consistent with the template style shown in the image

// CATEGORY GUIDELINES:
// - NEWS: Breaking news, crime, accidents, general news
// - SPORT: Sports events, championships, athlete news
// - POLITICS: Elections, policy changes, political events

// AUTHOR GUIDELINES:
// - Use "Admin" for general articles
// - Use specific names for attributed articles
// - Keep consistent with existing style

// READ TIME ESTIMATION:
// - 1-2 paragraphs: "2 min read"
// - 3-4 paragraphs: "3 min read"
// - 5-6 paragraphs: "4 min read"
// - 7+ paragraphs: "5+ min read"

// TAGS:
// - Use 3-5 relevant keywords
// - Keep them lowercase
// - Include location names, event types, key subjects
