import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Chat from './components/Chat'


function App() {
    return (
        <BrowserRouter>
        <Routes> 
          <Route path="/" element={<Chat />} />
        </Routes>
      </BrowserRouter>
    );
}

export default App;
