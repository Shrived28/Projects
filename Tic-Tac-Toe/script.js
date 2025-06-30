const winPatterns = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
];

let turn=0;
let count = 0;

let newBtn = document.querySelector("#new-btn");
let resetBtn = document.querySelector("#reset-btn");
let cells = document.querySelectorAll(".cells");
let afterGame = document.querySelector(".aftergame");
let msg = document.querySelector("#msg");

enablebtns =()=>{
    for(let cell of cells){
        cell.disabled = false;
        cell.innerText = '';
        msg.innerText = '';
    }
};

disablebtns = ()=>{
    for (let cell of cells){
        cell.disabled = true;
    }
};

resetGame = () => {
    turn = 0;
    count = 0;
    enablebtns();
    afterGame.classList.add("hide");
};

gameDraw = () => {
    if (msg.innerText === ''){
        msg.innerText = `Game was a Draw! \n Click Start new Game to Play again`;
    }
    afterGame.classList.remove("hide");
    resetBtn.classList.add("hide");
};

cells.forEach((cell) =>{
    cell.addEventListener("click",()=>{
        if (turn===0){
            cell.innerText="X";
            turn=1;
            
        }else{
            cell.innerText="O";
            turn=0;
        }
        cell.disabled = true;
        count++;

        let isWon = checkIfWon();

        if (count === 9 && !isWon){
            gameDraw();
        }
    });
});

const checkIfWon = () => {
    for (let pat of winPatterns){
        let pos1 = cells[pat[0]].innerText;
        let pos2 = cells[pat[1]].innerText;
        let pos3 = cells[pat[2]].innerText;

        if (pos1 != "" && pos2 != "" && pos3 != ""){
            if (pos1 === pos2 && pos2 === pos3){
                afterGame.classList.remove("hide");
                resetBtn.classList.add("hide");
                msg.innerText =`Hurray!! "${pos1}" Won The Game`;
                disablebtns();
            }
        }
    }
};

newBtn.addEventListener("click",resetGame);
resetBtn.addEventListener("click",resetGame);