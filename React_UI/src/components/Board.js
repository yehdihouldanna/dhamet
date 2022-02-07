//------------------------------------------------
// Copyrigh (c) SMART Solutions SM SA® 2021.
// All rights reserved.
// Code made by : Yehdhih ANNA (TheLuckyMagician).
//------------------------------------------------
//@ts-check
import '/static/css/Board.css';
import Cell from './Cell';
import React, { Component} from 'react';
import {CSSTransition} from 'react-transition-group';
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
      previous_board :[
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0]],
      player: 0,
      Code: props.game_code,
      Client : props.client,
      board_txt: "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbbbb_wwwwbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
      previous_board_txt : "_________________________________________________________________________________",
      move: "",
      last_move :"",
      move_history_render:[],
      creator   :"",
      opponent  :"",
      winner : "",
      initial_time:  5*60,
      creator_time:  5*60,
      opponent_time: 5*60,
      delay: 200,
      prevent: false,
      MouseOnBoard: true,
      username : "",
      tier: null,
      //* Souffle parameters
      can_souffle : true,
      souffle_move : "",
      soufflables : [],
      audio_url : "/static/sounds/punch.wav",
      game_started :false,
    };
    this.TimerInterval = null;
    this.AI_NAMES  = ["AI_Random","AI_Dummy","AI_MinMax"];
    this.BOT_NAMES = ["Med10","Mariem","Sidi","احمد","Khadijetou","Cheikh","Vatimetou","ابراهيم",
                      "Mamadou","Oumar","Amadou","3abdellahi","Va6me","Moussa","Aly","Samba"];
    //* Tiers : are the difficulty level, for now we have 3 tiers, 3 :AI_MinMax, 2 : Dummy, 1 : Random
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

    this.format_time = this.format_time.bind(this);
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
             if (this.state.board[i][j] === -1) {str += "b";}
        else if (this.state.board[i][j] === -3) {str += "B";}
        else if (this.state.board[i][j] ===  0) {str += "_";}
        else if (this.state.board[i][j] ===  1) {str += "w";}
        else if (this.state.board[i][j] ===  3) {str += "W";}
      }
    }
    return str
  };
  deserialize(text,text_prev) {
    let game_state = this.state
    let k = 0;
    for (let i = 0; i < 9; i++) {
      for (let j = 0; j < 9; j++) {
             if (text[k] === "b") game_state.board[i][j] = -1;
        else if (text[k] === "B") game_state.board[i][j] = -3;
        else if (text[k] === "_") game_state.board[i][j] =  0;
        else if (text[k] === "w") game_state.board[i][j] =  1;
        else if (text[k] === "W") game_state.board[i][j] =  3;

             if (text_prev[k] === "b") game_state.previous_board[i][j] = -1;
        else if (text_prev[k] === "B") game_state.previous_board[i][j] = -3;
        else if (text_prev[k] === "_") game_state.previous_board[i][j] =  0;
        else if (text_prev[k] === "w") game_state.previous_board[i][j] =  1;
        else if (text_prev[k] === "W") game_state.previous_board[i][j] =  3;

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
      let x  = Number(this.state.move[len-2])
      let y  = Number(this.state.move[len-1])
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
        this.handleSouffle(key);
    }
    if (this.state.move.length>=5)
    {
      // if the user double click his piece and double click on another piece of his
      let len = this.state.move.length;
      let x  = Number(this.state.move[len-5])
      let y  = Number(this.state.move[len-4])
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
  };

  //?-----------------------------------------------------------------------
  // * Handling Request and getting the reponses from the back end methods :
  //?-----------------------------------------------------------------------
  handleSouffle(piece_key)
  {
    let i = parseInt(piece_key[0]);
    let j = parseInt(piece_key[1]);
    let game_state= this.state;
    game_state.souffle_move = piece_key;
    game_state.can_souffle = false;
    console.log("🚀 ~ Souffle Move", game_state.souffle_move);
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
    // console.log("🚀 ~ file: Board.js ~ line 248 ~ Board ~ MoveRequest_ws")
    // * This function communicate with the GameMoveConsumer in the backend
    if (this.state.Code === "") {
      this.CreateGameRequest();
    }
    else if (move_str.length >= 5) {
      console.log("Trying the move : ", move_str,"with souffle :",souffle_move);
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
    let game_state= this.state;
    game_state.souffle_move = "";
    this.setState(game_state);
  };
  CreateFakeOpponent()
  {
    // creates a game with a fake opponenet if the player waited so long, without another human joining his game
    let me = this;
    let thisTimeout = setTimeout(() =>{
        if ((me.state.opponent === ""))
            {CallFakeOpponent(me);}
    }, 30000);

    function CallFakeOpponent(me) {
        clearTimeout(thisTimeout);
        // console.log("🚀 ~ file: Board.js ~ line 285 ~ Board ~ CallFakeOpponent ~ 'Launched the request for fake opponenet'")
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
  // @ts-ignore
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
            }
        });
  }
  //?----------------------------------------
  // * Web Page modifiers :
  //?----------------------------------------
  add_one_history_item(content,color)
  {
    let time_line_item = document.createElement("div");
    time_line_item.classList.add("timeline-item","mb-2");

    let time_label = document.createElement("div");
    time_label.classList.add("timeline-label", "fw-bolder", "text-gray-800", "fs-6");
    let today = new Date();
    let min = today.getMinutes() ? "" + today.getMinutes(): "0" + today.getMinutes();
    let sec = today.getSeconds() ? "" + today.getSeconds(): "0" + today.getSeconds();
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

  format_time()
  {
    let timer_id1="timer_player1";
    let timer_id2="timer_player2";
    if(this.state.opponent===this.state.username)
    {
        timer_id1= "timer_player2";
        timer_id2= "timer_player1";
    }
    let timer_id = this.state.player===0 ? timer_id1 : timer_id2;
    let seconds_left = this.state.player===0 ? this.state.creator_time : this.state.opponent_time;
    let hours, minutes, seconds;
    if (seconds_left >= 0) {
        if ((seconds_left) < Math.min(60, (this.state.initial_time / 2))) {
            document.getElementById(timer_id).classList.remove('color-full');
            document.getElementById(timer_id).classList.add('color-half');
        }
        if ((seconds_left) < Math.min(30, (this.state.initial_time / 4))) {
            document.getElementById(timer_id).classList.remove('color-half');
            document.getElementById(timer_id).classList.add('color-empty');
        }
        // @ts-ignore
        hours = pad(parseInt(seconds_left / 3600));
        seconds_left = seconds_left % 3600;
        // @ts-ignore
        minutes = pad(parseInt(seconds_left / 60));
        seconds = pad(seconds_left % 60);
        // format countdown string + set tag value
        document.getElementById(timer_id).innerHTML = "<span>" + hours + ":</span><span>" + minutes + ":</span><span>" + seconds + "</span>";
    }
    function pad(n) { return (n < 10 ? '0' : '') + n; }
  }
  //?---------------------------------------------------------
  // * Component's Native methods :
  //?---------------------------------------------------------
  componentWillMount() {
      this.getUserNameRequest();
      this.CreateFakeOpponent();

      //?-----------------------------------
      //**? Moves Socket :**
      //?-----------------------------------
      this.props.client.onopen = () => {
          console.log('A new client Connected');
          this.props.client.send(
              JSON.stringify({
                  'id': this.state.Code,
                  'state': this.state.board_txt,
                  'last_move': this.state.move,
                  'souffle_move': this.state.souffle_move,
                  'current_turn': this.state.player,
                  'creator': this.state.creator,
                  'creator_score': "",
                  'opponent': this.state.opponent,
                  'opponent_score': "",
                  'winner': this.state.winner,
                  'winner_score': "",
                  'tier': "",
              }));

              this.props.client.send(
                JSON.stringify({
                  'id': me.state.Code,
                  'current_turn' : me.state.player,
                  'type' : "timer",
                  'creator_time' :me.state.creator_time,
                  'opponent_time' :me.state.opponent_time,
                  'winner':"",
                }));
      };
      let me = this;
      this.props.client.onmessage = function (e) {
          const data = JSON.parse(e.data);
          if (typeof data["Bad Request"] != "undefined") {
              console.log("Invalid Move : Ignored!");
              me.state.move = "";
          }
          else {
                if(data.type==="timer")
                {
                    // * server returned a valid time :
                    // console.log("Recevied data from timer socket ", data);
                    let game_state = me.state;
                    game_state.creator_time = data.creator_time;
                    game_state.opponent_time = data.opponent_time;
                    if (data.winner !== null && data.winner !== "") {
                        // TODO : change this to a better thing.
                        me.state.winner = data.winner
                        alert(data.winner + " Won on time !");
                    }
                    me.setState(game_state);
                }

            else{
              // * server returned a valid move :
              console.log("We received a correct data: ", data);
              let game_state = me.state;
              game_state.player = data.current_turn;
              console.log("The player now is : ", game_state.player);
              game_state.previous_board_txt = game_state.board_txt;
              game_state.board_txt = data.state;
              game_state.soufflables = data.soufflables;
              if (game_state.soufflables.length) { game_state.can_souffle = true; }
              if (game_state.last_move != data.last_move) {
                  game_state.last_move = data.last_move;
                  game_state.move_history_render.push(game_state.last_move);
                  me.setState(game_state);
                  if (game_state.move_history_render.length == 2) {
                      me.update_moves_time_line();
                      me.state.move_history_render = [];
                  }
                  me.deserialize(data.state, game_state.previous_board_txt);
              }
              me.state.move = "";

              if (data.winner !== null && data.winner !== "") {
                  // TODO : change this to a better thing.
                  alert(data.winner + " Won the game!");
                  me.state.winner = data.winner
              }

              if (data.opponent !== me.state.opponent) {
                  me.state.game_started = true;
                  me.state.opponent = data.opponent;
                  me.state.creator = data.creator;
                  me.state.tier = data.tier === 0 ? null : data.tier;
                  if (data.opponent === me.state.username) {
                      document.getElementById("player2_name").innerHTML = data.creator;
                      document.getElementById("player2_score").innerHTML = data.creator_score;
                      document.getElementById("player1_name").innerHTML = data.opponent;
                      document.getElementById("player1_score").innerHTML = data.opponent_score;
                      // document.getElementById("player1").style.backgroundColor  = "rgb(156,108,20)";
                      // document.getElementById("player2").style.backgroundColor  = "rgb(76,52,36)";
                  }
                  else if (data.creator === me.state.username) {
                      document.getElementById("player1_name").innerHTML = data.creator;
                      document.getElementById("player1_score").innerHTML = data.creator_score;
                      document.getElementById("player2_name").innerHTML = data.opponent;
                      document.getElementById("player2_score").innerHTML = data.opponent_score;
                      // document.getElementById("player1").style.backgroundColor  = "rgb(76,52,36)";
                      // document.getElementById("player2").style.backgroundColor  = "rgb(156,108,20)";
                  }
                  me.forceUpdate();
              }
              // * If We are playing vs AI then we will send it's request after the player's
              if (me.AI_NAMES.includes(me.state.opponent) && me.state.player === 1 && me.state.winner === "") {
                  setTimeout(() => {
                      // * We can change the response time based on the need
                      if (me.state.previous_board_txt != me.state.board_txt) {
                          console.log("The AI request waited for 350 ms !")
                          me.props.client.send(
                              JSON.stringify({
                                  'id': me.state.Code,
                                  'state': me.state.board_txt,
                                  'last_move': "",
                                  'souffle_move': "",
                                  'current_turn': me.state.player,
                                  'winner': "",

                              }));
                      }
                  }, 350);
              }

              // * If the player is playing vs a Bot
              if (me.state.tier !== null && me.state.player === 1 && me.state.winner === "") {
                  let delay = 350 + Math.floor(Math.random() * 10000) // randomizing the time of the response
                  setTimeout(() => {
                      // * We can change the response time based on the need
                      // @ts-ignore
                      if (me.state.previous_board_txt != me.state.board_txt) {
                          console.log("The AI request waited for 350 ms !")
                          me.props.client.send(
                              JSON.stringify({
                                  'id': me.state.Code,
                                  'state': me.state.board_txt,
                                  'last_move': "",
                                  'souffle_move': "",
                                  'current_turn': me.state.player,
                                  'winner': "",
                                  'tier': me.state.tier,
                              }));
                      }
                  }, delay);
              }

            }
          }
      };
      // @ts-ignore
      this.props.client.onclose = function (e) {
          console.error('Client socket closed unexpectedly');
          clearInterval(this.TimerInterval);
      };
        //?-----------------------------------
        //**? Timer Socket : **
        //?-----------------------------------
    }
  componentDidMount() {
    document.getElementById("timer_player1").classList.add('tiles');
    document.getElementById("timer_player1").classList.add('color-full');
    document.getElementById("timer_player2").classList.add('tiles');
    document.getElementById("timer_player2").classList.add('color-full');
    let me = this;
    this.TimerInterval = setInterval(function () {
        //TODO Improve the timer gestion for the case of 2 players :
        if (me.state.username === me.state.creator && me.state.opponent!=="" && me.state.winner==="" && me.state.creator_time>-1 && me.state.opponent_time>-1)
        {
                console.log("sent a request to check for time update");
                me.format_time();
                me.state.Client.send(
                    JSON.stringify({
                        'id': me.state.Code,
                        'current_turn': me.state.player,
                        'type': "timer",
                        'creator_time': me.state.creator_time,
                        'opponent_time': me.state.opponent_time,
                        'winner': "",
                    }));
            }
          }, 1000);


      {this.state.first_render = false;}
      if(this.state.opponent_time<=0 || this.state.creator_time<=0 || this.state.winner!="")
      {
          clearInterval(this.TimerInterval);
          this.game_started=false;
      }
    }
  //?--------------------------------------
  // * Rendering React native method :
  //?--------------------------------------
  render() {
    let Cells = [];
    let { board , previous_board} = this.state;
    let len = board.length;

    // if (this.state.opponent === "" || this.state.username==="")
    if (!this.state.game_started)
    {
        Cells.push(
            <div className="d-flex flex-column justify-content-center align-items-center Wait_text" style = {{"width": "100%" , "height":"100%"}}>
                <div className="spinner-border text-warning " role="status" style={{width: "5rem",height: "5rem"}}>
                </div>
                <div > حاني اشوي مسَحفاك <br/>  مَانَك عجلان اعل شي </div>
            </div>
        );
    }
    else if(this.state.opponent === this.state.username && this.state.creator !=="")
    {
        for (let i = 0; i < len; i++) {
            for (let j = 0; j < len; j++) {
              let key = i.toString() + j.toString();
              let ex_css_class="";
              if (this.state.last_move.includes(key))
              {ex_css_class = " highlight_last_move";}
              Cells.push(
                <Cell
                  key={key}
                  i={i}
                  j={j}
                  value={board[i][j]}
                  previous_value = {previous_board[i][j]}
                  player={this.state.player}
                  move={this.state.move}
                  onMove={this.handleMove}
                  onHover={this.handleHover}
                  onStartMove={this.handleStartMove}
                  onClick={this.handleClick}
                  ex_css_class ={ex_css_class}
                  toggle = {this.state.move.includes(key)}
                  soufflables = {this.state.soufflables}
                  audio_url = {this.state.audio_url}
                  first_render= {this.state.first_render}
                  game_started = {this.state.game_started}
                  >
                </Cell>
              );
            }
          }
        }
    else //if (this.state.opponent !==""  && this.state.creator === this.state.username)
        {
        for (let i = len - 1; i >= 0; i--) {
            for (let j = 0; j < len; j++) {
                let key = i.toString() + j.toString();
                let ex_css_class="";
                if (this.state.last_move.includes(key))
                {ex_css_class = " highlight_last_move";}
                Cells.push(
                    <Cell
                    key={key}
                    i={i}
                    j={j}
                    value={board[i][j]}
                    previous_value = {previous_board[i][j]}
                    player={this.state.player}
                    move={this.state.move}
                onMove={this.handleMove}
                onHover={this.handleHover}
                onStartMove={this.handleStartMove}
                onClick={this.handleClick}
                ex_css_class ={ex_css_class}
                toggle = {this.state.move.includes(key)}
                soufflables = {this.state.soufflables}
                audio_url = {this.state.audio_url}
                first_render= {this.state.first_render}
                game_started = {this.state.game_started}
              >
              </Cell>
            );
          }
        }
    }
    return (
        <CSSTransition
            in = {true}
            appear = {true}
            timeout = {300}
            classNames = "transition">
            <div id="board"  onMouseLeave={this.handleMouseLeave}>
                {Cells}
            </div>
        </CSSTransition>

    );
  };
}

export default Board;
