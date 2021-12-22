// Drag sources and drop targets only interact
// if they have the same string type.
// You want to keep types in a separate file with

import React,{ Component } from "react"
import '/static/css/Piece.css';
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
    let can = (props.color==="Black" && props.player===1) || (props.color ==="White" && props.player===0) ? true :false;
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
    // console.log("Begginind drag ! ",component);
    let piece_key = component.props.i.toString()+component.props.j.toString();
    console.log("the piece key is : '",piece_key,"'")
    component.props.onStartMove(piece_key);
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

    let item = monitor.getItem();
    const dropCell = monitor.getDropResult();
    // console.log("item :" , item);
    // console.log("Drop result : ",dropCell);

    item.onMove([item.i,item.j],[dropCell.i,dropCell.j]);
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
  constructor()
  {
    super();
    this.onClick_ = this.onClick_.bind(this);
  }
  onClick_(e,key)
  {
      console.log("🚀 ~ file: Piece.js ~ line 91 ~ Piece ~ onClick_",this.props.soufflables.includes(key),e.detail,this.props.player,this.props.color,((this.props.soufflables.includes(key)) && (e.detail > 1) && ((this.props.player ===0 && this.props.color==="Black") || (this.props.player ===1 && this.props.color==="White"))))

    if ( (e.detail > 1) || (this.props.player ===0 && this.props.color==="White") || (this.props.player ===1 && this.props.color==="Black"))
    {
      this.props.onClick(e,key,1); // the piece is present
    }
    if((this.props.soufflables.includes(key)) && (e.detail > 1) && ((this.props.player ===0 && this.props.color==="Black") || (this.props.player ===1 && this.props.color==="White")))
    {
        console.log("yes it does include key but something is wrong after this point");
        this.props.onClick(e,key,2) // 2 for souffle
    }
}
  render() {
    // console.log("the props of the piece are ",this.props);
    let  class_ = "Piece "+this.props.color +"_"+ this.props.type ;
    // Your component receives its own props as usual
    // const { id } = this.props

    // These props are injected by React DnD,
    // as defined by your `collect` function above:
    const { isDragging, connectDragSource} = this.props

    return connectDragSource(
        <div className = {class_} onClick = {(e)=>this.onClick_(e,this.props.i.toString()+this.props.j.toString())}
            style={{ // this is not working as intended yet:
                textShadow: isDragging ? "20px" : "0px",
            }}>
        </div>
    )
  }
}

export default DragSource(Types.Piece, PieceSource, collect)(Piece)
