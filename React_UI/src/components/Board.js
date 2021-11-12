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
      player:0,
      Code : "",
      board_txt:"wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    };
    this.handleMove= this.handleMove.bind(this);
    this.Create_game= this.Create_game.bind(this);
    this.serialize= this.serialize.bind(this);
    this.deserialize= this.deserialize.bind(this);
  }

  serialize()
  {
    let str = ""
    for(let i =0;i<9;i++)
    {
      for(let j =0;j<9;j++)
      {
        if (this.state.board[i][j]===-1)
        {
          str+="b";
        }
        else if(this.state.board[i][j]===-3)
        {
          str+="B";
        }
        else if(this.state.board[i][j]===0)
        {
          str+="_";
        }
        else if(this.state.board[i][j]===1)
        {
          str+="w";
        }
        else if(this.state.board[i][j]===3)
        {
          str+="W";
        }
      }
    }
    return str
  }

  deserialize(text)
  {
    let game_state=this.state
    let k=0;
    for(let i =0;i<9;i++)
    {
      for(let j =0;j<9;j++)
      {
        if     (text[k]==="b") game_state.board[i][j]=-1;
        else if(text[k]==="B") game_state.board[i][j]=-3;
        else if(text[k]==="_") game_state.board[i][j]=0;
        else if(text[k]==="w") game_state.board[i][j]=1;
        else if(text[k]==="W") game_state.board[i][j]=3;
        k+=1;
      }
    }
    this.setState(game_state)
  }

  handleMove(from,to) 
  {
    // console.log("handleMove got invoked",from,to);
    if (typeof from != "undefined" && typeof to != "undefined")
    {
      this.MoveRequest(from,to);
      
    }
  }
  MoveRequest(from,to)
  {
    console.log("Code:",this.state.Code);
    if (this.state.Code==="")
    {this.Create_game();}
    else
    {
      let move_str = from[0].toString()+from[1].toString()+" "+to[0].toString()+to[1].toString();
      console.log("Trying the move : ",move_str);
      const requestOptions=
      {
        method : 'POST',
        headers : {'Content-Type':'application/json'},
        body: JSON.stringify({
          'Code':this.state.Code,
          'State': this.state.board_txt,
          'last_move': move_str,
          'Current_Player':this.state.player,
    })
      };
      fetch('/DhametCode/move',requestOptions).
        then((response)=> response.json()).
        then((data)=> 
              { 
                if (typeof data["Bad Request"] != "undefined")
                {
                  console.log("Invalid Move : Ignored!")
                }
                else
                {
                  console.log("Receiving data after the move request:")
                  console.log("-----------------------")
                  console.log(data);
                  let game_state = this.state;
                  
                  game_state.player=game_state.player===0? 1 :0;
                  game_state.board_txt = data.State;
                  this.setState(game_state);
                  this.deserialize(data.State);
                  console.log("-----------------------")
                }
                

                
                // game_state.board[to[0]][to[1]]  = game_state.board[from[0]][from[1]] ;
                // game_state.board[from[0]][from[1]] =0;
                // game_state.player = game_state.player===0? 1 :0;
                // this.setState(game_state);

                // let game_state = this.state;
                // console.log(game_state);
                // game_state.board[to[0]][to[1]]  = game_state.board[from[0]][from[1]] ;
                // game_state.board[from[0]][from[1]] =0;
                // game_state.player = game_state.player===0? 1 :0;
                // this.setState(game_state);
              }
      
      );

    }
    
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
          let game_state = this.state;
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