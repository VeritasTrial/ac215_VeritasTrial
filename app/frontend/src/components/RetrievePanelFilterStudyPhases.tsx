/**
 * @file RetrievePanelFilterStudyPhases.tsx
 *
 * The filter for the study phases in the retrieval panel, using @radix-ui/themes Select.
 */

import { Dispatch, SetStateAction } from "react";
import { Select } from "@radix-ui/themes";
import { TrialFilters } from "../types";

interface RetrievePanelFilterStudyPhasesProps {
  filters: TrialFilters;
  setFilters: Dispatch<SetStateAction<TrialFilters>>;
}

export const RetrievePanelFilterStudyPhases = ({
  filters,
  setFilters,
}: RetrievePanelFilterStudyPhasesProps) => {
  const options = [
    { value: "all", label: "All" },
    { value: "EARLY_PHASE1", label: "Early Phase" },
    { value: "PHASE1", label: "Phase 1" },
    { value: "PHASE2", label: "Phase 2" },
    { value: "PHASE1, PHASE2", label: "Phase 1 & Phase 2" },
    { value: "PHASE3", label: "Phase 3" },
    { value: "PHASE2, PHASE3", label: "Phase 2 & Phase 3" },
    { value: "PHASE4", label: "Phase 4" },
  ];

  const handleChange = (value: string | undefined) => {
    setFilters((prevFilters) => ({
      ...prevFilters,
      studyPhases: value === "all" ? undefined : value,
    }));
  };

  return (
    <Select.Root
      defaultValue="all"
      value={filters.studyPhases ?? "all"}
      onValueChange={handleChange}
    >
      <Select.Trigger>
        <span>
          {filters.studyPhases
            ? options.find((option) => option.value === filters.studyPhases)?.label
            : "Select a study phase"}
        </span>
      </Select.Trigger>
      <Select.Content>
        {options.map((option) => (
          <Select.Item key={option.value} value={option.value}>
            {option.label}
          </Select.Item>
        ))}
      </Select.Content>
    </Select.Root>
  );
};
