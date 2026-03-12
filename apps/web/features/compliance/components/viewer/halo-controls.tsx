"use client";

import React, { useState, useEffect } from "react";
import { Eye, EyeOff, Radio } from "lucide-react";
import { Button } from "@/components/ui/button";

interface HaloControlsProps {
  onToggle: (visible: boolean) => void;
}

export function HaloControls({ onToggle }: HaloControlsProps) {
  const [isVisible, setIsVisible] = useState(true);

  const toggle = () => {
    const next = !isVisible;
    setIsVisible(next);
    onToggle(next);
  };

  return (
    <div className="absolute top-4 right-4 z-50 flex flex-col gap-2">
      <Button 
        variant={isVisible ? "default" : "secondary"} 
        size="sm" 
        onClick={toggle}
        className="shadow-md"
      >
        {isVisible ? <Eye className="mr-2 h-4 w-4" /> : <EyeOff className="mr-2 h-4 w-4" />}
        Spatial Halos
      </Button>
    </div>
  );
}
