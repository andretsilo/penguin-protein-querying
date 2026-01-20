import { useEffect, useRef } from "react";

interface ProteinGraphProps {
  selectedEntry?: string;
}

export function ProteinGraph({ selectedEntry }: ProteinGraphProps) {
  return (
    <div className="w-full h-full flex items-center justify-center p-6">
      <div className="text-center">
        <h3 className="text-xl mb-4">Graph Visualization</h3>
        <p className="text-gray-600 mb-4">
          {selectedEntry 
            ? `Showing connections for ${selectedEntry}` 
            : "Select a protein to view its similarity network"}
        </p>
        <p className="text-sm text-gray-500">
          Neo4j graph visualization will be available when the database is connected.
        </p>
      </div>
    </div>
  );
}
