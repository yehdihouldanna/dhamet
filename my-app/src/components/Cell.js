import React, { Component } from 'react'
import { findDOMNode } from 'react-dom';
import { DropTarget } from 'react-dnd';
import Piece from "./Piece";
import './Cell.css';
// Drag sources and drop targets only interact
// if they have the same string type.
// You want to keep types in a separate file with
// the rest of your app's constants.
const Types = {
  PIECE: 'Piece'
}

/**
 * Specifies the drop target contract.
 * All methods are optional.
 */
const CellTarget = {
  canDrop(props, monitor) {
    // You can disallow drop based on props or item
    // const item = monitor.getItem()
    // return canMakeChessMove(item.fromPosition, props.position)
    return props.value===0 ? true : false

  },

  hover(props, monitor, component) {
    // This is fired very often and lets you perform side effects
    // in response to the hover. You can't handle enter and leave
    // here—if you need them, put monitor.isOver() into collect() so you
    // can use componentDidUpdate() to handle enter/leave.

    // You can access the coordinates if you need them
    const clientOffset = monitor.getClientOffset()
    const componentRect = findDOMNode(component).getBoundingClientRect()

    // You can check whether we're over a nested drop target
    const isOnlyThisOne = monitor.isOver({ shallow: true })

    // You will receive hover() even for items for which canDrop() is false
    const canDrop = monitor.canDrop()
  },

  drop(props, monitor, component) {
    if (monitor.didDrop()) {
      // If you want, you can check whether some nested
      // target already handled drop
      return 
    }

    // Obtain the dragged item
    const item = monitor.getItem()

    // You can do something with it
    // ChessActions.movePiece(item.fromPosition, props.position)
    
    
    // You can also do nothing and return a drop result,
    // which will be available as monitor.getDropResult()
    // in the drag source's endDrag() method
    
    // console.log("we are about to call onMove method with the params , ",item,[props.i,props.j]);
    return props.onMove([item.i,item.j],[props.i,props.j]);
    // return props.onMove(item,[props.i,props.j])
  }
}

/**
 * Specifies which props to inject into your component.
 */
function collect(connect, monitor) {
  return {
    // Call this function inside render()
    // to let React DnD handle the drag events:
    connectDropTarget: connect.dropTarget(),
    // You can ask the monitor about the current drag state:
    isOver: monitor.isOver(),
    isOverCurrent: monitor.isOver({ shallow: true }),
    canDrop: monitor.canDrop(),
    itemType: monitor.getItemType(),
    item : monitor.getItem(),
    
  }
}

class Cell extends Component {
  componentDidUpdate(prevProps) {
    if (!prevProps.isOver && this.props.isOver) {
      // You can use this as enter handler
      this.props.onMove()
    }

    if (prevProps.isOver && !this.props.isOver) {
      // You can use this as leave handler
    }

    if (prevProps.isOverCurrent && !this.props.isOverCurrent) {
      // You can be more specific and track enter/leave
      // shallowly, not including nested targets
    }
  }

  render() {
    // console.log("the props of the cell are : ", this.props);
    // Your component receives its own props as usual
    const { key } = this.props

    // These props are injected by React DnD,
    // as defined by your `collect` function above:
    const { isOver, canDrop, connectDropTarget } = this.props

    if(this.props.value===0)
        { 
            return connectDropTarget(
                <div className="cell"> 
                    {/* {isOver && <div>Drop Here!</div>} */}
                </div>
            );
        }
        else
        {   
            return connectDropTarget(
                <div className="cell">
                    <Piece 
                        type={Math.abs(this.props.value)===1 ? "regular" : "dhaimat"} 
                        color={this.props.value<0 ? "Black":"White"}
                        i={this.props.i}
                        j={this.props.j}
                        player = {this.props.player}>
                    </Piece>
                </div>
            );
        }
  }
}

export default DropTarget(
  Types.PIECE,
  CellTarget,
  collect
)(Cell)