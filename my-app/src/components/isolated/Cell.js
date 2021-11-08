import {useDrop} from 'react-dnd'
import Piece from "./Piece"
import React,{useState} from 'react'
import './Cell.css';



function Cell(props) 
{
    // const [cell , setCell] = useState()
    // console.log(cell,setCell);
    // const [{isOver}, drop] = useDrop({
    //         accept:'Piece',
    //         drop : (item) => setCell((cell) =>
    //             !cell.includes(item) ?  [...cell,item] :cell),
    //         collect : (monitor) =>({
    //             isOver : monitor.isOver()
    //         })
    // })
    const [cell,setCell] = useState()
    const [{ isOver, canDrop }, drop] = useDrop(
        () => ({
          accept: 'Piece',
          canDrop: () => props.value===0,
          drop: () => ({
              i : props.i,
              j : props.j
          }),
          collect: (monitor) => ({
            isOver: !!monitor.isOver(),
            canDrop: !!monitor.canDrop(),
          }),
        }),
        cell,
      )
    // const [{ isOver }, drop] = useDrop(
    //     () => ({
    //       accept: 'Piece',
    //       drop: () => moveKnight(x, y),
    //       collect: (monitor) => ({
    //         isOver: !!monitor.isOver()
    //       })
    //     }),
    //     [x, y]
    //   )
    try{
        if(props.value===0)
        { 
            return (
                <div className="cell" ref={drop} onMove={props.onMove}> 
                    {/* {isOver && <div>Drop Here!</div>} */}
                </div>
            );
        }
        else
        {   
            return (
                <div className="cell">
                    <Piece 
                        type={Math.abs(props.value)===1 ? "regular" : "dhaimat"} 
                        color={props.value<0 ? "Black":"White"}
                        i={props.i}
                        j={props.j}>
                    </Piece>
                </div>
            );
        }
    } catch(error)
    {
        console.log("Something went wrong in cell");
    }
}
export default Cell;