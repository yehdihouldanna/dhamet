//------------------------------------------------
// Copyrigh (c) SMART Solutions SM SA® 2021.
// All rights reserved.
// Code made by : Yehdhih ANNA (TheLuckyMagician).
//------------------------------------------------

// import '/static/css/App.css';
import React, { Component } from 'react';
import Board from './components/Board';
import { Routes, Route , Link, Redirect} from "react-router-dom";

class App extends Component 
{
    render()
    {
        return (
        // <Board/>
            <Routes>
                <Route exact path = "/" element = {<p>This is the home page go to /game for the board</p>}></Route>
                <Route exact path = "/game" element = {<Board/>} ></Route>
            </Routes>
        );
    }
}
export default App;
