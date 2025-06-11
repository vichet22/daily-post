import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AppProvider } from "./context/AppContext";
import { PostsProvider } from "./context/PostsContext";
import HomePage from "./pages/HomePage";
import AdminPage from "./pages/AdminPage";

function App() {
  return (
    <AppProvider>
      <PostsProvider>
        <Router>
          <div className="App">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/admin" element={<AdminPage />} />
            </Routes>
          </div>
        </Router>
      </PostsProvider>
    </AppProvider>
  );
}

export default App;
