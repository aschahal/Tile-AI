import heapq

def get_manhattan_distance(from_state, to_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    INPUT: 
        Two states (if second state is omitted then it is assumed that it is the goal state)

    RETURNS:
        A scalar that is the sum of Manhattan distances for all tiles.
    """

    distance = 0
    for i, tile in enumerate(from_state):
        if tile != 0:
            # Find the index of the current tile in the goal state
            goal_index = to_state.index(tile)
            # Convert indices into coordinates for both states
            current_x, current_y = i % 3, i // 3
            goal_x, goal_y = goal_index % 3, goal_index // 3
            # Sum up the distances for each tile
            distance += abs(current_x - goal_x) + abs(current_y - goal_y)

    return distance

def print_succ(state):
    """
    INPUT: 
        A state (list of length 9)

    RETURNS:
        Prints the list of all the valid successors in the puzzle. 
    """
    succ_states = get_succ(state)

    for succ_state in succ_states:
        print(succ_state, "h={}".format(get_manhattan_distance(succ_state)))


def get_succ(state):
    """
    INPUT: 
        A state (list of length 9)

    RETURNS:
        A list of all the valid successors in the puzzle, while in a sorted format. 
    """
    succ_states = []
    empty_indices = [i for i, x in enumerate(state) if x == 0] # Find indices of empty spaces

    # Directions: left, right, up, down
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    for empty_index in empty_indices:
        x,y = empty_index % 3, empty_index // 3 # Convert index into coordinates
        for dx, dy in directions:
            # Calculate new position after moving
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3: # Check if new positon is within bounds
                new_index = ny * 3 + nx
                new_state = state[:]
                # Swap the tile and empty space
                new_state[empty_index], new_state[new_index] = new_state[new_index], new_state[empty_index]
                # Check if this state is a new state
                if new_state not in succ_states and new_state != state:
                    # Add new state 
                    succ_states.append(new_state)

    return sorted(succ_states)
    


def solve(state, goal_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    A* algorithm here

    INPUT: 
        An initial state (list of length 9)

    RETURNS:
        Prints a path of configurations from initial state to goal state along  h values, number of moves, and max queue number in specified format.
    """
    pq = []
    initial_h = get_manhattan_distance(state, goal_state)
    heapq.heappush(pq, (initial_h, state, (0, initial_h, -1))) # Pushing initial state with given format
    visited = {str(state): 0} # Track visited states
    parent_map = {str(state): -1} # Using state string as key for parent_map
    state_info_list = [(state, initial_h, 0)]
    max_length = 1 # Track max length of prority queue

    while pq:
        # Pop state with lowest cost
        current_cost, current_state, (g, _, parent_index) = heapq.heappop(pq)
        str_current_state = str(current_state)

        # Skip if this state has been visited with a lower cost
        if str_current_state in visited and visited[str_current_state] < g:
            continue

        # Update the visited states and parent map
        visited[str_current_state] = g
        parent_map[str_current_state] = parent_index
        state_info_list.append((current_state, current_cost - g, g))

        if current_state == goal_state:
            break

        # Explore the successor states
        for succ_state in get_succ(current_state):
            str_succ_state = str(succ_state)
            new_g = g + 1
            new_h = get_manhattan_distance(succ_state, goal_state)

            # If successor state is not visited or can be reached with a lower cost
            if str_succ_state not in visited or visited[str_succ_state] > new_g:
                heapq.heappush(pq, (new_g + new_h, succ_state, (new_g, new_h, len(state_info_list) - 1)))
                visited[str_succ_state] = new_g
                max_length = max(max_length, len(pq))
    
    # Reconstructing the path
    path = []
    current_index = len(state_info_list) - 1
    while current_index != -1:
        current_state, _, current_g = state_info_list[current_index]
        current_h = get_manhattan_distance(current_state, goal_state)
        path.append((current_state, current_h, current_g))
        current_index = parent_map[str(current_state)]

    path.reverse() # Reverse path to start from initial state

    # Printing the path
    for i, (current_state, h, moves) in enumerate(path):
        print(f"{current_state} h={h} moves: {i}")
    print(f"Max queue length: {max_length}")

    return path, max_length


if __name__ == "__main__":
    """
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    """
    print_succ([2,5,1,4,0,6,7,0,3])
    print()

    print(get_manhattan_distance([2,5,1,4,0,6,7,0,3], [1, 2, 3, 4, 5, 6, 7, 0, 0]))
    print()

    solve([6, 0, 0, 3, 5, 1, 7, 2, 4])
    print()
