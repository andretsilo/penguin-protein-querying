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
    const params = new URLSearchParams({ identifier: "A0A087QH", name: "", description: "" });
    const response = await fetch(`${API_URL}/protein?${params}`);
    if (!response.ok) throw new Error("Failed to fetch proteins");
    return response.json();
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
    const params = new URLSearchParams({ identifier: entry, name: "", description: "" });
    const response = await fetch(`${API_URL}/protein?${params}`);
    if (!response.ok) throw new Error("Failed to fetch protein");
    const data = await response.json();
    return data[0] || null;
  } catch (error) {
    console.error("Error fetching protein:", error);
    return null;
  }
}

export interface ProteinCorrelation {
  entry: string;
  jaccardCorrelations: Array<{
    entry: string;
    jaccard: number;
  }>;
}

export async function saveProteinCorrelations(correlations: ProteinCorrelation[]) {
  if (config.USE_MOCK_DATA) {
    return { status: "success" };
  }

  const response = await fetch(`${NEO4J_URL}/api/proteins`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(correlations)
  });
  if (!response.ok) throw new Error("Failed to save correlations");
  return { status: "success" };
}

export async function fetchProteinCorrelations(entry: string): Promise<Array<{ entry: string }>> {
  if (config.USE_MOCK_DATA) {
    const response = await fetch('/mock-correlations.json');
    return response.json();
  }

  try {
    const params = new URLSearchParams({ entry });
    const response = await fetch(`${NEO4J_URL}/api/proteins?${params}`);
    if (!response.ok) throw new Error("Failed to fetch correlations");
    return response.json();
  } catch (error) {
    console.error("Error fetching correlations:", error);
    return [];
  }
}
