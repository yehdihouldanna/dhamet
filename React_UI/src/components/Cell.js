import React, { Component } from 'react'
import Piece from "./Piece";
import '/static/css/Cell.css';
class Cell extends Component {
  render() {
    if(this.props.value===0)
        {
            return <div className={"cell opacity-active-75" + this.props.ex_css_class +(this.props.toggle ? " cell_active" : "")}  onClick = {(e)=>
                  {
                    this.props.onClick(e,this.props.i.toString()+this.props.j.toString(),0); // no piece is present
                  }
                    }>
                  {this.props.i.toString()+this.props.j.toString()}
                </div>
        }
        else
        {
            return <div className={"cell opacity-active-75"+ this.props.ex_css_class +(this.props.toggle ? " cell_active" : "")} >
                    {this.props.i.toString()+this.props.j.toString()}
                    <Piece
                        key ={this.props.key}
                        value={this.props.value}
                        previous_value = {this.props.previous_value}
                        i={this.props.i}
                        j={this.props.j}
                        ex_css_class ={this.props.ex_css_class}
                        player = {this.props.player}
                        onStartMove = {this.props.onStartMove}
                        onMove = {this.props.onMove}
                        onClick = {this.props.onClick}
                        soufflables = {this.props.soufflables}
                        >
                    </Piece>
                </div>
        }
  }
}

export default Cell;
