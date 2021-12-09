import React from 'react';
import ReactDOM from 'react-dom';
import '/static/css/index.css';
import App from './App';
import {BrowserRouter as Router} from "react-router-dom";
import {hashHistory} from "react-router"

let game_code = "";
try
{
  game_code = JSON.parse(document.getElementById('game_code').textContent);
}
catch (e){console.log("This game page doesn't have an identifier.")}
const client = new WebSocket(
    'ws://'
    + window.location.host
    + '/DhametCode/'
    + 'move/'
    + game_code
    + '/'
  );

ReactDOM.render(
  // <React.StrictMode>
  // <HashRouter>
    // <App/>
  // </HashRouter>
  <Router history = {hashHistory}>
    <App client={client} game_code={game_code}/>
  </Router>

  // </React.StrictMode>
  ,
  document.getElementById('dhamet_container')
);

