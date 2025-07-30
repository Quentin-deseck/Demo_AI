# snake_game.py
from fasthtml.common import *

app, rt = fast_app()

@rt("/")
def snake_page(sess):
    return Titled("Jeu Snake (FastHTML)",
        H1("🐍 Jeu Snake"),
        Canvas(id="gameCanvas", width=500, height=500, style="border:1px solid black;"),
        Script("""
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        const gridSize = 20;
        const tileCount = canvas.width / gridSize;
        let snake = [{x: 10, y: 10}];
        let velocity = {x: 0, y: 0};
        let food = {x: 5, y: 5};

        function gameLoop() {
            const head = {x: snake[0].x + velocity.x, y: snake[0].y + velocity.y};

            // Wall collision
            if (head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) {
                resetGame();
                return;
            }

            // Self collision
            for (let part of snake) {
                if (part.x === head.x && part.y === head.y) {
                    resetGame();
                    return;
                }
            }

            snake.unshift(head);

            // Eat food
            if (head.x === food.x && head.y === food.y) {
                placeFood();
            } else {
                snake.pop();
            }

            drawGame();
        }

        function drawGame() {
            ctx.fillStyle = "black";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Draw snake
            ctx.fillStyle = "lime";
            for (let part of snake) {
                ctx.fillRect(part.x * gridSize, part.y * gridSize, gridSize - 2, gridSize - 2);
            }

            // Draw food
            ctx.fillStyle = "red";
            ctx.fillRect(food.x * gridSize, food.y * gridSize, gridSize - 2, gridSize - 2);
        }

        function placeFood() {
            food.x = Math.floor(Math.random() * tileCount);
            food.y = Math.floor(Math.random() * tileCount);
        }

        function resetGame() {
            snake = [{x: 10, y: 10}];
            velocity = {x: 0, y: 0};
            placeFood();
        }

        document.addEventListener("keydown", e => {
            if (e.key === "ArrowUp" && velocity.y === 0) velocity = {x: 0, y: -1};
            if (e.key === "ArrowDown" && velocity.y === 0) velocity = {x: 0, y: 1};
            if (e.key === "ArrowLeft" && velocity.x === 0) velocity = {x: -1, y: 0};
            if (e.key === "ArrowRight" && velocity.x === 0) velocity = {x: 1, y: 0};
        });

        resetGame();
        setInterval(gameLoop, 100);
        """, type="module")
    )

serve()