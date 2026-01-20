import { Protein } from "@/app/data/proteins";
import { Dna, Activity, Link2, Copy } from "lucide-react";
import { useState } from "react";

interface ProteinDetailProps {
  protein: Protein | null;
  relatedProteins: Protein[];
  onSelectProtein: (protein: Protein) => void;
}

export function ProteinDetail({ protein, relatedProteins, onSelectProtein }: ProteinDetailProps) {
  const [showFullSequence, setShowFullSequence] = useState(false);
  
  if (!protein) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-gray-400">
        <Dna className="w-16 h-16 mb-4" />
        <p>Select a protein to view details</p>
      </div>
    );
  }

  const sequencePreview = protein.sequence.substring(0, 100);
  const copySequence = () => {
    navigator.clipboard.writeText(protein.sequence);
  };

  return (
    <div className="h-full overflow-y-auto p-6">
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-start gap-3 mb-2">
            <div className="p-3 bg-blue-100 rounded-lg">
              <Dna className="w-8 h-8 text-blue-600" />
            </div>
            <div className="flex-1">
              <h1 className="text-xl mb-1">{protein.protein_name.split('(')[0].trim()}</h1>
              <div className="flex items-center gap-2 flex-wrap">
                <span className="px-2 py-0.5 bg-gray-100 rounded text-sm">
                  Entry: {protein.entry}
                </span>
                <span className="px-2 py-0.5 bg-gray-100 rounded text-sm">
                  {protein.entry_name}
                </span>
                <span className={`px-2 py-0.5 rounded text-sm ${
                  protein.reviewed === 'reviewed' 
                    ? 'bg-green-100 text-green-700' 
                    : 'bg-yellow-100 text-yellow-700'
                }`}>
                  {protein.reviewed}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Full Protein Name */}
        {protein.protein_name.includes('(') && (
          <div className="bg-white border-2 border-gray-200 rounded-lg p-6 mb-6">
            <h3 className="mb-3">Alternate Names</h3>
            <p className="text-gray-700">{protein.protein_name}</p>
          </div>
        )}

        {/* Properties Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div className="bg-white border-2 border-gray-200 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2 text-gray-600">
              <Activity className="w-5 h-5" />
              <span>Organism</span>
            </div>
            <p className="text-lg">{protein.organism}</p>
          </div>

          <div className="bg-white border-2 border-gray-200 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2 text-gray-600">
              <Activity className="w-5 h-5" />
              <span>Gene Name</span>
            </div>
            <p className="text-lg">{protein.gene_name || 'N/A'}</p>
          </div>

          {protein.ec_number && (
            <div className="bg-white border-2 border-gray-200 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2 text-gray-600">
                <Activity className="w-5 h-5" />
                <span>EC Number</span>
              </div>
              <p className="text-lg">{protein.ec_number}</p>
            </div>
          )}

          {protein.interpro && (
            <div className="bg-white border-2 border-gray-200 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2 text-gray-600">
                <Activity className="w-5 h-5" />
                <span>InterPro Domains</span>
              </div>
              <p className="text-sm font-mono">{protein.interpro.split(';').filter(Boolean).length} domains</p>
            </div>
          )}
        </div>

        {/* Sequence */}
        <div className="bg-white border-2 border-gray-200 rounded-lg p-6 mb-6">
          <div className="flex items-center justify-between mb-3">
            <h3>Protein Sequence</h3>
            <button
              onClick={copySequence}
              className="flex items-center gap-2 px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded transition-colors"
            >
              <Copy className="w-4 h-4" />
              Copy
            </button>
          </div>
          <div className="bg-gray-50 p-4 rounded font-mono text-xs break-all">
            {showFullSequence ? protein.sequence : `${sequencePreview}...`}
          </div>
          <div className="mt-2 text-sm text-gray-600">
            Length: {protein.sequence.length} amino acids
          </div>
          {protein.sequence.length > 100 && (
            <button
              onClick={() => setShowFullSequence(!showFullSequence)}
              className="mt-2 text-blue-600 hover:text-blue-700 text-sm"
            >
              {showFullSequence ? 'Show less' : 'Show full sequence'}
            </button>
          )}
        </div>

        {/* Similar Proteins */}
        <div className="bg-white border-2 border-gray-200 rounded-lg p-6">
          <div className="flex items-center gap-2 mb-4">
            <Link2 className="w-5 h-5" />
            <h3>Similar Proteins ({relatedProteins.length})</h3>
          </div>

          {relatedProteins.length === 0 ? (
            <p className="text-gray-500">No similar proteins found</p>
          ) : (
            <div className="grid gap-3">
              {relatedProteins.map((relatedProtein) => (
                <button
                  key={relatedProtein.entry}
                  onClick={() => onSelectProtein(relatedProtein)}
                  className="text-left p-4 bg-gray-50 hover:bg-blue-50 rounded-lg border-2 border-gray-200 hover:border-blue-300 transition-colors"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 flex-wrap mb-1">
                        <h4 className="text-base">{relatedProtein.protein_name.split('(')[0].trim()}</h4>
                        <span className="px-2 py-0.5 bg-white rounded text-xs text-gray-600">
                          {relatedProtein.entry}
                        </span>
                        <span className={`px-2 py-0.5 rounded text-xs ${
                          relatedProtein.reviewed === 'reviewed' 
                            ? 'bg-green-100 text-green-700' 
                            : 'bg-yellow-100 text-yellow-700'
                        }`}>
                          {relatedProtein.reviewed}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600">
                        {relatedProtein.organism}
                      </p>
                      <div className="flex gap-4 mt-2 text-xs text-gray-500">
                        <span>Gene: {relatedProtein.gene_name || 'N/A'}</span>
                        <span>Sequence: {relatedProtein.sequence.length} aa</span>
                      </div>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}