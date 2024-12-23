import React from "react";

interface CountCard {
  title: string;
  totalCount: number | null;
}

const CountCard: React.FC<CountCard> = ({ totalCount, title }) => {
  return (
    <div className="flex-1 bg-white/5 p-6 rounded-xl border border-white/15">
      <div className="">
        <h2 className="text-l text-white/80">{title}</h2>
        {totalCount !== null ? (
          <p className="text-2xl font-semibold">{totalCount}</p>
        ) : (
          <p>Loading...</p>
        )}
      </div>
    </div>
  );
};

export default CountCard;
