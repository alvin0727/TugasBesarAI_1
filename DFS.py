import time
import threading

TILE_SIZE = 32 #tile size
WIDTH = 20 * TILE_SIZE # 32 tile
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
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

path = []

player = Actor("ufo", anchor=(0, 0), pos=(9 * TILE_SIZE, 2 * TILE_SIZE))
class MazeNode:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.visited_color = COLOR_WHITE
        self.path_color = COLOR_WHITE

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

    # Gambar pemain jika proses DFS telah selesai
    player.draw()

def dfs(node):
    if node.row < 0 or node.row >= len(maze) or node.col < 0 or node.col >= len(maze[0]):
        return False
    if maze[node.row][node.col] == 2:
        path.append((node.row, node.col))
        node.path_color = COLOR_GREEN  # Menandakan jalur tercepat
        return True
    if maze[node.row][node.col] == 1 or node.visited:
        return False

    node.visited = True
    node.visited_color = (100, 100, 100, 100)  # Warna untuk tile yang sudah dikunjungi
    draw()  # Gambar tampilan setelah mengunjungi node

    # Penundaan selama 0.3 detik
    time.sleep(0.3)

    if dfs(tree[node.row][node.col - 1]):
        return True
    if dfs(tree[node.row][node.col + 1]):
        return True
    if dfs(tree[node.row - 1][node.col]):
        return True
    if dfs(tree[node.row + 1][node.col]):
        return True

    node.visited_color = COLOR_WHITE  # Kembalikan warna jika jalur tidak ditemukan
    return False


def start_dfs():
    row = int(player.y / TILE_SIZE)
    col = int(player.x / TILE_SIZE)
    dfs(tree[row][col])

def update():
    global dfs_thread_started
    if not exit_found and not dfs_thread_started:
        dfs_thread_started = True
        thread = threading.Thread(target=start_dfs)
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
