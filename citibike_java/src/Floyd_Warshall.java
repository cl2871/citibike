import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintStream;
import java.util.*;


public class Floyd_Warshall {

	// Globals
	static int threads;
	static Set<Integer> vertices = new HashSet<>();;
	static HashMap<Integer, HashMap<Integer, Float>> distances = new HashMap<>();
	static HashMap<Integer, HashMap<Integer, Float>> edges = new HashMap<>();
	static HashMap<Integer, HashMap<Integer, Integer>> next = new HashMap<>();
	
	public static void main(String[] args) throws FileNotFoundException{
		Scanner file = new Scanner(new File("JC_edges.csv"));
		PrintStream out = new PrintStream("distances_java.csv");
		
		//threads = Integer.parseInt(args[0]);
		
		/* Read edges file line by line
		 * Store edges between stations
		 * edges[start][end] = edge
		 */
		
		final long startTime = System.currentTimeMillis();
		
		String[] line;
		while (file.hasNext()){
			
			// read in line and parse stations and edges
			line = file.nextLine().split(",");
			int start_station_id = Integer.parseInt(line[0]);
			int end_station_id = Integer.parseInt(line[1]);
			float edge = Float.parseFloat(line[2]);
			
			// add stations to vertices set
			vertices.add(start_station_id);
			vertices.add(end_station_id);
			
			// add station HashMaps to edges if needed then set the edge
			if (!edges.containsKey(start_station_id)){
				HashMap<Integer, Float> newHashMap = new HashMap<>();
				edges.put(start_station_id, newHashMap);
			}
			if (!edges.containsKey(end_station_id)){
				HashMap<Integer, Float> newHashMap = new HashMap<>();
				edges.put(end_station_id, newHashMap);
			}
			edges.get(start_station_id).put(end_station_id, edge);
		}
		
		run_floyd_warshall_path_reconstruction();
		
		
		System.out.println(distances.get(3183).get(3201));
		System.out.println(Arrays.toString(build_shortest_path(3183, 3201).toArray()));
		
		final long endTime = System.currentTimeMillis();
		System.out.println("Total execution time: " + (endTime - startTime) );
		
		out.close();
		file.close();
	}

	public static void run_floyd_warshall_path_reconstruction(){
		
		// make a sorted list of vertices from vertices set 
		ArrayList<Integer> vertices_list = new ArrayList<>();
		vertices_list.addAll(vertices);
		Collections.sort(vertices_list);
		
		// initialize the inner HashMaps of distances and next
		for(Integer vertex : vertices_list){
			HashMap<Integer, Float> newHashMap1 = new HashMap<>();
			newHashMap1.put(vertex, (float) 0.0);
			HashMap<Integer, Integer> newHashMap2 = new HashMap<>();
			distances.put(vertex, newHashMap1);
			next.put(vertex, newHashMap2);
		}
		
		for (Integer vertex_1 : vertices_list){
			for (Integer vertex_2 : vertices_list){
				if (vertex_1 == vertex_2){
					continue;
				}
				if (edges.containsKey(vertex_1) && edges.get(vertex_1).containsKey(vertex_2)){
					// distances[vertex_1][vertex_2] = edges[vertex_1][vertex_2]
					distances.get(vertex_1).put(vertex_2, edges.get(vertex_1).get(vertex_2));
					// next[vertex_1][vertex_2] = vertex_2
					next.get(vertex_1).put(vertex_2, vertex_2);
				}
				else{
					distances.get(vertex_1).put(vertex_2, Float.MAX_VALUE);
					next.get(vertex_1).put(vertex_2, null);
				}
			}
		}
		
		for (Integer k : vertices_list){
			for (Integer i : vertices_list){
				for (Integer j : vertices_list){
					// distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])
					// update next[i][j] if using k is shorter
					if (distances.get(i).get(j) > distances.get(i).get(k) + distances.get(k).get(j)){
						distances.get(i).put(j, distances.get(i).get(k) + distances.get(k).get(j));
						next.get(i).put(j, k);
					}
				}
			}
		}	
	}
	
	public static ArrayList<Integer> build_shortest_path(Integer vertex_1, Integer vertex_2){
		ArrayList<Integer> path = new ArrayList<>();
		if (next.get(vertex_1) == null || next.get(vertex_1).get(vertex_2) == null){
			return null;
		}
		path.add(vertex_1);
		int current = vertex_1;
		while (current != vertex_2){
			current = next.get(current).get(vertex_2);
			path.add(current);
		}
		return path;
	}
}
