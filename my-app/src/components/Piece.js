// Drag sources and drop targets only interact
// if they have the same string type.
// You want to keep types in a separate file with

import { Component } from "react"
import './Piece.css';
import { DragSource } from 'react-dnd';
// the rest of your app's constants.
const Types = {
  Piece: 'Piece'
}

/**
 * Specifies the drag source contract.
 * Only `beginDrag` function is required.
 */
const PieceSource = {
  canDrag(props) {
    // You can disallow drag based on props
    // return true
    let can = (props.color==="Black" && props.player===0) || (props.color ==="White" && props.player===1) ? true :false;
    // console.log("The player",props.player,"is trying to drag the piece ",props,"can he ? : ",can);
    // if (!can)
      // alert("Not Your Piece!");
    return can
  },

  isDragging(props, monitor) {
    // If your component gets unmounted while dragged
    // (like a card in Kanban board dragged between lists)
    // you can implement something like this to keep its
    // appearance dragged:
    // console.log("dragging the item" , props)
    return monitor.getItem().id === props.id
  },

  beginDrag(props, monitor, component) {
    // Return the data describing the dragged item
    return props
  },

  endDrag(props, monitor, component) {
    if (!monitor.didDrop()) {
      // You can check whether the drop was successful
      // or if the drag ended but nobody handled the drop
      return
    }

    // When dropped on a compatible target, do something.
    // Read the original dragged item from getItem():
    // const item = monitor.getItem()

    // You may also read the drop result from the drop target
    // that handled the drop, if it returned an object from
    // its drop() method.
    // const dropResult = monitor.getDropResult()

    // This is a good place to call some Flux action
    // CardActions.moveCardToList(item.id, dropResult.listId)
  }
}

/**
 * Specifies which props to inject into your component.
 */
function collect(connect, monitor) {
  return {
    // Call this function inside render()
    // to let React DnD handle the drag events:
    connectDragSource: connect.dragSource(),
    // You can ask the monitor about the current drag state:
    isDragging: monitor.isDragging()
  }
}

class Piece extends Component {
    
  render() {
    // console.log("the props of the piece are ",this.props);
    let  class_ = "Piece "+this.props.color +"_"+ this.props.type;
    // Your component receives its own props as usual
    // const { id } = this.props

    // These props are injected by React DnD,
    // as defined by your `collect` function above:
    const { isDragging, connectDragSource } = this.props

    return connectDragSource(
        <div className = {class_} 
            style={{
                textShadow: isDragging ? "20px" : "0px",
            }}>
            
            {/* {isDragging && '😱'} */}
        </div>

    )
  }
}

export default DragSource(Types.Piece, PieceSource, collect)(Piece)
