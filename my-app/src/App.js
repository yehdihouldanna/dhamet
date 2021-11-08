import './App.css';
import Cell from './components/Cell';
import {DndProvider} from 'react-dnd';
import {HTML5Backend}  from 'react-dnd-html5-backend';
import React, { Component } from 'react';

class App extends Component {
  state = {
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
    player:0
  };
  render(){
    let Cells = [];
    let {board} = this.state;
    let len = board.length;
    for (let i = 0;i<len;i++)
    {
      for(let j = 0 ; j <len; j++)
      {
        Cells.push(
          <Cell key = {i.toString() +j.toString()} i={i} j={j} value = {board[i][j]} ></Cell>
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
