/**
 * @file RetrievePanelFilterStudyType.tsx
 *
 * The filter for the study type in the retrieval panel.
 */

import { Dispatch, SetStateAction } from "react";
import { Flex, RadioGroup } from "@radix-ui/themes";
import { TrialFilters } from "../types";

interface RetrievePanelFilterStudyTypeProps {
  filters: TrialFilters;
  setFilters: Dispatch<SetStateAction<TrialFilters>>;
}

export const RetrievePanelFilterStudyType = ({
  filters,
  setFilters,
}: RetrievePanelFilterStudyTypeProps) => {
  const value = filters.studyType ?? "all";

  const handler = (value: string) => {
    setFilters((prevFilters) => ({
      ...prevFilters,
      studyType: value === "all" ? undefined : value,
    }));
  };

  return (
    <RadioGroup.Root
      variant="surface"
      asChild
      value={value}
      onValueChange={handler}
    >
      <Flex direction="row" gapX="4">
        <RadioGroup.Item value="all">All</RadioGroup.Item>
        <RadioGroup.Item value="interventional">Interventional</RadioGroup.Item>
        <RadioGroup.Item value="observational">Observational</RadioGroup.Item>
      </Flex>
    </RadioGroup.Root>
  );
};
