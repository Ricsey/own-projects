import java.util.ArrayList;
import java.util.List;

public class ratinmaze {


    public static int[][] maze = {
        {0, 0, 0, 0},
        {0, 0, 0, 1},
        {0, 1, 0, 0},
        {0, 0, 1, 0}
    };
    public static int destinationRow = 3;
    public static int destinationCol = 3;


    public static List<List<int[]>> solutions = new ArrayList<>();
    public static int[][] visited = makeVisited(maze);
    public static List<int[]> solution = new ArrayList<>();

    public static void printSolution(List<int[]> solution) {
        if (solution.size() == 0) {
            System.out.println("No solution found");
        }
        solution.forEach(coord -> System.out.print("-> (" + coord[0] + "," + coord[1] + ") " ));
        System.out.println();
    }

    public static int[][] makeVisited(int[][] maze) {
        int rows = maze.length;
        int cols = maze[0].length;
    
        int[][] visited = new int[rows][cols];
    
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                visited[i][j] = 0;
            }
        }
    
        return visited;
    }

    public static boolean isSafeToGo(int[][] maze, int row, int col) {
        // inside the maze
        if (row < 0 || row >= maze.length) {
            return false;
        }
        if (col < 0 || col >= maze[row].length) {
            return false;
        }

        // it's a wall
        if (maze[row][col] == 1) {
            return false;
        }

        // not visited
        if (visited[row][col] == 1) {
            return false;            
        }
        return true;
    }

    public static void findPath(int[][] maze, int row, int col, List<int[]> path, List<List<int[]>> solutions) {
        if (row == destinationRow && col == destinationCol) {
            solutions.add(new ArrayList<>(path));
            return;
        }
        
        int[][] directions = {  {0, 1}, {1, 0}, {-1, 0}, {0, -1} };
        for (int[] dir : directions) {
            int newRow = row + dir[0];
            int newCol = col + dir[1];
            if (isSafeToGo(maze, newRow, newCol)) {
                visited[row][col] = 1;
                path.add(new int[] { newRow, newCol });
                findPath(maze, newRow, newCol, path, solutions);
                path.remove(path.size() - 1);                
            }
        }
        visited[row][col] = 0;
        return;
    }

    public static void main(String[] args) {
        List<List<int[]>> solutions = new ArrayList<>(new ArrayList<>());
        findPath(maze, 0, 0, new ArrayList<>(), solutions);
        // printSolution(solution);
        int sol_num = 0;
        for (List<int[]> solution : solutions) {
            System.out.println("Solution num:" + ++sol_num);
            printSolution(solution);
        }
    }
}