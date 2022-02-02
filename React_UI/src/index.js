import React from 'react';
import ReactDOM from 'react-dom';
import '/static/css/index.css';
import App from './App';
import {HashRouter,BrowserRouter as Router} from "react-router-dom";

let game_code = "";
try
{game_code = JSON.parse(document.getElementById('game_code').textContent);}
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
  <Router history = {HashRouter}>
    <App client={client} game_code={game_code}/>
  </Router>,
  document.getElementById('dhamet_container')
);

