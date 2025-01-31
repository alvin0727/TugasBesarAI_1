import time
import threading
from collections import deque

TILE_SIZE = 32  # tile size
WIDTH = 20 * TILE_SIZE  # 32 tile
HEIGHT = 20 * TILE_SIZE
COLOR_GREEN = (0, 255, 0)
COLOR_WHITE = (255, 255, 255)

tiles = ['empty', 'wall', 'cow']

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


player = Actor("ufo", anchor=(0, 0), pos=(1 * TILE_SIZE, 2 * TILE_SIZE))
class MazeNode:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.visited_color = COLOR_WHITE
        self.path_color = COLOR_WHITE
        self.parent = None  # Added to store the parent node

    def set_parent(self, parent_node):
        self.parent = parent_node


def build_tree():
    tree = []
    for row in range(len(maze)):
        row_nodes = []
        for col in range(len(maze[row])):
            node = MazeNode(row, col)
            row_nodes.append(node)
        tree.append(row_nodes)
    return tree

tree = build_tree()
exit_found = False
dfs_thread_started = False

def draw():
    screen.clear()

    # Gambar dulu background maze
    for row in range(len(maze)):
        for column in range(len(maze[row])):
            x = column * TILE_SIZE
            y = row * TILE_SIZE
            tile = tiles[maze[row][column]]
            screen.blit(tile, (x, y))

    # Gambar jejak jalur yang sudah dikunjungi
    for row in tree:
        for node in row:
            x = node.col * TILE_SIZE + TILE_SIZE // 2
            y = node.row * TILE_SIZE + TILE_SIZE // 2
            radius = TILE_SIZE // 6

            if node.visited:
                screen.draw.filled_circle((x, y), radius, node.visited_color)

    # Gambar pemain jika proses BFS telah selesai
    player.draw()

def bfs(start_node):
    queue = deque()
    queue.append(start_node)

    while queue:
        current_node = queue.popleft()

        # Check if the current node is the exit node (2 in the maze)
        if maze[current_node.row][current_node.col] == 2:
            print("Selamat Anda menemukan sapi! Permainan selesai.")
            reconstruct_path(current_node)  # Print the forward path
            return True

        current_node.visited_color = (100, 100, 100, 100)  # Warna untuk tile yang sudah dikunjungi
        current_node.visited = True

        time.sleep(0.002)
        # Define possible moves (up, down, left, right)
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in moves:
            new_row, new_col = current_node.row + dr, current_node.col + dc

            # Check if the new position is valid and not visited
            if (
                0 <= new_row < len(maze)
                and 0 <= new_col < len(maze[0])
                and maze[new_row][new_col] != 1
                and not tree[new_row][new_col].visited
            ):
                neighbor = tree[new_row][new_col]
                neighbor.set_parent(current_node)  # Set the parent
                queue.append(neighbor)
    print("Tidak ada jalur menuju sapi.")
    return False



def reconstruct_path(current_node):
    path = []
    while current_node:
        path.append((current_node.row, current_node.col))
        current_node = current_node.parent

    path.reverse()  # Reverse the path to get it from start to finish
    for row, col in path:
        node = tree[row][col]
        node.visited_color = COLOR_WHITE
        time.sleep(0.05)

def start_bfs():
    row = int(player.y / TILE_SIZE)
    col = int(player.x / TILE_SIZE)
    bfs(tree[row][col])

def update():
    global dfs_thread_started
    if not exit_found and not dfs_thread_started:
        dfs_thread_started = True
        thread = threading.Thread(target=start_bfs)
        thread.start()

def on_key_down(key):
    global exit_found
    if maze[int(player.y / TILE_SIZE)][int(player.x / TILE_SIZE)] == 2:
        print("Selamat Anda menemukan sapi! Permainan selesai.")
        return

    if key == keys.LEFT:
        move_player(-1, 0)
    elif key == keys.RIGHT:
        move_player(1, 0)
    elif key == keys.UP:
        move_player(0, -1)
    elif key == keys.DOWN:
        move_player(0, 1)

def move_player(dx, dy):
    global exit_found

    row = int(player.y / TILE_SIZE)
    col = int(player.x / TILE_SIZE)

    new_row, new_col = row + dy, col + dx

    if new_row >= 0 and new_row < len(maze) and new_col >= 0 and new_col < len(maze[0]):
        if maze[new_row][new_col] != 1:
            player.x = new_col * TILE_SIZE
            player.y = new_row * TILE_SIZE



