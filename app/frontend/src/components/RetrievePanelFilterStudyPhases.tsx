/**
 * @file RetrievePanelFilterStudyPhases.tsx
 *
 * The filter for study phases in the retrieval panel
 */

import { useState } from "react";
import { Checkbox, Flex, Text } from "@radix-ui/themes";
import { Dispatch, SetStateAction } from "react";
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
    { value: "EARLY_PHASE1", label: "Early Phase 1" },
    { value: "PHASE1", label: "Phase 1" },
    { value: "PHASE2", label: "Phase 2" },
    { value: "PHASE3", label: "Phase 3" },
    { value: "PHASE4", label: "Phase 4" },
  ];

  const [selectedValues, setSelectedValues] = useState<string[]>(
    filters.studyPhases?.split(",") ?? []
  );

  const handleCheckboxChange = (value: string) => {
    if (value === "all") {
      if (!selectedValues.includes("all")) {
        setSelectedValues(["all"]);
        setFilters((prevFilters) => ({
          ...prevFilters,
          studyPhases: undefined,
        }));
      } else {
        setSelectedValues([]);
      }
    } else {
      const newValues = selectedValues.includes(value)
        ? selectedValues.filter((v) => v !== value)
        : [...selectedValues.filter((v) => v !== "all"), value];

      setSelectedValues(newValues);

      setFilters((prevFilters) => ({
        ...prevFilters,
        studyPhases: newValues.length > 0 ? newValues.join(", ") : undefined,
      }));
    }
  };

  return (
    <Flex direction="row" gap="4" wrap="wrap">
      {options.map((option) => (
        <Flex key={option.value} align="center" gap="2">
          <Checkbox
            checked={selectedValues.includes(option.value)}
            onCheckedChange={() => handleCheckboxChange(option.value)}
            id={option.value}
          />
          <Text as="label" htmlFor={option.value}>
            {option.label}
          </Text>
        </Flex>
      ))}
    </Flex>
  );
};
