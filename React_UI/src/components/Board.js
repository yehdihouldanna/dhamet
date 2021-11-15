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
      board : [
      [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
      [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
      [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
      [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
      [ 1,  1,  1,  1,  0, -1, -1, -1, -1],
      [-1, -1, -1, -1, -1, -1, -1, -1, -1],
      [-1, -1, -1, -1, -1, -1, -1, -1, -1],
      [-1, -1, -1, -1, -1, -1, -1, -1, -1],
      [-1, -1, -1, -1, -1, -1, -1, -1, -1]],
      player:0,
      Code : "",
      board_txt:"wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
      move : "",
      timer : 0,
      delay : 200,
      prevent : false,
      MouseOnBoard:true,
    }; 
    // Biding Events handlers : 
    this.handleMove  = this.handleMove.bind(this);
    this.handleHover = this.handleHover.bind(this);
    this.handleStartMove = this.handleStartMove.bind(this);
    
    this.handleClick = this.handleClick.bind(this);
    this.handleMouseLeave = this.handleMouseLeave.bind(this);


    this.doClickAction = this.doClickAction.bind(this);
    this.doDoubleClickAction = this.doDoubleClickAction.bind(this);
    // Binding request handlers : 
    this.CreateGameRequest= this.CreateGameRequest.bind(this);
    this.MoveRequest = this.MoveRequest.bind(this);

    // Binding extra util methods
    this.serialize= this.serialize.bind(this);
    this.deserialize= this.deserialize.bind(this);
  };

  //------------------------------------------
  //Utils Methods : 
  //------------------------------------------
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
  };
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
  };

  //---------------------------------------------------------------------------------------
  // "Click Vs DoubleClick"  Handling :
  //---------------------------------------------------------------------------------------
  doClickAction(key) {
    if (!this.state.move.slice(-5).includes(key) && !this.state.move!=="")
      {this.state.move +=" "+key;}
    console.log("current move : ",this.state.move);
  };
  doDoubleClickAction(key) {
    if (!this.state.move.slice(-5).includes(key) && !this.state.move!=="")
      {this.state.move +=" "+key;}
    this.handleMove() ;
  };
  handleClick(e,key) {
      if (e.detail>1)
      {
        this.doDoubleClickAction(key);
      }
      else
      {
        this.doClickAction(key);
      }  
    };
  
  //-------------------------------------------------
  // Main Handler methods :
  //--------------------------------------------------
  handleStartMove(piece_key)
  {this.state.move=piece_key;
    // console.log("handleStartMove got called ! the move now is : ",this.state.move);
  }
  handleHover(cell_key)
  {
    if (!this.state.move.slice(-5).includes(cell_key) && !this.state.move!=="")
      {this.state.move +=" "+cell_key[0].toString()+cell_key[1].toString();}
    // console.log("handleHover got called the move now is : ",this.state.move);
  }
  handleMove() 
  {if (this.state.move.length){this.MoveRequest(this.state.move);}};

  //-----------------------------------------------------------------------
  // Handling Request and getting the reponses from the back end methods :
  //-----------------------------------------------------------------------
  MoveRequest(move_str)
  { 
    /*This function communicate with the makeGameMove view in the 
      back end to update the board appopriatly after a move*/

    console.log("Code:",this.state.Code);
    if (this.state.Code==="")
    {this.CreateGameRequest();}
    else if(move_str.length>=5)
    {
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
                {console.log("Invalid Move : Ignored!");
                this.state.move = "";
                }
                else // to solve the problem of the fetch getting called twice.
                {
                  console.log(data);
                  let game_state = this.state;
                  game_state.player=game_state.player===0? 1 :0;
                  console.log("The player now is : ",game_state.player);
                  game_state.board_txt = data.State;
                  this.setState(game_state);
                  this.deserialize(data.State);
                  this.state.move = "";
                }
              }
      );
    }
  };
  CreateGameRequest()
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
          let game_state = this.state;
          game_state.Code = data.Code;
          this.setState(game_state);
          console.log("Create successfully a game who's code is :",data.Code)
        }).then(()=>this.handleMove())
  };
  handleMouseLeave()
  {
    console.log("On Mouse Leave got called")
    this.state.move="";
  }
  // --------------------------------------------------------------------------------
  // Rendering React native method :
  //------------------------------------------------------------------------------
  render()
  {
    let Cells = [];
    let {board} = this.state;
    let len = board.length;
    for (let i = len-1;i>=0;i--)
    {
      for(let j = 0 ; j <len; j++)
      {
        let key = i.toString() +j.toString();
        Cells.push(
          <Cell 
            key={key} 
            i={i} 
            j={j} 
            value = {board[i][j]} 
            player={this.state.player} 
            move = {this.state.move} 
            onMove={this.handleMove} 
            onHover={this.handleHover}
            onStartMove ={this.handleStartMove}
            onClick={this.handleClick} 
          >
          </Cell>
        );
      }
    }
  return (
      <DndProvider backend={HTML5Backend}>
        <div id="board" onMouseLeave={this.handleMouseLeave}>
          {Cells}
      </div>
      < div>The current player is {this.state.player}</div>
    </DndProvider>
    );
  };
}

export default Board;