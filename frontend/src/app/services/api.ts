import { config } from "@/app/config/config";
import { Protein } from "@/app/data/proteins";

const API_URL = config.API_BASE_URL;
const NEO4J_URL = "http://localhost:8080";

export async function fetchAllProteins(): Promise<Protein[]> {
  if (config.USE_MOCK_DATA) {
    const response = await fetch('/mock-proteins.json');
    return response.json();
  }

  try {
    const response = await fetch(`${API_URL}/protein/`);
    if (!response.ok) throw new Error("Failed to fetch proteins");
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching proteins:", error);
    return [];
  }
}

export async function fetchProteinByEntry(entry: string): Promise<Protein | null> {
  if (config.USE_MOCK_DATA) {
    const proteins = await fetchAllProteins();
    return proteins.find(p => p.entry === entry) || null;
  }

  try {
    const response = await fetch(`${API_URL}/protein/?identifier=${entry}`);
    if (!response.ok) throw new Error("Failed to fetch protein");
    const data = await response.json();
    return data[0] || null;
  } catch (error) {
    console.error("Error fetching protein:", error);
    return null;
  }
}

export interface ProteinCorrelation {
  Entry: string;
  JaccardCorrelations: Array<{
    Entry: string;
    Jaccard: number;
  }>;
}

export async function fetchProteinCorrelations(entry?: string): Promise<ProteinCorrelation[]> {
  if (config.USE_MOCK_DATA) {
    const response = await fetch('/mock-correlations.json');
    const data = await response.json();
    return entry ? data.filter((p: ProteinCorrelation) => p.Entry === entry) : data;
  }

  try {
    const url = entry ? `${NEO4J_URL}/api/protein?entry=${entry}` : `${NEO4J_URL}/api/protein`;
    const response = await fetch(url);
    if (!response.ok) throw new Error("Failed to fetch correlations");
    return response.json();
  } catch (error) {
    console.error("Error fetching correlations:", error);
    return [];
  }
}
