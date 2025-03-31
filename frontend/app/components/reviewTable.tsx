"use client";
import {
  ArrowDownLeftIcon,
  ChevronDoubleLeftIcon,
  ChevronDoubleRightIcon,
} from "@heroicons/react/24/outline";
import React from "react";
import { useState, useEffect } from "react";

interface Produto {
  id: number;
  product_dsc: string;
  product_shor_dsc: string;
  _20231226: number;
}

const ReviewTable = () => {
  const [data, setData] = useState<Produto[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    let isMounted = true;
    
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:8000/generate_risky_products");
        
        console.log(response);
        
        // Check if response is ok
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        // Parse response carefully
        const responseData = await response.json();
        console.log("Response data:", responseData);
        const product : Produto[] = responseData as Produto[];
        console.log("Response data:", product);
        
        // Only update state if component is still mounted
        if (isMounted) {
          // Make sure we have an array
          if (Array.isArray(responseData)) {
            setData(responseData);
          } else if (responseData && typeof responseData === 'object') {
            // Try to extract array if it's nested in an object
            const possibleArrays = Object.values(responseData).filter(val => Array.isArray(val));
            if (possibleArrays.length > 0) {
              setData(possibleArrays[0] as Produto[]);
            } else {
              console.log("Could not find array in response:", responseData);
              setData([]);
            }
          } else {
            console.log("Unexpected response format:", responseData);
            setData([]);
          }
          setLoading(false);
        }
      } catch (err) {
        if (isMounted) {
          console.log("Error fetching data:", err);
          setError(err instanceof Error ? err.message : "Unknown error occurred");
          setLoading(false);
        }
      }
    };

    fetchData();
    
    // Cleanup function to handle unmounting
    return () => {
      isMounted = false;
    };
  }, []);

  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 7;
  
  // Safely calculate max page
  const maxPage = data && data.length > 0 ? Math.ceil(data.length / itemsPerPage) : 1;
  
  // Make sure current page is valid
  useEffect(() => {
    if (currentPage > maxPage) {
      setCurrentPage(maxPage);
    }
  }, [maxPage, currentPage]);
  
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;

  const handlePrevPage = () => {
    setCurrentPage((prev) => Math.max(prev - 1, 1));
  };
  
  const handleNextPage = () => {
    setCurrentPage((prev) => Math.min(prev + 1, maxPage));
  };
  
  // Create a safe version of items to display
  const itemsToDisplay = React.useMemo(() => {
    if (!Array.isArray(data)) return [];
    try {
      return data.slice(startIndex, endIndex);
    } catch (err) {
      console.log("Error slicing data:", err);
      return [];
    }
  }, [data, startIndex, endIndex]);

  return (
    <div className="px-12">
      <h1 className="text-4xl text-coral font-bold">Produtos que necessitam de revisão:</h1>
      <div className="flex flex-col text-white overflow-x-auto w-full h-[500px] gap-1 mt-10">
        {loading ? (
          <div className="text-coral text-xl flex justify-center items-center h-full">
            Carregando...
          </div>
        ) : error ? (
          <div className="text-red-500 text-xl flex justify-center items-center h-full">
            Erro: {error}
          </div>
        ) : itemsToDisplay.length === 0 ? (
          <div className="text-coral text-xl flex justify-center items-center h-full">
            Nenhum produto encontrado
          </div>
        ) : (
          itemsToDisplay.map((produto: Produto, index) => (
            <div
              className={`flex pl-9 pr-3 items-center gap-56 h-16 ${
                index % 2 === 0 ? "bg-[#821300]" : "bg-[#a0140F]"
              } rounded-2xl`}
              key={produto.id || index}
            >
              <p className="font-bold text-lg flex-1">{produto.product_dsc}</p>
              <span
                className={`${
                  produto._20231226 < 0.9 && produto._20231226 > 0.8
                    ? "text-yellow-500"
                    : "text-red-500"
                } flex items-center gap-2 bg-white/100 box-shadow rounded-xl px-3 py-1`}
              >
                <ArrowDownLeftIcon className="h-8 w-8 font-extrabold" />
                <p className="text-xl font-extrabold">{produto._20231226.toFixed(2)}</p>
              </span>
            </div>
          ))
        )}
      </div>
      {data && data.length > 0 && (
        <div className="flex px-3 gap-5 mt-4 items-center">
          <ChevronDoubleLeftIcon
            onClick={handlePrevPage}
            className="border-2 border-coral rounded-lg h-9 w-9 transition-all duration-300 ease-in-out cursor-pointer hover:bg-coral hover:text-white p-1 active:scale-90"
          />
          <span className="text-coral">
            Página {currentPage} de {maxPage}
          </span>
          <ChevronDoubleRightIcon
            onClick={handleNextPage}
            className="border-2 border-coral rounded-lg h-9 w-9 transition-all duration-300 ease-in-out hover:bg-coral hover:text-white p-1 cursor-pointer active:scale-90"
          />
        </div>
      )}
    </div>
  );
};

export default ReviewTable;