package assignment4;

import java.util.ArrayList;
import java.util.Random;

import javax.swing.RowFilter;

public class Node{

	private static final int MOVE_UP = 0;
	private static final int MOVE_DOWN = 2;
	
	private boolean[][] eggs;
	private Board board;
	

	
	public Node(Board board, boolean[][] eggs){
		this.board = board;
		this.eggs = eggs;
	}

	public Node(Board board){
		this.board = board;
		eggs = new boolean[board.getRows()][board.getCols()];
	}
	
	//metode som returnerer en liste med alle nabonoder etter de er flyttet til en bedre posisjon
	public ArrayList<Node> neighbours() {
		ArrayList<Node> neighbours = new ArrayList<Node>();
		for (int i = 0; i < board.getCols(); i++) {
			for (int j = 0; j < board.getRows(); j++) {
				if(eggs[j][i]){
					if (isLegalMove(i, j, MOVE_UP)) {
						neighbours.add(new Node(board, moveNode(eggs, i, j, MOVE_UP)));
					}
					
					if (isLegalMove(i, j, MOVE_DOWN)) {
						neighbours.add(new Node(board, moveNode(eggs, i, j, MOVE_DOWN)));
					}
				}
			}
		}
		return neighbours;
	}

	
	//Metode for å flytte på egget og nulle ut den gamle posisjonen
	private static boolean[][] moveNode(boolean[][] eggs, int oldX, int oldY, int direction) {
	    
	    boolean[][] newPos = new boolean[eggs.length][eggs[0].length];
	    for (int i = 0; i < eggs.length; i++) {
	        System.arraycopy(eggs[i], 0, newPos[i], 0, eggs[i].length);
	    }
	    
	    newPos[oldY][oldX] = false;
	    
	    if (direction == MOVE_UP) {
	    	newPos[oldY - 1][oldX] = true;
	    }
	    else if (direction == MOVE_DOWN) {
	    	newPos[oldY + 1][oldX] = true;
	    }
	    return newPos;
	}
	
	// metode for å evaluere om en node er optimalisert og returnerer en verdi mellom 0 og 1, hvor 1 er optimalisert
	public double evaluate() {
		int row = board.getRows();
		int col = board.getCols();
		int keggs = board.k_eggs();
		
		int[] row_k = new int[col];
		int[] col_k = new int[row];
		int[] diagonal_left_k = new int[row + col - 1];
		int[] diagonal_rigth_k = new int[row + col - 1];
		double value = 0;
				
		for (int y = 0; y < row; y++) {
			for (int x = 0; x < col; x++) {
				if (eggs[y][x]) {
					row_k[y] ++;
					col_k[x] ++;
					int index_diagonal_rigth = col - x + y - 1;
					int index_diagonal_left = x + y;
					diagonal_rigth_k[index_diagonal_rigth] ++;
					diagonal_left_k[index_diagonal_left] ++;
				}
			}
		}
		
		for (int y = 0; y < row; y++) {
			for (int x = 0; x < col; x++) {
				if (eggs[y][x]) {
					int index_diagonal_right = col - x + y - 1;
					int index_diagonal_left = x + y;
					if ((row_k[y] <= keggs) && (col_k[x] <= keggs) && (diagonal_rigth_k[index_diagonal_right] <= keggs) && 
							(diagonal_left_k[index_diagonal_left] <= keggs)) {
						value++;
					}
				}
			}
		}
		//Hvert egg på brettet får en optimaliseringsverdi
		return value / (row * keggs);			
	}

	
	// plasserer eggene på blettet
	public void placeNodesInList() {
		Random random = new Random();
		for (int i = 0; i < board.getRows(); i++) {
			int teller = 0;
			
			while (teller < board.k_eggs()) {
				int row = random.nextInt(board.getRows()); 
				if(!eggs[row][i]) {
					eggs[row][i] = true;
					teller ++;
				}
			}
		}
	}

	/*Sjekker om det er lov å flytte på egget, sjekker om det er i ytterst i raden og/eller colonnen, 
	samt at det ikke finnes et egg i posisjonen fra før av!*/
	private boolean isLegalMove(int x, int y, int direction) {
		if ((direction == MOVE_UP) && (y-1 >= 0) && (!eggs[y-1][x])) return true;
		else if ((direction == MOVE_DOWN) && (y + 1 < board.getRows()) && (!eggs[y+1][x])) return true;
		return false;
	}
	
	//metode for å printe brettet med eggene på, '0' egg, '-' tomt
	public String toString() {
		String print = "";
		
		for (int y = 0; y < board.getRows(); y++) {
			for (int x = 0; x < board.getRows(); x++) {
				if (eggs[y][x]) {
					print += "0  ";
				}
				else {
					print += "-  ";
				}
			}
			print += "\n";
		}
		return print;
	}
	
}


/*hjelpeklasse for brettet som holder på hvor mange egg som er tilatt på 
brettet(rad,diag,col) og hvor stort brettet er*/
class Board {

	
	private int rows;
	private int cols;
	private int k_eggs;
	
	public Board(int board_size, int k_eggs){
		this.rows = board_size;
		this.cols = board_size;
		this.k_eggs = k_eggs;
	}
	
	public int getRows(){
		return rows;
	}
	public int getCols(){
		return cols;
	}
	public int k_eggs(){
		return k_eggs;
	}
}
