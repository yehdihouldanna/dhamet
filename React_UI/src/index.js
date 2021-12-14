import React from 'react';
import ReactDOM from 'react-dom';
import '/static/css/index.css';
import App from './App';
import {BrowserRouter as Router} from "react-router-dom";
import {hashHistory} from "react-router"

let game_code = "";
try
{game_code = JSON.parse(document.getElementById('game_code').textContent);}
catch (e){console.log("This game page doesn't have an identifier.")}


// let username = "Guest";
// console.log("Getting Current usename for the GameApp");
// // let csrftoken = document.mainform.csrftoken.value;
// const requestOptions =
// {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json',
//                   "X-CSRFToken":document.getElementsByName('csrfmiddlewaretoken')[0].value },
//     body: JSON.stringify({
//     'username': "",
//     })
// };
// fetch('/DhametCode/username', requestOptions).
//     then((response) => response.json()).
//     then((data) => {
//         if (typeof data["Bad Request"] !="undefined") {console.log("Invalid Data : Ignored!");}
//         else {username = data.username;

//             console.log("['f': fetch]['user': ",username,"]");
//         }
//     });

// console.log("['f': main]['user': ",username,"]");


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

