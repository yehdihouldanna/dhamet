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
      tier: null,
      //* Souffle parameters
      can_souffle:true,
      souffle_move : "",
      soufflables : [],
    };
    this.AI_NAMES  = ["AI_Random","AI_Dummy","AI_MinMax"];


    this.BOT_NAMES = ["Med10","Mariem","Sidi","احمد","Khadijetou","Cheikh","Vatimetou","ابراهيم",
                      "Mamadou","Oumar","Amadou","3abdellahi","Va6me","Moussa","Aly","Samba"];
    //* Tiers are the difficulty level, for now we have 3 tiers, 3 :AI_MinMax, 2 : Dummy, 1 : Random
    this.Tiers = [3,2,3,2,1,2,3,1,1,2,3,3,1,1,3,2];

    // Biding Events handlers :
    this.handleMove = this.handleMove.bind(this);
    this.handleHover = this.handleHover.bind(this);
    this.handleStartMove = this.handleStartMove.bind(this);

    this.handleClick = this.handleClick.bind(this);
    this.handleMouseLeave = this.handleMouseLeave.bind(this);
    this.handleSouffle = this.handleSouffle.bind(this);

    this.doClickAction = this.doClickAction.bind(this);
    this.doDoubleClickAction = this.doDoubleClickAction.bind(this);
    // Binding request handlers :
    this.CreateGameRequest = this.CreateGameRequest.bind(this);
    this.CreateFakeOpponent = this.CreateFakeOpponent.bind(this);
    this.MoveRequest_ws = this.MoveRequest_ws.bind(this);
    this.getUserNameRequest = this.getUserNameRequest.bind(this);
    // Binding extra util methods
    this.serialize = this.serialize.bind(this);
    this.deserialize = this.deserialize.bind(this);

    this.update_moves_time_line = this.update_moves_time_line.bind(this);
    this.add_one_history_item = this.add_one_history_item.bind(this);
  };
  //?------------------------------------------
  //* Utils Methods :
  //?------------------------------------------
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
  //?-------------------------------------------------
  // * "Click Vs DoubleClick"  Handling :
  //?-------------------------------------------------
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
    if (this.state.move.length==0 && piece_present ==2)
    {
        console.log("🚀 ~ file: Board.js ~ line 148 ~ Board ~ doDoubleClickAction ~ handleSouffle got called")
        this.handleSouffle(key);
    }
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
  handleClick(e, key,piece_state) {
      // * piece state: 0 (no piece in cell), (1 a piece in cell non souffle),(2 a souffle piece in cell)
    if (e.detail > 1) {
      this.doDoubleClickAction(key,piece_state);
    }
    else {
      this.doClickAction(key,piece_state);
    }
  };
  //?-------------------------------------------------
  // * Main Handler methods :
  //?-------------------------------------------------
  handleStartMove(piece_key) {
    this.state.move = piece_key;
    console.log(this.state.move)
  }
  handleHover(cell_key) {
    if (!this.state.move.slice(-5).includes(cell_key) && this.state.move !== "") { this.state.move += " " + cell_key[0].toString() + cell_key[1].toString(); }
    // console.log("handleHover got called the move now is : ",this.state.move);
  }
  handleMove() {
    if (this.state.move.length)
      {this.MoveRequest_ws(this.state.move,this.state.souffle_move);}
    console.log("🚀 ~ file: Board.js ~ line 188 ~ Board ~ handleMove")
  };
  //?-----------------------------------------------------------------------
  // * Handling Request and getting the reponses from the back end methods :
  //?-----------------------------------------------------------------------
  handleSouffle(piece_key)
  {
      console.log("in handle souffle")
    let i = parseInt(piece_key[0]);
    let j = parseInt(piece_key[1]);
    let game_state= this.state;
   game_state.souffle_move = piece_key;
    console.log("souffle contains now : ",game_state.souffle_move)
   game_state.can_souffle = false;
   game_state.soufflables = [];
   game_state.board[i][j] = 0;
   game_state.board_txt = this.serialize();
   game_state.move = "";
   this.setState(game_state);
  }
  is_player_turn()
  {
      if ((this.state.username === this.state.creator && this.state.player==0) || (this.state.username === this.state.opponent && this.state.player==1))
      {return true;}
      return false;
  }
  MoveRequest_ws(move_str,souffle_move) {
    console.log("🚀 ~ file: Board.js ~ line 248 ~ Board ~ MoveRequest_ws")
    // * This function communicate with the GameMoveConsumer in the backend
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
          'souffle_move':souffle_move,
          'current_turn': this.state.player,
          'winner':"",
        }));
      {
      }
    }
  };
  CreateFakeOpponent()
  {
    // creates a game with a fake opponenet if the player waited so long, without another human joining his game
    let me = this;
    let thisTimeout = setTimeout(() =>{
        console.log("🚀 ~ Waited 10s, Launching a fake opponent request")
        if ((me.state.opponent === ""))
            {CallFakeOpponent(me);}
        else
            { console.log("🚀 ~ file: Board.js ~ line 279 ~ Board ~ thisTimeout ~ Opponent does exist no need for fake")}
    }, 30000);

    function CallFakeOpponent(me) {
        clearTimeout(thisTimeout);
        console.log("🚀 ~ file: Board.js ~ line 285 ~ Board ~ CallFakeOpponent ~ 'Launched the request for fake opponenet'")
        let idx = Math.floor(Math.random() * me.BOT_NAMES.length);
        const requestOptions =
        {method: 'POST',
            headers: { 'Content-Type': 'application/json',
                        // @ts-ignore
                        "X-CSRFToken":document.getElementsByName('csrfmiddlewaretoken')[0].value },
            body: JSON.stringify({
                'id':me.state.id,
                'creator':me.state.creator,
                'opponent':me.BOT_NAMES[idx],
                'allow_fake':true,
                'tier': me.Tiers[idx],
            })
        };
        fetch('/DhametCode/create-game', requestOptions).
            then((response) => response.json()).
            then((data) => {
                if (typeof data["Bad Request"] !="undefined")
                {}
                else {

                    console.log("🚀 ~ file: Board.js ~ line 295 ~ Board ~ then ~ data", data)
                    me.state.opponent = data.opponent;
                    me.state.tier = me.Tiers[idx];
                    me.props.client.send(
                        JSON.stringify({
                          'id': me.state.Code,
                          'state': me.state.board_txt,
                          'last_move': me.state.move,
                          'souffle_move':me.state.souffle_move,
                          'current_turn': me.state.player,
                          'creator': me.state.creator,
                          'creator_score': "",
                          'opponent' : me.state.opponent,
                          'opponent_score': "",
                          'winner': me.state.winner,
                          'winner_score': "",
                          'tier': me.state.tier,
                        }));
                }
            });
        }
    }
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
                me.state.username = username;
                // console.log("🚀 ~ file: Board.js ~ line 351 ~ Board ~ then ~ username", username)
            }
        });
  }
  //?---------------------------------------------------------
  // * Component's Native methods :
  //?---------------------------------------------------------
  componentWillMount() {
        this.getUserNameRequest();
        this.CreateFakeOpponent();
        this.props.client.onopen = () => {
          console.log('A new client Connected');
          this.props.client.send(
            JSON.stringify({
              'id': this.state.Code,
              'state': this.state.board_txt,
              'last_move': this.state.move,
              'souffle_move':this.state.souffle_move,
              'current_turn': this.state.player,
              'creator': this.state.creator,
              'creator_score': "",
              'opponent' : this.state.opponent,
              'opponent_score': "",
              'winner': this.state.winner,
              'winner_score': "",
              'tier': "",
            }));
        };
        let me = this;
          this.props.client.onmessage = function (e) {

            const data = JSON.parse(e.data);
            let moved = false;
            if (typeof data["Bad Request"] != "undefined") {
              console.log("Invalid Move : Ignored!");
              me.state.move = "";
            }
            else { // *server returned a valid move :
                console.log("We received a correct data: ", data);
                let game_state = me.state;
                game_state.player = data.current_turn;
                console.log("The player now is : ", game_state.player);
                game_state.board_txt = data.state;
                game_state.soufflables = data.soufflables;
                if(game_state.soufflables.length)
                {
                    game_state.can_souffle= true;
                }
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
                {
                    // TODO : change this to a better thing.
                    alert(data.winner + " Won the game!");
                    me.state.winner = data.winner
                }

                if (data.opponent !== me.state.opponent)
                {
                    me.state.opponent = data.opponent;
                    me.state.creator  = data.creator;
                    me.state.tier = data.tier===0? null : data.tier;
                    console.log("🚀 ~ file: Board.js ~ line 425 ~ Board ~ componentWillMount ~ state", me.state)
                  if (data.opponent === me.state.username)
                  {
                    document.getElementById("player2_name").innerHTML       = data.creator;
                    document.getElementById("player2_score").innerHTML = data.creator_score;
                    document.getElementById("player1_name").innerHTML       = data.opponent;
                    document.getElementById("player1_score").innerHTML = data.opponent_score;

                    document.getElementById("player1").style.backgroundColor  = "rgb(156,108,20)";
                    document.getElementById("player2").style.backgroundColor  = "rgb(76,52,36)";

                    // document.getElementById("timer_p1").style.backgroundColor = "rgb(156,108,20)";
                    // document.getElementById("timer_p2").style.backgroundColor = "rgb(76,52,36)";
                  }
                  else if (data.creator === me.state.username)
                  {
                    document.getElementById("player1_name").innerHTML       = data.creator;
                    document.getElementById("player1_score").innerHTML = data.creator_score;
                    document.getElementById("player2_name").innerHTML       = data.opponent;
                    document.getElementById("player2_score").innerHTML = data.opponent_score;

                    document.getElementById("player1").style.backgroundColor  = "rgb(76,52,36)";
                    document.getElementById("player2").style.backgroundColor  = "rgb(156,108,20)";

                    // document.getElementById("timer_p1").style.backgroundColor = "rgb(76,52,36)";
                    // document.getElementById("timer_p2").style.backgroundColor =  "rgb(156,108,20)";
                  }
                }

                // * If We are playing vs AI then we will send it's request after the player's
                if( me.AI_NAMES.includes(me.state.opponent) && me.state.player===1)
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
                            'souffle_move':"",
                            'current_turn': me.state.player,
                            'winner':"",

                        }));
                    }
                        }, 350);
                    }

                // * If the player is playing vs a Bot
                if( me.state.tier!==null && me.state.player===1)
                {
                    let delay = 350 + Math.floor(Math.random() * 10000) // randomizing the time of the response
                    setTimeout(() => {
                    // * We can change the response time based on the need
                    if (me.state.previous_board != me.state.board_txt) {
                        console.log("The AI request waited for 350 ms !")
                        me.props.client.send(
                        JSON.stringify({
                            'id': me.state.Code,
                            'state': me.state.board_txt,
                            'last_move': "",
                            'souffle_move':"",
                            'current_turn': me.state.player,
                            'winner':"",
                            'tier':me.state.tier,
                        }));
                    }
                        }, delay);
                    }
                }
          };
          this.props.client.onclose = function (e) {
            console.error('Client socket closed unexpectedly');
        };

    }
  //?----------------------------------------
  // * Web Page modifiers :
  //?----------------------------------------
  add_one_history_item(content,color)
  {
    console.log("Adding a history item")
    // colors: [blue:"text_primary",yellow: "text-warning",red:"text-danger",green:"text_success"]
    let time_line_item = document.createElement("div");
    time_line_item.classList.add("timeline-item","mb-2");

    let time_label = document.createElement("div");
    time_label.classList.add("timeline-label", "fw-bolder", "text-gray-800", "fs-6");
    let today = new Date();
    let min = today.getMinutes() ? "" + today.getMinutes(): "0" + today.getMinutes();
    let sec = today.getSeconds() ? "" +today.getSeconds(): "0" + today.getSeconds();
    let time = min + ":" + sec;
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
  //?--------------------------------------
  // *Rendering React native method :
  //?--------------------------------------
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
                  soufflables = {this.state.soufflables}
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
                soufflables = {this.state.soufflables}
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
