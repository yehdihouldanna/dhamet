import './App.css';

function App() {
  console.log("The app started!");
  let data = {
    "Baord" : 
    [[ 1,  1,  1,  1,  1,  1,  1,  1,  1],
    [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
    [ 0,  0,  0,  0,  1,  0,  1,  1,  1],
    [ 0,  0,  0, -1,  0,  0,  1,  1,  1],
    [ 0,  0, -1,  0,  0,  0, -1, -1, -1],
    [ 0,  0,  0,  0, -1, -1, -1, -1, -1],
    [ 0,  0,  0, -1, -1,  0, -1, -1, -1],
    [ 0, -1, -1, -1, -1, -1, -1, -1, -1],
    [ 2, -1, -1, -1, -1, -1, -1, -1, -1]],
    "Player":0
    };
  
  return (
    
    <div id="board">
        Something 
      </div>
  );
}

export default App;
