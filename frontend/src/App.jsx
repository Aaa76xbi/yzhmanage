import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ApolloClient, InMemoryCache, ApolloProvider } from '@apollo/client';
import HomePage from './pages/HomePage';
import UserProfile from './pages/UserProfile';
import Navbar from './components/Navbar';

// 配置 Apollo Client 连接 Nest.js GraphQL 服务
const client = new ApolloClient({
  uri: 'http://localhost:3000/graphql',
  cache: new InMemoryCache()
});

function App() {
  return (
    <ApolloProvider client={client}>
      <Router>
        <Navbar />
        <div className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/user/:id" element={<UserProfile />} />
          </Routes>
        </div>
      </Router>
    </ApolloProvider>
  );
}

export default App;
  