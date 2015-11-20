package assignment4;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class SA_run {

	//Kjører programmet
	public static void main(String[] args) throws IOException{
		int size = 0;
		int k = 0;
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		System.out.print("Enter the value of N=M: ");

		try{
			size = Integer.parseInt(br.readLine());
		}catch(NumberFormatException nfe){
			System.err.println("Invalid Format!");
			System.exit(0);
		}    
		System.out.print("Enter the value of K: ");
		try{
			k = Integer.parseInt(br.readLine());
		}catch(NumberFormatException nfe2){
			System.err.println("Invalid Format!");
			System.exit(0);
		}

		SA.run(size, k);

	}
}
