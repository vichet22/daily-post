import Header from '../components/Header'
import Hero from '../components/Hero'
import LatestPosts from '../components/LatestPosts'
import PostModal from '../components/PostModal'
import AdminPanel from '../components/AdminPanel'

const HomePage = () => {
  return (
    <>
      <Header />
      <Hero />
      <LatestPosts />
      <AdminPanel />
      <PostModal />
    </>
  )
}

export default HomePage
