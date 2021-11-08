import {useDrag} from 'react-dnd'
import './Piece.css';

function Piece({i,j,type,color}) 
{ // Type : Regular or Dhaimat
    // Color : Black or white
    const [{isDragging} , dragRef] = useDrag({
        type : 'Piece',
        color : color,
        item : {i,j},
        collect:(monitor) =>({
            isDragging : monitor.isDragging()
        })
    })
    let  class_ = "Piece "+color +"_"+ type;
    try {  
    return (
        <div ref = {dragRef} className = {class_} 
        style={{
            textShadow: isDragging ? "20px" : "0px",
          }}>
            
            {/* {isDragging && '😱'} */}
        </div>

    );
    }catch(error)
    {
        console.log("Something went wrong Piece");
    }
}


export default Piece;