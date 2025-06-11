import { createContext, useContext, useReducer, useEffect } from "react";

const AppContext = createContext();

// Action types
const ACTIONS = {
  SET_SEARCH_QUERY: "SET_SEARCH_QUERY",
  SET_ACTIVE_CATEGORY: "SET_ACTIVE_CATEGORY",
  SET_SELECTED_POST: "SET_SELECTED_POST",
  SET_LOADING: "SET_LOADING",
  SET_ERROR: "SET_ERROR",
  TOGGLE_MOBILE_MENU: "TOGGLE_MOBILE_MENU",
  SET_ADMIN_MODE: "SET_ADMIN_MODE",
  SET_CURRENT_PAGE: "SET_CURRENT_PAGE",
  SET_ADMIN_AUTHENTICATED: "SET_ADMIN_AUTHENTICATED",
  ADMIN_LOGOUT: "ADMIN_LOGOUT",
};

// Initial state
const initialState = {
  searchQuery: "",
  activeCategory: "all",
  selectedPost: null,
  loading: false,
  error: null,
  mobileMenuOpen: false,
  adminMode: false,
  adminAuthenticated: false,
  postsPerPage: 6,
  currentPage: 1,
};

// Reducer function
function appReducer(state, action) {
  switch (action.type) {
    case ACTIONS.SET_SEARCH_QUERY:
      return { ...state, searchQuery: action.payload, currentPage: 1 };

    case ACTIONS.SET_ACTIVE_CATEGORY:
      return { ...state, activeCategory: action.payload, currentPage: 1 };

    case ACTIONS.SET_SELECTED_POST:
      return { ...state, selectedPost: action.payload };

    case ACTIONS.SET_LOADING:
      return { ...state, loading: action.payload };

    case ACTIONS.SET_ERROR:
      return { ...state, error: action.payload };

    case ACTIONS.TOGGLE_MOBILE_MENU:
      return { ...state, mobileMenuOpen: !state.mobileMenuOpen };

    case ACTIONS.SET_ADMIN_MODE:
      return { ...state, adminMode: action.payload };

    case ACTIONS.SET_CURRENT_PAGE:
      return { ...state, currentPage: action.payload };

    case ACTIONS.SET_ADMIN_AUTHENTICATED:
      return { ...state, adminAuthenticated: action.payload };

    case ACTIONS.ADMIN_LOGOUT:
      return {
        ...state,
        adminMode: false,
        adminAuthenticated: false,
      };

    default:
      return state;
  }
}

// Context Provider
export function AppProvider({ children }) {
  const [state, dispatch] = useReducer(appReducer, initialState);

  // Check for saved admin authentication on mount
  useEffect(() => {
    const adminAuth = localStorage.getItem("dailyPostAdminAuth");
    if (adminAuth === "true") {
      dispatch({ type: ACTIONS.SET_ADMIN_AUTHENTICATED, payload: true });
    }
  }, []);

  // Save admin authentication state
  useEffect(() => {
    localStorage.setItem(
      "dailyPostAdminAuth",
      state.adminAuthenticated.toString()
    );
  }, [state.adminAuthenticated]);

  const value = {
    ...state,
    dispatch,
    ACTIONS,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

// Custom hook to use the context
export function useApp() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error("useApp must be used within an AppProvider");
  }
  return context;
}

export default AppContext;
