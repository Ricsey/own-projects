public class GameOfLife {
    public int N = 20; //size of grid
    public int[][] grid = new int[N][N];
    public int seedCount = 100;

    private static void printGrid(int[][] grid) {
        String printval;
        for (int[] row : grid) {
            for (int value : row) {
                if (value == 0) {
                    printval = "'";
                } else {
                    printval = "o";
                }
                System.out.print(printval + " ");
            }
            System.out.println();
        }
        System.out.println();
    }

    public int[][] initialize_grid(int N) {
        int[][] new_grid = new int[N][N];
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                new_grid[i][j] = 0;
            }
        }
        return new_grid;
    }

	public void randomSeed(int[][] grid){
		for ( int i = 0; i < seedCount; i++ ){
			int x = (int)(Math.random() * N);
			int y = (int)(Math.random() * N);
			grid[x][y] = 1;
		}
    }


    public int getAliveNeighbors(int[][] grid, int row, int col) {
        int[][] neighbour_dirs = {
            {-1, -1},
            {-1, 0},
            {-1, 1},
            {1, -1},
            {0, -1},
            {1, 0},
            {0, 1},
            {1, 1}
        };
        int alive_neighbours_count = 0;
        for (int[] dir : neighbour_dirs) {
            int new_row = row + dir[0];
            int new_col = col + dir[1];
            if (new_row < N && new_row >= 0 && new_col < N && new_col >= 0) { // dir is inside the grid
                if (grid[new_row][new_col] == 1) {
                    alive_neighbours_count += 1;
                }
            }
        }
        return alive_neighbours_count;
    }
    
    public void copyArray(int[][] src_array, int[][] dest_array, int size){
        for (int i = 0; i < src_array.length; i++) {
            for (int j = 0; j < src_array[i].length; j++) {
                dest_array[i][j] = src_array[i][j];
            }
        }
    }

    private boolean allElementsZero(int[][] array) {
        for (int[] row : array) {
            for (int value : row) {
                if (value != 0) {
                    return false;
                }
            }
        }
        return true;
    }

    private boolean arraysEqual(int[][] array1, int[][] array2) {
        for (int i = 0; i < array1.length; i++) {
            for (int j = 0; j < array1[0].length; j++) {
                if (array1[i][j] != array2[i][j]) {
                    return false;
                }
            }
        }
    
        return true;
    }

    public void main(String[] args) {
        int[][] grid = initialize_grid(N);

        randomSeed(grid);
        printGrid(grid);
        
        int[][] prev_grid = new int[N][N];
        int[][] new_grid = initialize_grid(N);
        copyArray(grid, prev_grid, N);
        while (true) {
            copyArray(prev_grid, new_grid, N);
            for (int i = 0; i < N; i++) {
                for (int j = 0; j < N; j++) {
                    int alive_neighbours = getAliveNeighbors(prev_grid, i, j);
                    // if cell alive
                    if (grid[i][j] == 1) {
                        if (alive_neighbours < 2 || alive_neighbours > 3) {
                            new_grid[i][j] = 0;                            
                        } else if (alive_neighbours == 2 || alive_neighbours == 3) {
                            new_grid[i][j] = 0;
                        }
                    }
                    // if cell is dead
                    else {
                        if (alive_neighbours == 3) {
                            new_grid[i][j] = 1;
                        }
                    }
                }
            }
            printGrid(new_grid);
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            if (allElementsZero(new_grid) || arraysEqual(new_grid, prev_grid)) {
                break;                
            }
            copyArray(new_grid, prev_grid, N);
        }
    }
}
