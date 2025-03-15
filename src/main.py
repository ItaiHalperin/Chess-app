from pathlib import Path
import json
import os

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from src.helpers import is_valid_final_rank_pawn
from src.boardposition import BoardPosition
from src.player import Player
from src.board import Board

# Constants
DEFAULT_PORT = 8000
INDEX_PATH = "../index.html"
STATIC_PATH = "/Users/itaihalperin/chess/static"

# Initialize FastAPI app
app = FastAPI()

# Setup static files
static_directory = Path("../static").resolve()
app.mount("/static", StaticFiles(directory=static_directory), name="static")


# Routes
@app.get("/")
async def get():
    """Serve the main HTML page."""
    html_content = Path(INDEX_PATH).read_text()
    return HTMLResponse(html_content)


# Game handling
class ChessGameHandler:
    def __init__(self, websocket):
        self.websocket = websocket
        self.game_board = None

    async def initialize_game(self, cookie=None):
        """Initialize a new game or load from cookie."""
        if cookie:
            cookie_data = json.loads(cookie)
            turn = cookie_data.get('turn', 0)
            player_a_color = 0 if turn == 0 else 1
            player_b_color = 1 - player_a_color
            self.game_board = Board(
                Player("a", player_a_color),
                Player("b", player_b_color),
                cookie_data
            )
        else:
            self.game_board = Board(Player("a", 1), Player("b", 0))

        await self.send_json({"type": "new_game", "board": self.game_board.render_board()})

    async def restart_game(self):
        """Start a new game."""
        self.game_board = Board(Player("a", 1), Player("b", 0))
        board = self.game_board.render_board()
        await self.send_json({"type": "new_game", "board": board})
        await self.send_json({"type": "cookie_update", "board": board})

    async def handle_checkmate(self):
        """Handle checkmate scenario."""
        self.game_board.change_turn()
        board = self.game_board.render_board()
        await self.send_json({"type": "new_board", "board": board})
        await self.send_json({"type": "checkmate"})

        # Wait for user acknowledgment
        await self.websocket.receive_text()

        # Restart game
        await self.restart_game()

    async def handle_move(self, data):
        """Process a move from the client."""
        origin = BoardPosition(data["origin"]["row"], data["origin"]["col"])
        destination = BoardPosition(data["destination"]["row"], data["destination"]["col"])

        # Handle pawn promotion
        if is_valid_final_rank_pawn(self.game_board, origin, destination):
            is_valid_move = True
            await self.handle_pawn_promotion(data, origin, destination)
        else:
            is_valid_move = self.game_board.move(origin, destination)

        # Update board state
        board = self.game_board.render_board()
        await self.send_json({"type": "new_board", "board": board})

        # Handle move consequences
        if is_valid_move:
            self.game_board.change_turn()
            if self.game_board.is_checkmate():
                await self.handle_checkmate()
            else:
                # Update cookie
                board = self.game_board.render_board()
                await self.send_json({"type": "cookie_update", "board": board})

    async def handle_pawn_promotion(self, data, origin, destination):
        """Handle pawn promotion scenario."""
        msg = {
            "type": "final_rank_pawn",
            "origin": data["origin"],
            "destination": data["destination"],
            "turn": self.game_board.turn.color
        }
        await self.send_json(msg)

        # Wait for user selection
        promotion_piece = await self.websocket.receive_text()
        self.game_board.replace_pawn(promotion_piece, origin, destination)

    async def send_json(self, data):
        """Send JSON data to the client."""
        await self.websocket.send_json(data)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for game communication."""
    await websocket.accept()

    # Create game handler
    game_handler = ChessGameHandler(websocket)

    # Initial startup message
    await websocket.send_json({"type": "startup"})

    # Handle cookie
    cookie = await websocket.receive_text()
    await game_handler.initialize_game(cookie)

    # Main game loop
    while True:
        if game_handler.game_board.is_checkmate():
            await game_handler.handle_checkmate()
        else:
            data = await websocket.receive_text()
            await game_handler.handle_move(json.loads(data))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", DEFAULT_PORT))
    uvicorn.run(app, host="0.0.0.0", port=port)