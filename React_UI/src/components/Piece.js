import React, { Component } from "react"
import '/static/css/Piece.css';
import { CSSTransition, TransitionGroup } from 'react-transition-group';

class Piece extends Component {
    constructor(props) {
        super(props);
        this.onClick_ = this.onClick_.bind(this);
        this.audio = new Audio(this.props.audio_url);
        this.play = true;
        // this.StartPlay = this.StartPlay.bind(this);
    }
    onClick_(e, key) {
        if (this.props.value === 0) {
            this.props.onClick(e, key, 0) // 0 no piece
        }
        else {
            let color = this.props.value < 0 ? "Black" : "White";
            if ((e.detail > 1) || (this.props.player === 0 && color === "White") || (this.props.player === 1 && color === "Black")) {
                this.props.onClick(e, key, 1); // the piece is present
            }
            if ((this.props.soufflables.includes(key)) && (e.detail > 1) && ((this.props.player === 0 && color === "Black") || (this.props.player === 1 && color === "White"))) {
                this.props.onClick(e, key, 2) // 2 for souffle
            }
        }
    }

    // componentWillMount()
    // {
    //     this.audio.play()
    //     // this.audio.removeEventListener('ended', () => this.setState({ play: true }));
    // }

    componentDidMount() {
        if(this.play && this.props.game_started && !this.first_render)
        {   this.audio.play();
            this.play = false;
        }
        else
        {
            this.audio.pause();
        }
        // this.audio.removeEventListener('ended', () => this.setState({ play: true }));
    }


    // StartPlay() {
    //     this.setState({}, () => {
    //         this.state.play ? this.audio.play() : this.audio.pause();
    //         this.state.play = !this.state.play;
    //     });
    // }
    render() {
        let class_ = ""
        if (this.props.value !== 0) {
            let type = Math.abs(this.props.value) === 1 ? "regular" : "dhaimat";
            let color = this.props.value < 0 ? "Black" : "White";
            class_ = "Piece " + color + "_" + type;
        }
        let animation_in = null;
        if (this.props.value !== 0 && this.props.previous_value === 0) {
            animation_in = true;
        }
        else if (this.props.value === 0 && this.props.previous_value !== 0) { animation_in = false; }

        return <TransitionGroup className="class__">
            <CSSTransition
                in={animation_in}
                appear={true}
                // enter = {true}
                exit={true}
                timeout={{ enter: 500, exit: 500 }}
                classNames="anim">
                <div className={class_} onClick={(e) => this.onClick_(e, this.props.i.toString() + this.props.j.toString())}>
                    {/* {this.StartPlay()} */}
                </div>
            </CSSTransition>
        </TransitionGroup>
    }
}
export default Piece;
