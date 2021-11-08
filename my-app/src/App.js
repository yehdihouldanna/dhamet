//------------------------------------------------
// Copyrigh (c) SMART Solutions SM SA® 2021.
// All rights reserved.
// Code made by : Yehdhih ANNA (TheLuckyMagician).
//------------------------------------------------

import './App.css';
import Cell from './components/Cell';
import {DndProvider} from 'react-dnd';
import {HTML5Backend}  from 'react-dnd-html5-backend';
import React, { Component } from 'react';
class App extends Component {
  constructor() 
  {
    super();
    this.state = {
      board : 
      [[ 1,  1,  1,  1,  1,  1,  1,  1,  1],
      [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
      [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
      [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
      [ 1,  1,  1,  1,  0, -1, -1, -1, -1],
      [-1, -1, -1, -1, -1, -1, -1, -1, -1],
      [-1, -1, -1, -1, -1, -1, -1, -1, -1],
      [-1, -1, -1, -1, -1, -1, -1, -1, -1],
      [-1, -1, -1, -1, -1, -1, -1, -1, -1,]],
      // board : 
      // [[ 1,  1,  1,  1,  1,  1,  1,  1,  1],
      // [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
      // [ 0,  0,  0,  0,  1,  0,  1,  1,  1],
      // [ 0,  0,  0, -1,  0,  0,  1,  1,  1],
      // [ 0,  0, -1,  0,  0,  0, -1, -1, -1],
      // [ 0,  0,  0,  0, -1, -1, -1, -1, -1],
      // [ 0,  0,  0, -1, -1,  0, -1, -1, -1],
      // [ 0, -1, -1, -1, -1, -1, -1, -1, -1],
      // [ 3, -1, -1, -1, -1, -1, -1, -1, -1]],
      player:1
    };

    this.handleMove= this.handleMove.bind(this);
  }
  

  handleMove(from,to) 
  {
    // console.log("handleMove got invoked",from,to);
    if (typeof from != "undefined" && typeof to != "undefined")
    {
      let game_state = this.state;
      console.log(game_state);
      game_state.board[to[0]][to[1]]  = game_state.board[from[0]][from[1]] ;
      game_state.board[from[0]][from[1]] =0;
      game_state.player = game_state.player===0? 1 :0;
      this.setState(game_state);
    }
  }

  render(){
    let Cells = [];
    let {board} = this.state;
    let len = board.length;
    for (let i = len-1;i>=0;i--)
    {
      for(let j = 0 ; j <len; j++)
      {
        Cells.push(
          <Cell key = {i.toString() +j.toString()} i={i} j={j} value = {board[i][j]} player={this.state.player} onMove={this.handleMove}></Cell>
        );
      }
    }
  return (
      <DndProvider backend={HTML5Backend}>
        <div id="board">
          {Cells}
      </div>
    </DndProvider>
    );
  }
}
export default App;
