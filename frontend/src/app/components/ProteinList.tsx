import { Protein } from "@/app/data/proteins";
import { Dna, Search } from "lucide-react";
import { Input } from "@/app/components/ui/input";

interface ProteinListProps {
  proteins: Protein[];
  selectedProtein: Protein | null;
  onSelectProtein: (protein: Protein) => void;
  searchQuery: string;
  onSearchChange: (query: string) => void;
}

export function ProteinList({ proteins, selectedProtein, onSelectProtein, searchQuery, onSearchChange }: ProteinListProps) {
  return (
    <div className="flex flex-col h-full">
      <div className="p-6 border-b">
        <h2 className="flex items-center gap-2">
          <Dna className="w-6 h-6" />
          Protein Database
        </h2>
        <p className="text-sm text-gray-600 mt-1">{proteins.length} proteins available</p>
        <div className="relative mt-4">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
          <Input
            type="text"
            placeholder="Search by entry ID..."
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            className="pl-10"
          />
        </div>
      </div>
      
      <div className="flex-1 overflow-y-auto">
        <div className="p-2">
          {proteins.map((protein) => (
            <button
              key={protein.entry}
              onClick={() => onSelectProtein(protein)}
              className={`w-full text-left p-4 rounded-lg mb-2 transition-colors ${
                selectedProtein?.entry === protein.entry
                  ? "bg-blue-100 border-2 border-blue-500"
                  : "bg-white border-2 border-gray-200 hover:border-blue-300 hover:bg-blue-50"
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 flex-wrap">
                    <h3 className="text-base">{protein.protein_name.split('(')[0].trim()}</h3>
                    <span className="px-2 py-0.5 bg-gray-100 rounded text-xs text-gray-600">
                      {protein.entry}
                    </span>
                    <span className={`px-2 py-0.5 rounded text-xs ${
                      protein.reviewed === 'reviewed' 
                        ? 'bg-green-100 text-green-700' 
                        : 'bg-yellow-100 text-yellow-700'
                    }`}>
                      {protein.reviewed}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mt-1">
                    {protein.organism}
                  </p>
                  <div className="flex gap-4 mt-2 text-xs text-gray-500">
                    <span>Gene: {protein.gene_name || 'N/A'}</span>
                    {protein.similar_proteins && (
                      <span>Similar: {protein.similar_proteins.length}</span>
                    )}
                  </div>
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}