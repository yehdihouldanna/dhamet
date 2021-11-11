//------------------------------------------------
// Copyrigh (c) SMART Solutions SM SA® 2021.
// All rights reserved.
// Code made by : Yehdhih ANNA (TheLuckyMagician).
//------------------------------------------------

import '/static/css/Board.css';
import Cell from './Cell';
import {DndProvider} from 'react-dnd';
import {HTML5Backend}  from 'react-dnd-html5-backend';
import React, { Component } from 'react';

class Board extends Component {
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
      player:0,
      Code : "",
    };

    this.handleMove= this.handleMove.bind(this);
    this.Create_game= this.Create_game.bind(this);
  }
  handleMove(from,to) 
  {
    // console.log("handleMove got invoked",from,to);
    if (typeof from != "undefined" && typeof to != "undefined")
    {
      if (this.state.Code == "")
      {
        this.Create_game();
      }
      
      let move_str = from[0].toString+from[1].toString+" "+to[0].toString()+to[1].toString()
      this.MoveRequest(
            {
                'Code':this.state.Code,
                'State': {'board': this.state.board},
                'Player':this.state.player,
                'Move': move_str,
           })
      let game_state = this.state;
      console.log(game_state);
      game_state.board[to[0]][to[1]]  = game_state.board[from[0]][from[1]] ;
      game_state.board[from[0]][from[1]] =0;
      game_state.player = game_state.player===0? 1 :0;
      this.setState(game_state);
    }
  }
  MoveRequest(from,to)
  {
    console.log("Code:",this.state.Code);
    if (this.state.Code==="")
    {return}
    const requestOptions=
    {
      method : 'POST',
      headers : {'Content-Type':'application/json'},
      body: JSON.stringify({
        'source' : from,
        'to' : to
      })
    };
    fetch('/DhametCode/move',requestOptions).
      then((response)=> response.json()).
      then((data)=> 
            { 
              console.log("Receiving data after the move request:")
              console.log(data);
              // game_state.board[to[0]][to[1]]  = game_state.board[from[0]][from[1]] ;
      // game_state.board[from[0]][from[1]] =0;
      // game_state.player = game_state.player===0? 1 :0;
      // this.setState(game_state);
            }
      
      );
  };
  Create_game()
  {
    const requestOptions=
    {
      method : 'POST',
      headers : {'Content-Type':'application/json'},
      body: JSON.stringify({
        Code : "",
        player1 : "Dummy",
        player2 : "Random",
      })
    };
    fetch('/DhametCode/create-game',requestOptions).
      then((response)=> response.json()).
      then((data)=> {
          console.log("The returned data is :: :",data)
          game_state = this.state;
          game_state.Code = data.Code;
          this.setState(game_state);
          console.log("Create successfully a game who's code is :",data.Code)
        })
  };

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
export default Board;