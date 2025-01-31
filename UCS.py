import heapq
import threading
import time

TILE_SIZE = 32  # Tile size
WIDTH = 20 * TILE_SIZE
HEIGHT = 20 * TILE_SIZE
tiles = ['empty', 'wall', 'cow']
moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
COLOR_GREEN = (0, 255, 0)
COLOR_WHITE = (255, 255, 255)
class MazeNode:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.parent = None  # Added to store the parent node
        self.cost = float('inf')  # Added to store the cost from the start node

    def set_parent(self, parent_node):
        self.parent = parent_node

    def __lt__(self, other):
        return self.cost < other.cost

def build_tree():
    tree = []
    for row in range(len(maze)):
        row_nodes = []
        for col in range(len(maze[row])):
            node = MazeNode(row, col)
            row_nodes.append(node)
        tree.append(row_nodes)
    return tree

def reconstruct_path(end_node):
    path = []
    current_node = end_node
    while current_node is not None:
        path.append((current_node.row, current_node.col))
        current_node = current_node.parent
    return list(reversed(path))

def ucs(maze, start_node, end_value):
    # Initialize the priority queue with the start node and cost 0
    queue = [(0, start_node)]
    start_node.cost = 0

    while queue:
        # Get the node with the lowest cost
        cost, current_node = heapq.heappop(queue)

        # Check if we've reached the end (target node with the specified value)
        if maze[current_node.row][current_node.col] == end_value:
            path = reconstruct_path(current_node)
            return path, cost

        # Mark the current node as visited
        current_node.visited_color = (100, 100, 100, 100)
        current_node.visited = True
        time.sleep(0.002)
        # Explore the neighboring nodes
        for move in moves:
            x, y = current_node.row, current_node.col
            new_x, new_y = x + move[0], y + move[1]

            # Check if the neighbor is within bounds and not a wall
            if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] != 1:
                neighbor_node = tree[new_x][new_y]

                # Calculate the new cost
                new_cost = cost + maze[new_x][new_y]

                # If the neighbor has not been visited or has a lower cost, update it and add it to the queue
                if not neighbor_node.visited or new_cost < neighbor_node.cost:
                    neighbor_node.cost = new_cost
                    neighbor_node.set_parent(current_node)
                    heapq.heappush(queue, (new_cost, neighbor_node))

    # If no path is found, return an empty path and -1 cost
    return [], -1

# Contoh penggunaan:
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 7, 8, 3, 2, 4, 9, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1],
    [1, 3, 10, 10, 5, 4, 8, 1, 1, 4, 1, 1, 1, 1, 6, 1, 1, 1, 1, 1],
    [1, 4, 2, 10, 3, 3, 8, 1, 1, 9, 1, 1, 1, 5, 9, 4, 8, 4, 1, 1],
    [1, 1, 1, 1, 1, 1, 5, 1, 1, 8, 1, 1, 1, 6, 8, 5, 3, 3, 1, 1],
    [1, 1, 1, 1, 1, 1, 3, 1, 1, 8, 1, 1, 1, 1, 6, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 4, 1, 1, 7, 4, 5, 1, 1, 4, 1, 1, 1, 1, 1],
    [1, 5, 1, 1, 1, 1, 2, 9, 3, 5, 2, 6, 1, 1, 9, 1, 1, 1, 1, 1],
    [1, 4, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 8, 1, 1, 1, 1, 7, 8, 7, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 6, 8, 9, 2, 3, 5, 9, 4, 8, 6, 4, 7, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 7, 4, 1, 1, 1, 1, 1, 5, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 1, 1, 1, 5, 1],
    [1, 1, 1, 7, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 8, 4, 9, 3, 6, 1],
    [1, 1, 1, 4, 6, 7, 2, 3, 9, 7, 5, 9, 5, 5, 2, 7, 4, 4, 9, 1],
    [1, 1, 1, 5, 7, 2, 9, 5, 10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 8, 5, 3, 10, 9, 4, 6, 8, 5, 3, 20, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
player = Actor("ufo", anchor=(0, 0), pos=(1 * TILE_SIZE, 2 * TILE_SIZE))
def draw():
    screen.clear()
    for row in range(len(maze)):
        for column in range(len(maze[row])):
            x = column * TILE_SIZE
            y = row * TILE_SIZE
            tile_index = maze[row][column]

            if tile_index == 1:
                tile = tiles[1]  # Use 'wall' tile for value 1
            elif tile_index == 0 or (2 <= tile_index <= 10):
                tile = tiles[0]  # Use 'empty' tile for values 0 and 2-10
            elif tile_index == 20:
                tile = tiles[2]  # Use 'cow' tile for value 20
            else:
                # Handle any other values here
                tile = tiles[0]  # Use 'empty' as a default

            screen.blit(tile, (x, y))
    # Gambar jejak jalur yang sudah dikunjungi
    for row in tree:
        for node in row:
            x = node.col * TILE_SIZE + TILE_SIZE // 2
            y = node.row * TILE_SIZE + TILE_SIZE // 2
            radius = TILE_SIZE // 6

            if node.visited:
                screen.draw.filled_circle((x, y), radius, node.visited_color)

    player.draw()

tree = build_tree()
exit_found = False  # Define this appropriately
ucs_thread_started = False

# Define your maze and MazeNode class here

def start_ucs():
    row = int(player.y / TILE_SIZE)
    col = int(player.x / TILE_SIZE)
    end_value = 20  # Replace with the target value
    start_node = tree[row][col]
    path, cost = ucs(maze, start_node, end_value)

    # Handle the result as needed, e.g., updating the game environment
    if path:
        for row, col in path:
            node = tree[row][col]
            node.visited_color = COLOR_WHITE
            time.sleep(0.05)
        print("Shortest path:", path)
        print("Shortest path cost:", cost)
        node.visited_color = COLOR_WHITE
        # Update your game environment with the new path and cost here
    else:
        print("No path found")

def update():
    global ucs_thread_started
    if not exit_found and not ucs_thread_started:
        ucs_thread_started = True
        thread = threading.Thread(target=start_ucs)
        thread.start()


