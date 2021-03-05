import logo from './logo.svg';
import './App.css';
import Home from './components/Home'
import { BrowserRouter, Switch, Route } from 'react-router-dom'
import AboutUs from './components/AboutUs'
import Login from './components/Login'

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Switch>
          <Route path="/aboutus">
              <AboutUs/>
          </Route>
          <Route path="/login">
              <Login/>
          </Route>
          <Route path="/">
              <Home/>
          </Route>
        </Switch>
      </div>
    </BrowserRouter>
    
  );
}

export default App;
