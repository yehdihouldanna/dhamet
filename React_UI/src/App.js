//------------------------------------------------
// Copyrigh (c) SMART Solutions SM SA® 2021.
// All rights reserved.
// Code made by : Yehdhih ANNA (TheLuckyMagician).
//------------------------------------------------

import React, { Component } from 'react';
import Board from './components/Board';
import { Routes, Route } from "react-router-dom";

class App extends Component
{
    render()
    {
        return (
                <Routes>
                    <Route exact path = "/" element = {<p>This is the home page go to /game for the board</p>}></Route>

                    <Route exact path = "/game"
                            element = {<Board client={this.props.client}
                                              game_code={this.props.game_code}
                                       />} >
                     </Route>

                    <Route exact path = "/game/*"
                            element = {<Board client={this.props.client}
                                              game_code={this.props.game_code}
                                       />} >

                    </Route>

                    <Route exact path = "/main/"
                            element = {<Board client={this.props.client}
                            game_code={this.props.game_code}
                            />} >
                    </Route>
                    <Route exact path = "/main/game"
                            element = {<Board client={this.props.client}
                            game_code={this.props.game_code}
                            />} >
                    </Route>
                    <Route exact path = "/main/game/*"
                            element = {<Board client={this.props.client}
                            game_code={this.props.game_code}
                            />} >
                    </Route>
                </Routes>
        );
    }
}
export default App;
