from src.helpers import is_valid_final_rank_pawn
from src.boardposition import BoardPosition
from src.player import Player
from src.board import Board
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import json
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
import uvicorn

app = FastAPI()

@app.get("/")
async def get():
    html_content = Path("../index.html").read_text()
    return HTMLResponse(html_content)


app.mount("/Users/itaihalperin/chess/static", StaticFiles(directory="/Users/itaihalperin/chess/static"), name="static")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    msg = {"type": "startup"}
    await websocket.send_json(msg)
    cookie = await websocket.receive_text()

    if cookie:
        cookie = json.loads(cookie)
        if cookie.get('turn') == 0:
            game_board = Board(Player("a",0), Player("b",1), cookie)
        else:
            game_board = Board(Player("a",1), Player("b",0), cookie)

    else:
        game_board = Board(Player("a",1), Player("b",0))
    await websocket.send_json({"type": "new_game", "board":game_board.render_board()})



    
    async def restart(new_board: Board):
        board = new_board.render_board()
        await websocket.send_json({"type": "new_game", "board": board})
        message = {"type": "cookie_update", "board": board}
        await websocket.send_json(message)
    
    async def checkmate_modal(game_board: Board, new_board: Board):
        game_board.change_turn()
        board = game_board.render_board()
        await websocket.send_json({"type": "new_board", "board": board})
        msg = {"type": "checkmate"}
        await websocket.send_json(msg)
        await websocket.receive_text()
        await restart(new_board)

    while True:
        if game_board.is_checkmate():
            new_board = Board(Player("a", 1), Player("b", 0))
            await checkmate_modal(game_board, new_board)
            game_board = new_board
        
        else:
            is_valid_move = False
            data = await websocket.receive_text()
            data = json.loads(data)
            origin = data["origin"]
            destination = data["destination"]
            origin = BoardPosition(origin["row"], origin["col"])
            destination = BoardPosition(destination["row"], destination["col"])
            if is_valid_final_rank_pawn(game_board, origin, destination):
                    is_valid_move = True
                    msg = {"type": "final_rank_pawn", "origin": data["origin"], "destination": data["destination"], "turn": game_board.turn.color}
                    await websocket.send_json(msg)
                    data = await websocket.receive_text()
                    game_board.replace_pawn(data, origin, destination)
            else:
                is_valid_move = game_board.move(origin, destination)
            
            board = game_board.render_board()
            msg = {"type": "new_board", "board":board}
            await websocket.send_json(msg)

            if is_valid_move:
                game_board.change_turn()
                if game_board.is_checkmate():
                    new_board = Board(Player("a", 1), Player("b", 0))
                    await checkmate_modal(game_board, new_board)
                    game_board = new_board
                else:
                    board = game_board.render_board()
                    message = {"type": "cookie_update", "board": board}
                    await websocket.send_json(message)

            
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
    
    

