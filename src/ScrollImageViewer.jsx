import { useState } from "react";
import { Scrollama, Step } from "react-scrollama";

const years = Array.from({ length: 2021 - 2000 }, (_, i) => 2000 + i);

export default function ScrollImageViewer() {
  const [currentYear, setCurrentYear] = useState(2000);

  const onStepEnter = ({ data }) => {
    setCurrentYear(data);
  };

  return (
    <div className="relative">
      {/* Sticky image viewer */}
      <div className="sticky top-0 h-screen flex items-center justify-center bg-white z-10">
        <img
          src={`/SI649-final/chart_${currentYear}.png`}
          alt={`Year ${currentYear}`}
          className="max-h-full max-w-full object-contain"
        />
      </div>

      {/* Scroll steps */}
      <div className="relative z-0">
        <Scrollama onStepEnter={onStepEnter} offset={0.5}>
          {years.map((year) => (
            <Step data={year} key={year}>
              <div className="h-screen flex items-center justify-center">
                <div className="text-4xl text-gray-400">{year}</div>
              </div>
            </Step>
          ))}
        </Scrollama>
      </div>
    </div>
  );
}
