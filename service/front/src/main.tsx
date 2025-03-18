import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
// import './index.css'
import App from './App.tsx'
0
import Test from './components/Test'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    {/* <App /> */}
    <Test/>
  </StrictMode>,
)
