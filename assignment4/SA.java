package assignment4;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Random;

public class SA {

	public static double highestEvaluated = 0;
	private static double startTemperature = 1000;
	private static double decreseValue = 0.01;
	private static double currentTemperature = 0;
	
	
	// Tar inn startnodene
	public static Node SA(Node startNodes) {
		System.out.println("Start " + "\n" + startNodes);
		
		Node currentNode = startNodes;
		currentTemperature = startTemperature;
		
		
		// kjører så lenge temperaturen er positiv
		while( currentTemperature > 0) {
			
			//lager labonodelisten
			ArrayList<Node> neighbours = new ArrayList<Node>();
			
			currentTemperature -= decreseValue;
			System.out.println(currentTemperature);
			
			// verdien som den objektive funksjonen evaluate returnerer for løsningen
			double evCurrent = currentNode.evaluate();
			
			//og dersom den objektive funksjonen returnerer 1 er den optimale løsingen funnet! YAY
			if (evCurrent >= 1) return currentNode;
			
			
			double maxEval = 0;
			Node nextNode = null;
			neighbours = currentNode.neighbours();
			
			//alle naboer blir evaluert og den med høyeste verdi blir satt til nabonoden
			for (int i = 0; i < neighbours.size(); i++) {
				double evalForNeighbours = neighbours.get(i).evaluate();
				if (evalForNeighbours > maxEval) {
					maxEval = evalForNeighbours;
					nextNode = neighbours.get(i);
				}
			}
			

			double q = ((maxEval - evCurrent) / evCurrent);
			double p = Math.min(1.0, Math.exp((-q) / currentTemperature));
			double x = Math.random();
			
			
			// sjekker om vi er nærmere en løsning en forrige gang
			if (highestEvaluated < maxEval) highestEvaluated = maxEval;
	
			
			
			if (x > p) currentNode = nextNode;
			
			else{
				Random random = new Random();
				currentNode = neighbours.get(random.nextInt(neighbours.size()));
			}
		}
		
		
		//Dersom ingen løsning blir funnet det en ikke-optimalisert løsning som returneres.
		return currentNode;
	}
	
	//Her er bare initialisering av brett, node og printing av resultat om løsningen er optimal eller ikke
	public static void run(int size, int k) {
		Board board = new Board(size, k);
		Node node = new Node(board);

		node.placeNodesInList();

		Node result = SA(node);

		System.out.println("Resultat: " + "\n" + result);
		if (highestEvaluated == 1.0) System.out.println("Optimal løsning funnet! Funksjonen returnerte " + highestEvaluated);
		else System.out.println("Uffda, algoritmen klarte ikke å finne en optimal løsning"); System.out.println("Optimaliseringsverdien: " + highestEvaluated);

	}
}
