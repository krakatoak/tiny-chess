# Mock env server to test the chess engine locally
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

INIT_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

class H(BaseHTTPRequestHandler):
    moves_made = 0
    finished = False
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(n))
        H.moves_made = getattr(H, 'moves_made', 0)
        H.finished = getattr(H, 'finished', False)
        if self.path == "/game" and body == {}:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            if H.finished:
                resp = {"status": "done", "wins": 1, "draws": 0, "losses": 0}
            else:
                resp = {"game": 1, "games": 1, "opponent": "depth-2",
                        "opponent_name": "depth-2", "colour": "white",
                        "opening": {"id": 1, "name": "test", "moves": []},
                        "start_fen": INIT_FEN, "moves": [], "fen": INIT_FEN,
                        "plies": 0, "last_move": None, "status": "your_move",
                        "legal_moves": ["e2e4", "e2e3", "d2d4", "g1f3", "b1c3"],
                        "result": None, "outcome": None, "reason": None,
                        "next_game": None, "move_limit_ms": 10000, "max_plies": 200}
            self.wfile.write(json.dumps(resp).encode())
        elif self.path == "/move":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            H.moves_made += 1
            if H.moves_made >= 3:
                H.finished = True
                resp = {"game": 1, "games": 1, "status": "done",
                        "wins": 1, "draws": 0, "losses": 0,
                        "outcome": "win", "reason": "checkmate"}
            else:
                resp = {"game": 1, "games": 1, "status": "your_move",
                        "fen": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
                        "legal_moves": ["e7e5", "d7d5"]}
            self.wfile.write(json.dumps(resp).encode())
        else:
            self.send_response(404); self.end_headers()
    def log_message(self, *a): pass

if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 9123), H).serve_forever()
