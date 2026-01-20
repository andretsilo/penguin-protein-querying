import { useState, useMemo, useEffect } from "react";
import { ProteinList } from "@/app/components/ProteinList";
import { ProteinDetail } from "@/app/components/ProteinDetail";
import { ProteinGraph } from "@/app/components/ProteinGraph";
import { Protein, getSimilarProteins } from "@/app/data/proteins";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/app/components/ui/tabs";
import { fetchAllProteins } from "@/app/services/api";

export default function App() {
  const [selectedProtein, setSelectedProtein] = useState<Protein | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [proteins, setProteins] = useState<Protein[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAllProteins()
      .then(data => {
        setProteins(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const filteredProteins = useMemo(() => {
    if (!searchQuery.trim()) return proteins;
    return proteins.filter(protein => 
      protein.entry.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [searchQuery, proteins]);

  // Get similar proteins based on the selected protein
  const relatedProteins = selectedProtein
    ? getSimilarProteins(selectedProtein.entry)
    : [];

  return (
    <div className="size-full bg-gray-50">
      {loading ? (
        <div className="flex items-center justify-center h-screen">
          <p>Loading proteins...</p>
        </div>
      ) : (
        <div className="h-full grid grid-cols-1 lg:grid-cols-[400px,1fr]">
        {/* Protein List */}
        <div className="bg-white border-r border-gray-200 h-full lg:h-screen overflow-hidden">
          <ProteinList
            proteins={filteredProteins}
            selectedProtein={selectedProtein}
            onSelectProtein={setSelectedProtein}
            searchQuery={searchQuery}
            onSearchChange={setSearchQuery}
          />
        </div>

        {/* Protein Detail */}
        <div className="bg-gray-50 h-full lg:h-screen">
          <Tabs defaultValue="details" className="h-full flex flex-col">
            <TabsList className="mx-6 mt-6">
              <TabsTrigger value="details">Details</TabsTrigger>
              <TabsTrigger value="graph">Graph View</TabsTrigger>
            </TabsList>
            <TabsContent value="details" className="flex-1 overflow-auto">
              <ProteinDetail
                protein={selectedProtein}
                relatedProteins={relatedProteins}
                onSelectProtein={setSelectedProtein}
              />
            </TabsContent>
            <TabsContent value="graph" className="flex-1">
              <ProteinGraph selectedEntry={selectedProtein?.entry} />
            </TabsContent>
          </Tabs>
        </div>
      </div>
      )}
    </div>
  );
}