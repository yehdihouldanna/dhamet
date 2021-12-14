//------------------------------------------------
// Copyrigh (c) SMART Solutions SM SA® 2021.
// All rights reserved.
// Code made by : Yehdhih ANNA (TheLuckyMagician).
//------------------------------------------------

//@ts-check
import '/static/css/Board.css';
import Cell from './Cell';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import React, { Component, useReducer } from 'react';


class Board extends Component {
  constructor(props) {
    super();
    this.state = {
      board : [
        [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
        [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
        [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
        [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
        [-1, -1, -1, -1,  0,  1,  1,  1,  1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1]],
      player: 0,
      Code: props.game_code,
      Client : props.client,
      board_txt: "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbbbb_wwwwbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
      previous_board : "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbbbb_wwwwbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
      move: "",
      last_move :"",
      move_history_render:[],
      creator   :"",
      opponent  :"",
      winner : "",
      timer: 0,
      delay: 200,
      prevent: false,
      MouseOnBoard: true,
      username : "",
    };
    // Biding Events handlers :
    this.handleMove = this.handleMove.bind(this);
    this.handleHover = this.handleHover.bind(this);
    this.handleStartMove = this.handleStartMove.bind(this);

    this.handleClick = this.handleClick.bind(this);
    this.handleMouseLeave = this.handleMouseLeave.bind(this);

    this.doClickAction = this.doClickAction.bind(this);
    this.doDoubleClickAction = this.doDoubleClickAction.bind(this);
    // Binding request handlers :
    this.CreateGameRequest = this.CreateGameRequest.bind(this);
    this.MoveRequest = this.MoveRequest.bind(this);
    this.MoveRequest_ws = this.MoveRequest_ws.bind(this);
    this.getUserNameRequest = this.getUserNameRequest.bind(this);
    // Binding extra util methods
    this.serialize = this.serialize.bind(this);
    this.deserialize = this.deserialize.bind(this);

    this.update_moves_time_line = this.update_moves_time_line.bind(this);
    this.add_one_history_item = this.add_one_history_item.bind(this);
  };
  //------------------------------------------
  //Utils Methods :
  //------------------------------------------
  serialize() {
    let str = ""
    for (let i = 0; i < 9; i++) {
      for (let j = 0; j < 9; j++) {
        if (this.state.board[i][j] === -1) {
          str += "b";
        }
        else if (this.state.board[i][j] === -3) {
          str += "B";
        }
        else if (this.state.board[i][j] === 0) {
          str += "_";
        }
        else if (this.state.board[i][j] === 1) {
          str += "w";
        }
        else if (this.state.board[i][j] === 3) {
          str += "W";
        }
      }
    }
    return str
  };
  deserialize(text) {
    let game_state = this.state
    let k = 0;
    for (let i = 0; i < 9; i++) {
      for (let j = 0; j < 9; j++) {
        if (text[k] === "b") game_state.board[i][j] = -1;
        else if (text[k] === "B") game_state.board[i][j] = -3;
        else if (text[k] === "_") game_state.board[i][j] = 0;
        else if (text[k] === "w") game_state.board[i][j] = 1;
        else if (text[k] === "W") game_state.board[i][j] = 3;
        k += 1;
      }
    }
    this.setState(game_state)
  };
  //-------------------------------------------------
  // "Click Vs DoubleClick"  Handling :
  //---------------------------------------------------------------------------------------
  doClickAction(key,piece_present) {
    if (this.state.move === "" && piece_present) { this.state.move = key;}
    else if (this.state.move.length>=2) // switching the selected piece
    {
      let len = this.state.move.length;
      let x = Number(this.state.move[len-2])
      let y = Number(this.state.move[len-1])
      let xc = Number(key[0])
      let yc = Number(key[1])

      if (this.state.board[x][y]*this.state.board[xc][yc]>=1 )  // checks if the cellls the two pieces are of the same type
      {this.state.move = key;}
      }
    if (!this.state.move.slice(-5).includes(key) && this.state.move !== "")
    { this.state.move += " " + key; }
    console.log("current move : ", this.state.move);
    let game_state = this.state;
    game_state.move = this.state.move;
    this.setState(game_state);
  };
  doDoubleClickAction(key,piece_present) {
    if (this.state.move.length>=5)
    {
      console.log("This condition got invoked!");
      console.log("key: ",key,"Move:",this.state.move);
      // if the user double click his piece and double click on another piece of his
      let len = this.state.move.length;
      let x = Number(this.state.move[len-5])
      let y = Number(this.state.move[len-4])
      let xc = Number(key[0])
      let yc = Number(key[1])

      if (this.state.board[x][y]*this.state.board[xc][yc]>=1 ) // checks if the two cells containt pieces of the same type
      { console.log("The indices we are trying : ",x,y,xc,yc, "are equal")
        this.state.move = ""
        let game_state = this.state;
        game_state.move = this.state.move;
        this.setState(game_state);
        return;}
    }
    if (!this.state.move.slice(-5).includes(key) && this.state.move !== "")
    { this.state.move += " " + key;
      let game_state = this.state;
      game_state.move = this.state.move;
      this.setState(game_state);
    }
    this.handleMove();


  };
  handleClick(e, key,piece_present) {
    if (e.detail > 1) {
      this.doDoubleClickAction(key,piece_present);
    }
    else {
      this.doClickAction(key,piece_present);
    }
  };
  //-------------------------------------------------
  // Main Handler methods :
  //-------------------------------------------------

  handleStartMove(piece_key) {
    this.state.move = piece_key;
    console.log(this.state.move)
  }
  handleHover(cell_key) {
    if (!this.state.move.slice(-5).includes(cell_key) && this.state.move !== "") { this.state.move += " " + cell_key[0].toString() + cell_key[1].toString(); }
    // console.log("handleHover got called the move now is : ",this.state.move);
  }
  handleMove() {
    if (this.state.move.length) {
      if(this.state.AI)
      {
        console.log("We are calling the view for AI.")
        this.MoveRequest(this.state.move);
      }
      else
      {
        console.log("We are calling websocket")
        this.MoveRequest_ws(this.state.move);
      }
    }
  };
  //-----------------------------------------------------------------------
  // Handling Request and getting the reponses from the back end methods :
  //-----------------------------------------------------------------------
  MoveRequest(move_str) {
    /*This function communicate with the makeGameMove view in the
      back end to update the board appopriatly after a move it is used
      in games vs AI only as it doesnt require a websocket to play vs AI.
      */

      if (move_str.length >= 5) {
      console.log("Trying the move : ", move_str);
      const requestOptions =
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json',
                    "X-CSRFToken": '{{ csrf_token }}' },
        body: JSON.stringify({
          'id': this.state.Code,
          'state': this.state.board_txt,
          'last_move': move_str,
          'current_turn': this.state.player,
          'winner':"",
        })
      };
      fetch('/DhametCode/move', requestOptions).
        then((response) => response.json()).
        then((data) => {
          if (typeof data["Bad Request"] != "undefined") {
            console.log("Invalid Move : Ignored!");
            this.state.move = "";
          }
          else // to solve the problem of the fetch getting called twice.
          {
            console.log(data);
            let game_state = this.state;
            game_state.player = game_state.player === 0 ? 1 : 0;
            console.log("The player now is : ", game_state.player);
            game_state.board_txt = data.state;
            this.setState(game_state);
            this.deserialize(data.state);
            this.state.move = "";
          }
        }
        );
    }
  };
  MoveRequest_ws(move_str) {
    /**
     * * This function communicate with the GameMoveConsumer in the backend
    **/
    console.log("a move request");
    console.log("Code:", this.state.Code);
    if (this.state.Code === "") {
      this.CreateGameRequest();
    }
    else if (move_str.length >= 5) {

      console.log("Trying the move : ", move_str);
        this.props.client.send(
        JSON.stringify({
          'id': this.state.Code,
          'state': this.state.board_txt,
          'last_move': move_str,
          'current_turn': this.state.player,
          'winner':"",
        }));
      {
      }
    }
  };
  CreateGameRequest(name) {
    console.log("Starting a game vs another local player.")
    const requestOptions =
    {
      method: 'POST',
      headers: { 'X-CSRFToken' : "{{csrf_token}}" },
      body: JSON.stringify({
        "id": "",
        "creator": "",
        "opponent": "",
      })
    };
    fetch('/DhametCode/create-game', requestOptions).
      then((response) => response.json()).
      then((data) => {
        let game_state = this.state;
        game_state.Code = data.Code;
        game_state.creatro = data.creator
        game_state.opponent = data.opponent
        this.setState(game_state);
        console.log("Create successfully a game who's code is :", data.Code)
      }).then(() => this.handleMove())
  };
  handleMouseLeave() {
    // console.log("On Mouse Leave got called");
    this.state.move = "";
    let game_state = this.state;
    game_state.move = this.state.move;
    this.setState(game_state);
  }
  getUserNameRequest()
  {
    let me = this;
    let username = "Guest";
    console.log("Getting Current usename for the GameApp");
    const requestOptions =
    {method: 'POST',
        headers: { 'Content-Type': 'application/json',
                      // @ts-ignore
                      "X-CSRFToken":document.getElementsByName('csrfmiddlewaretoken')[0].value },
        body: JSON.stringify({'username': ""})
    };
    fetch('/DhametCode/username', requestOptions).
        then((response) => response.json()).
        then((data) => {
            if (typeof data["Bad Request"] !="undefined") {console.log("Invalid Data : Ignored!");}
            else {username = data.username;
                // console.log("['f': fetch]['user': ",username,"]");
                me.state.username = username;
            }
        });
    // console.log("['f': getUserNameRequest]['user': ",username,"]");
    // console.log("['_': state]['user': ",this.state.username,"]");
  }
  // Componenets Native methods :
  componentWillMount() {
        this.getUserNameRequest();
        this.props.client.onopen = () => {
          console.log('A new client Connected');
          this.props.client.send(
            JSON.stringify({
              'id': this.state.Code,
              'state': this.state.board_txt,
              'last_move': this.state.move,
              'current_turn': this.state.player,
              'creator': this.state.creator,
              'creator_score': "",
              'opponent' : this.state.opponent,
              'opponent_score': "",
              'winner': this.state.winner,
              'winner_score': "",
            }));
        };
        let me = this;
          this.props.client.onmessage = function (e) {
            const data = JSON.parse(e.data);
            var moved = false;
            if (typeof data["Bad Request"] != "undefined") {
              console.log("Invalid Move : Ignored!");
              me.state.move = "";
            }
            else {
                let AI_NAMES = ["AI_Random","AI_Dummy","AI_MinMax"];
                console.log("We received a correct data: ", data);
                let game_state = me.state;
                game_state.player = data.current_turn;
                // console.log("The winner returned is : ",data.winner)
                console.log("The player now is : ", game_state.player);
                game_state.board_txt = data.state;
                if (game_state.last_move != data.last_move )
                {
                  game_state.last_move = data.last_move;
                  game_state.move_history_render.push(game_state.last_move);
                  me.setState(game_state);
                  if (game_state.move_history_render.length==2)
                  {
                    me.update_moves_time_line();
                    me.state.move_history_render=[];
                  }
                  me.deserialize(data.state);
                }
                me.state.move = "";
                if (data.winner!==null && data.winner!=="")
                {// TODO : change this to a better thing.
                    alert(data.winner + " Won the game!");
                    me.state.winner = data.winner
                }
                if (data.opponent !== me.state.opponent)
                {
                    me.state.opponent = data.opponent;
                    me.state.creator  = data.creator;
                    console.log("['f': move]['state' : ",me.state,"]");
                  if (data.opponent === me.state.username)
                  {
                    document.getElementById("player2_name").innerHTML       = data.creator;
                    document.getElementById("player2_score").innerHTML = data.creator_score;
                    document.getElementById("player1_name").innerHTML       = data.opponent;
                    document.getElementById("player1_score").innerHTML = data.opponent_score;
                    document.getElementById("player1").style.backgroundColor  = "rgb(156,108,20)";
                    document.getElementById("player2").style.backgroundColor  = "rgb(76,52,36)";
                  }
                  else if (data.creator === me.state.username)
                  {
                    document.getElementById("player1_name").innerHTML       = data.creator;
                    document.getElementById("player1_score").innerHTML = data.creator_score;
                    document.getElementById("player2_name").innerHTML       = data.opponent;
                    document.getElementById("player2_score").innerHTML = data.opponent_score;
                    document.getElementById("player1").style.backgroundColor  = "rgb(76,52,36)";
                    document.getElementById("player2").style.backgroundColor  = "rgb(156,108,20)";
                  }
                }

                // * If We are playing vs AI then we will send it's request after the player's
                if( AI_NAMES.includes(me.state.opponent) && me.state.player===1)
                {
                    setTimeout(() => {
                    // * We can change the response time based on the need
                    if (me.state.previous_board != me.state.board_txt) {
                        console.log("The AI request waited for 350 ms !")
                        me.props.client.send(
                        JSON.stringify({
                            'id': me.state.Code,
                            'state': me.state.board_txt,
                            'last_move': "",
                            'current_turn': me.state.player,
                            'winner':"",
                        }));
                    }
                        }, 350);
                    }
                }
          };
          this.props.client.onclose = function (e) {
          console.error('Client socket closed unexpectedly');
        };
    }
  //----------------------------------------
  // Web Page modifiers :
  //----------------------------------------
  add_one_history_item(content,color)
  {
    console.log("Adding a history item")
    // colors: [blue:"text_primary",yellow: "text-warning",red:"text-danger",green:"text_success"]
    let time_line_item = document.createElement("div");
      // mb for margin bottom
      time_line_item.classList.add("timeline-item","mb-2");

      let time_label = document.createElement("div");
      time_label.classList.add("timeline-label", "fw-bolder", "text-gray-800", "fs-6");
      var today = new Date();
      // var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
      var time = today.getMinutes() + ":" + today.getSeconds();
      time_label.innerHTML = time;
      let badge = document.createElement("div");
      badge.classList.add("timeline-badge");
      let icon = document.createElement("i");
      let icon_class = "text-"+color;
      icon.classList.add("fa", "fa-genderless", icon_class ,"fs-1");
      badge.appendChild(icon)

      let move_div = document.createElement("div");
      move_div.classList.add("fw-mormal", "timeline-content", "text-muted", "ps-3");
      move_div.innerHTML=content;

      time_line_item.appendChild(time_label);
      time_line_item.appendChild(badge);
      time_line_item.appendChild(move_div);

      document.getElementById("MovesContainer").appendChild(time_line_item);
  }
  update_moves_time_line()
  {
    this.add_one_history_item(this.state.move_history_render[0],"dark");
    this.add_one_history_item(this.state.move_history_render[1],"secondary");
  }
  // --------------------------------------
  // Rendering React native method :
  //---------------------------------------
  render() {
    let Cells = [];
    let { board } = this.state;
    let len = board.length;

    if(this.state.opponent === this.state.username)
    {
        for (let i = 0; i < len; i++) {
            for (let j = 0; j < len; j++) {
              let key = i.toString() + j.toString();
              let ex_css_class="";
              if (this.state.last_move.includes(key))
              {
                ex_css_class = " highlight_last_move";
              }
              Cells.push(
                <Cell
                  key={key}
                  i={i}
                  j={j}
                  value={board[i][j]}
                  player={this.state.player}
                  move={this.state.move}
                  onMove={this.handleMove}
                  onHover={this.handleHover}
                  onStartMove={this.handleStartMove}
                  onClick={this.handleClick}
                  ex_css_class ={ex_css_class}
                  toggle = {this.state.move.includes(key)}
                >
                </Cell>
              );
            }
          }
    }
    else
    {

        for (let i = len - 1; i >= 0; i--) {
          for (let j = 0; j < len; j++) {
            let key = i.toString() + j.toString();
            let ex_css_class="";
            if (this.state.last_move.includes(key))
            {
              ex_css_class = " highlight_last_move";
            }
            Cells.push(
              <Cell
                key={key}
                i={i}
                j={j}
                value={board[i][j]}
                player={this.state.player}
                move={this.state.move}
                onMove={this.handleMove}
                onHover={this.handleHover}
                onStartMove={this.handleStartMove}
                onClick={this.handleClick}
                ex_css_class ={ex_css_class}
                toggle = {this.state.move.includes(key)}
              >
              </Cell>
            );
          }
        }
    }

    return (
      <DndProvider backend={HTML5Backend}>
        <div id="board"  onMouseLeave={this.handleMouseLeave}>
          {Cells}
        </div>
      </DndProvider>
    );
  };
}

export default Board;
