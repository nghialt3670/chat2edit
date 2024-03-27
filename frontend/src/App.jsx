import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Chat from './components/Chat'
import Edit from './components/Edit';

function App() {
    return (
        <BrowserRouter>
        <Routes> 
          <Route path="/" element={<Chat />} />
          <Route path='/edit' element={<Edit />} />
        </Routes>
      </BrowserRouter>
    );
}

export default App;
